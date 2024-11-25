from flask_wtf import FlaskForm  
from wtforms import StringField, TextAreaField, DateField, SubmitField  
from wtforms.validators import DataRequired, Optional  

class NewsForm(FlaskForm):  
    title = StringField('Заголовок', validators=[DataRequired()])  
    content = TextAreaField('Содержимое', validators=[DataRequired()])  
    submit = SubmitField('Сохранить')  

class SearchForm(FlaskForm):  
    title = StringField('Поиск по заголовку', validators=[Optional()])  
    date = DateField('Дата с', format='%Y-%m-%d', validators=[Optional()])  
    submit = SubmitField('Поиск')