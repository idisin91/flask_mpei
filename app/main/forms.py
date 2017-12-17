from wtforms import StringField, SubmitField, DateField, TextField, BooleanField, SelectField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Required

class AddUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    role = SelectField('Роль', choices=[("admin","Администратор"), ("moder","Модератор"), ("user","Пользователь")])
    submit = SubmitField('Добавить')


class AddNewsForm(FlaskForm):
    title = StringField('Название новости', validators=[DataRequired()])
    author = StringField('Имя автора', validators=[DataRequired()])
    text = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class DeleteUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class NameForm(FlaskForm):
    name = StringField('Как тебя зовут?', validators=[DataRequired()])
    submit = SubmitField('Отправить')
