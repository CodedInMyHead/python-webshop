from flask import Flask, render_template

from sqlalchemy import create_engine, String, Integer, Column, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_app():
    app_flask = Flask(__name__)
    base_var = declarative_base()
    return app_flask, base_var


def create_engines():
    engine = create_engine('sqlite:///data.db')
    base.metadata.create_all(bind=engine)
    sm = sessionmaker(bind=engine)
    session = sm()
    return session


app, base = create_app()


class Person(base):
    __tablename__ = "people"
    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.firstname = first
        self.lastname = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn} {self.first} {self.last} {self.gender} {self.age})"


class Util(base):
    __tablename__ = "util"
    ssn = Column("ssn", Integer, primary_key=True)
    person_counter = Column("person_counter", Integer)

    def __init__(self, ssn, person_counter):
        self.ssn = ssn
        self.person_counter = person_counter

    def __repr__(self):
        return f"({self.ssn} {self.person_counter})"


sqlite_session = create_engines()

util = sqlite_session.query(Util).filter_by(ssn=1).first()
if util is None:
    util = Util(1, 0)
    sqlite_session.add(util)
    sqlite_session.commit()


@app.route("/api/v1/user", methods=['POST'])
def add_user():
    person = Person(util.person_counter, "Micha", "Schmitt", "m", 20)
    util.person_counter = util.person_counter + 1
    sqlite_session.add(person)
    to_update = sqlite_session.query(Util).filter_by(ssn=1).first()
    to_update.person_counter = util.person_counter
    sqlite_session.commit()
    return ""


@app.route("/api/v1/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    person = sqlite_session.query(Person).filter(Person.ssn == user_id)
    return f"<p>{person[0].firstname} {person[0].lastname}'s gender is {person[0].gender} and he is {person[0].age} years old.</p>"


@app.route("/api/v1/user", methods=['GET'])
def get_users():
    people = sqlite_session.query(Person)
    result = ""
    for person in people:
        result = result + f"<p>{person.firstname} {person.lastname}'s gender is {person.gender} and he is {person.age} years old. His ID is {person.ssn}</p>"
    return result


@app.route("/")
def index():
    return render_template('index.html')
