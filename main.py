#Импорт
from flask import Flask, render_template,request, redirect
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(100), primary_key=False)
    #Текст
    text = db.Column(db.VARCHAR(50), nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'



#Запуск страницы с контентом
@app.route('/')
def index():
    return render_template('index.html')


#Динамичные скиллы
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    button_tg = request.form.get('button_tg')
    button_html = request.form.get('button_html')
    button_db = request.form.get('button_db')
    return render_template('index.html', button_python=button_python, button_tg=button_tg, button_html=button_html, button_db=button_db)

#Результаты формы
@app.route('/submit',methods=['POST'])
def submit():
    email = request.form['email']
    text = request.form['text']

    #Создание объкта для передачи в дб

    card = Card(email=email, text=text)

    db.session.add(card)
    db.session.commit()
    return redirect('/form_result')

#Запуск страницы с контентом
@app.route('/form_result')
def form_result():
    #Отображение объектов из БД
    cards = Card.query.order_by(Card.id).all()
    return render_template('form_result.html', cards=cards)


#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)



if __name__ == "__main__":
    app.run(debug=True)