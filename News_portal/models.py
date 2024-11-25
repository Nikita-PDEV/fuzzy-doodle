from flask_sqlalchemy import SQLAlchemy  

db = SQLAlchemy()  

class NewsArticle(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), nullable=False)  
    content = db.Column(db.Text, nullable=False)  
    date = db.Column(db.DateTime, default=db.func.current_timestamp())  
    article_type = db.Column(db.String(50), default='новость')