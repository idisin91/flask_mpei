import re
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, jsonify
from . import main
from .forms import AddUserForm, AddNewsForm
from .. import db
from ..models import User, Role, News


# home page
@main.route('/', methods=['GET', 'POST'])
def index():
    admins = User.query.filter_by(role_id=1)
    newscount = len(News.query.all())
    usercount = len(User.query.all())
    return render_template('index.html', usercount=usercount, newscount=newscount, admins=admins)

# adding user
@main.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        if (not (re.match("^[A-Za-z0-9_-]{3,15}$",form.username.data))):
            flash("Имя пользователя должно быть от 3 до 15 символов. Можно использовать строчные латинские буквы от a до z,цифры, дефис и символ нижнего подчеркивания. ")
            return redirect(url_for('.adduser'))
        username = form.username.data.lower()
        user = User.query.filter_by(username=username).first()
        if user is None:
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
            return redirect(url_for('.userlist'))
        else:
            flash('Имя %s занято'% form.username.data)
        return redirect(url_for('adduser'))
    return render_template('adduser.html', form=form, username=session.get('username'), password=session.get('password'))

# list of all users
@main.route('/userlist', methods=['POST', 'GET'])
def userlist():
    userlist = User.query.all()
    return render_template('userlist.html', userlist=userlist)

# deleting user
@main.route('/userlist/delete/<id>', methods=['POST', 'GET'])
def userlistdelete(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('Пользователь c идентификатором %s не найден' %id)
        return redirect(url_for('.userlist'))

    else:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash("Пользователь %s успешно удален из базы" % username)
        return redirect(url_for('.userlist'))

# adding news
@main.route('/addnews', methods=['GET', 'POST'])
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
            return redirect(url_for('.newslist'))
        else:
            flash('Новость с заголовком \"%s\" уже существует'% form.title.data)
            return render_template('addnews.html', form=form, username=session.get('username'),
                                   password=session.get('password'))
    return render_template('addnews.html', form=form, username=session.get('username'), password=session.get('password'))

# list of all news
@main.route('/newslist', methods=['GET', 'POST'])
def newslist():
    news = News.query.all()
    return render_template('newslist.html', newslist=news)

# deleting news
@main.route('/newslist/delete/<id>', methods=['GET', 'POST'])
def newslistdelete(id):
    news = News.query.filter_by(id=id).first()
    if news is None:
        flash('Новость с идентификатором %s не найдена' % id)
        newslist = News.query.all()
        return render_template('newslist.html', newslist=newslist)
    else:
        db.session.delete(news)
        db.session.commit()
        flash("Новость с id %s успешно удалена из базы" % id)
        return redirect(url_for('.newslist'))

# list of all news in JSON format
@main.route('/api/1.0/news/', methods=['GET'])
def api_getnews():
    newslist = News.query.limit(30).offset(0)
    news = []
    for item in newslist:
        news.append(
            {
                'id':item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'link': item.link
            }
        )
    return jsonify({'news': news})

# list of all news in JSON format with offset
@main.route('/api/1.0/news/offset/<offset>', methods=['GET'])
def api_getnews_offset(offset):
    newslist = News.query.offset(offset).limit(30)
    news = []
    for item in newslist:
        news.append(
            {
                'id':item.id,
                'title': item.title,
                'text': item.text,
                'author': item.author,
                'link': item.link
            }
        )
    return jsonify({'news': news})


# data of news with id
@main.route('/api/1.0/news/<id>', methods=['GET'])
def api_get_by_id(id):
    item = News.query.filter_by(id=id).first()
    if item is None:
        return jsonify({'news': []})

    news = {
            'id':item.id,
            'title': item.title,
            'text': item.text,
            'author': item.author,
            'link': item.link
        }
    return jsonify({'news': news})
