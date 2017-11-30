from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Required
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mpei.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
moment = Moment(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    text = db.Column(db.Text)
    author = db.Column(db.String(64))

    def __repr__(self):
        return '<Table %r>' % self.title


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    role = SelectField('Роль', choices=[("admin","Администратор"), ("moder","Модератор"), ("user","Пользователь")])
    submit = SubmitField('Добавить')

class AddNewsForm(FlaskForm):
    title = StringField('Название новости', validators=[DataRequired()])
    text = TextAreaField('Текст новости', validators=[DataRequired()])
    author = StringField('Имя автора', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class DeleteUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class LoginForm(FlaskForm):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class NameForm(FlaskForm):
    name = StringField('Как тебя зовут?', validators=[DataRequired()])
    submit = SubmitField('Отправить')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    newscount = len(News.query.all())
    usercount = len(User.query.all())
    return render_template('index.html', usercount=usercount, newscount=newscount)


@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        if (not (re.match("^[a-z0-9_-]{3,15}$",form.username.data))):
            flash("Имя пользователя должно быть от 3 до 15 символов. Можно использовать строчные латинские буквы от a до z,цифры, дефис и символ нижнего подчеркивания. ")
            return redirect(url_for('adduser'))
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None:
            username = form.username.data
            role = form.role.data
            if(role=="admin"):
                role_db = Role.query.filter_by(id=1).first()
            elif (role=="moder"):
                role_db = Role.query.filter_by(id=2).first()
            else:
                role_db = Role.query.filter_by(id=3).first()
            u = User(username=username,role=role_db)
            db.session.add(u)
            db.session.commit()
            flash("Пользователь %s успешно добавлен в базу" %username)
            return redirect(url_for('userlist'))
        else:
            flash('Имя %s занято'% form.username.data)
        return redirect(url_for('adduser'))
    return render_template('adduser.html', form=form, username=session.get('username'),password=session.get('password'))


@app.route('/userlist', methods=['POST','GET'])
def userlist():
    userlist = User.query.all()
    return render_template('userlist.html', userlist=userlist)


@app.route('/userlist/delete/<id>', methods=['POST','GET'])
def userlistdelete(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        if(not(id is None)):
            flash('Пользователь c идентификатором %s не найден' %id)
            return redirect(url_for('userlist'))

    else:
        db.session.delete(user)
        db.session.commit()
        flash("Пользователь c идентификатором %s успешно удален из базы" % id)
        return redirect(url_for('userlist'))


@app.route('/addnews', methods=['GET', 'POST'])
def addnews():
    form = AddNewsForm()
    if form.validate_on_submit():
        news = News.query.filter_by(title=form.title.data).first()
        if news is None:
            title = form.title.data
            author = form.author.data
            text = form.text.data
            u = News(title=title,author=author, text=text)
            db.session.add(u)
            db.session.commit()
            flash("Новость \"%s\" успешно добавлен в базу" %form.title.data)
            return redirect(url_for('addnews'))
        else:
            flash('Новость с заголовком \"%s\" уже существует'% form.title.data)
            return render_template('addnews.html', form=form, username=session.get('username'),
                                   password=session.get('password'))
    return render_template('addnews.html', form=form, username=session.get('username'),password=session.get('password'))


@app.route('/newslist', methods=['GET', 'POST'])
def newslist():
    news = News.query.all()
    return render_template('newslist.html', newslist=news)


@app.route('/newslist/delete/<id>', methods=['GET', 'POST'])
def newslistdelete(id):
    news = News.query.filter_by(id=id).first()
    if news is None:
        if (not (news is None)):
            flash('Новость с идентификатором %s не найдена' % id)
            newslist = News.query.all()
            return render_template('newslist.html', newslist=newslist)
    else:
        db.session.delete(news)
        db.session.commit()
        flash("Новость с id %s успешно удалена из базы" % id)
        return redirect(url_for('newslist'))




if __name__ == '__main__':
    app.run()