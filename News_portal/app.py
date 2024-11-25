from flask import Flask, render_template, request, redirect, url_for, flash, abort  
from datetime import datetime  
from forms import NewsForm, SearchForm  
from models import db, NewsArticle  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.secret_key = 'supersecretkey'  
db.init_app(app)  

# Создаем базу данных и таблицы  
with app.app_context():  
    db.create_all()  

censored_words = ['редиска', 'редиске', 'редиски', 'редиску']  

def censor(text):  
    if not isinstance(text, str):  
        raise ValueError("filter censor должен применяться только к строкам")  
    for word in censored_words:  
        replacement = word[0] + '*' * (len(word) - 1)  
        text = text.replace(word, replacement)  
    return text  

@app.route('/news/', methods=['GET'])  
def news_list():  
    page = request.args.get('page', 1, type=int)  
    per_page = 10  
    # Получаем все статьи с пагинацией  
    pagination = NewsArticle.query.order_by(NewsArticle.date.desc()).paginate(page=page, per_page=per_page, error_out=False) 
    articles = pagination.items  
    return render_template('news_list.html', news=articles, pagination=pagination)  

@app.route('/news/create/', methods=['GET', 'POST'])  
def news_create():  
    form = NewsForm()  
    if form.validate_on_submit():  
        new_article = NewsArticle(  
            title=form.title.data,  
            content=form.content.data,  
            date=datetime.now(),  
            article_type='новость'  # автоматически выставляем значение  
        )  
        db.session.add(new_article)  
        db.session.commit()  
        flash('Статья успешно создана!', 'success')  
        return redirect(url_for('news_list'))  
    return render_template('news_create.html', form=form)  

@app.route('/news/<int:news_id>/edit/', methods=['GET', 'POST'])  
def news_edit(news_id):  
    article = NewsArticle.query.get_or_404(news_id)  
    form = NewsForm(obj=article)  
    if form.validate_on_submit():  
        article.title = form.title.data  
        article.content = form.content.data  
        db.session.commit()  
        flash('Статья успешно обновлена!', 'success')  
        return redirect(url_for('news_detail', news_id=article.id))  
    return render_template('news_edit.html', form=form, article=article)  

@app.route('/news/<int:news_id>/delete/', methods=['GET', 'POST'])  
def news_delete(news_id):  
    article = NewsArticle.query.get_or_404(news_id)  
    if request.method == 'POST':  
        db.session.delete(article)  
        db.session.commit()  
        flash('Статья успешно удалена!', 'success')  
        return redirect(url_for('news_list'))  
    return render_template('news_delete.html', article=article)  

@app.route('/news/search', methods=['GET'])  
def news_search():  
    form = SearchForm()  
    articles = []  
    if form.validate_on_submit():  
        # Фильтрация по критериям  
        query = NewsArticle.query  
        if form.title.data:  
            query = query.filter(NewsArticle.title.contains(form.title.data))  
        if form.date.data:  
            query = query.filter(NewsArticle.date >= form.date.data)  
        articles = query.all()  
    return render_template('search.html', form=form, articles=articles)  

@app.route('/news/<int:news_id>/', methods=['GET'])  
def news_detail(news_id):  
    article = NewsArticle.query.get_or_404(news_id)  
    article.title = censor(article.title)  
    article.content = censor(article.content)  
    formatted_date = article.date.strftime('%d.%m.%Y')  
    return render_template('news_detail.html', article=article, date=formatted_date)  

if __name__ == '__main__':  
    app.run(debug=True)