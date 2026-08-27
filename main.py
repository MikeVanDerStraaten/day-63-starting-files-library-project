from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
# initialize the app with the extension
db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    rating: Mapped[int]

with app.app_context():
    db.create_all()

with app.app_context():
    books = Books(title="Harry Pots", author="J. K. Rowling", rating=9)
    db.session.add(books)
    db.session.commit()

# Read All Records

with app.app_context():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.fetchall()
print(all_books)

all_books = []


@app.route('/', methods=['POST','GET'])
def home():
    return render_template('index.html', all_books=all_books)

@app.route("/add", methods=['POST','GET'])
def add():
    if request.method == 'POST':
        data = dict(request.form)
        all_books.append(data)
        return redirect(url_for('home'))
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

