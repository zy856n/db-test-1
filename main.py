from flask import Flask, request, flash, url_for, redirect, render_template

from sqlalchemy import create_engine, Column, Integer, String, insert
from sqlalchemy.orm import declarative_base, sessionmaker

from os import path

# Using sqlalchemy ORM

app = Flask(__name__)

basedir = path.abspath("instance/")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{path.join(basedir, "database.db")}"
app.config['SECRET_KEY'] = "random string"

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base = declarative_base()

class Students(Base):
    __tablename__ = "Students"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(100))
    city = Column(String(50))
    addr = Column(String(200)) 
    pin = Column(String(10))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def show_all():
   students = session.query(Students).all()
   return render_template('showall.html', students = students)

@app.route('/new', methods = ['GET', 'POST'])
def new():

    if request.method == "POST":
        if not request.form["name"] or not request.form["city"] or not request.form["addr"] or not request.form["pin"]:
            flash("Please enter all the fields", "error")
        else:
            new_student = Students(name=request.form['name'], city=request.form['city'],
            addr=request.form['addr'], pin=request.form['pin'])
            session.add(new_student)
            session.commit()
            flash("Record successfully added.")
            return redirect(url_for("show_all"))

    return render_template("new.html")

if __name__ == '__main__':
   app.run(debug = True)