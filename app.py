from flask import Flask

from sqlalchemy import create_engine, ForeignKey, String, Integer, Column, VARCHAR, CHAR, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
Base = declarative_base()


class Person(Base):
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


class Util(Base):
    __tablename__ = "util"
    ssn = Column("ssn", Integer, primary_key=True)
    person_counter = Column("person_counter", Integer)

    def __init__(self, ssn, person_counter):
        self.ssn = ssn
        self.person_counter = person_counter

    def __repr__(self):
        return f"({self.ssn} {self.person_counter})"


engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

util = session.query(Util).filter_by(ssn=1).first()
if util is None:
    util = Util(1, 0)
    session.add(util)
    session.commit()


@app.route("/api/v1/user", methods=['POST'])
def add_user():
    person = Person(util.person_counter, "Micha", "Schmitt", "m", 20)
    util.person_counter = util.person_counter + 1
    session.add(person)
    to_update = session.query(Util).filter_by(ssn=1).first()
    to_update.person_counter = util.person_counter
    session.commit()
    return ""


@app.route("/api/v1/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    person = session.query(Person).filter(Person.ssn == user_id)
    return f"<p>{person[0].firstname} {person[0].lastname}'s gender is {person[0].gender} and he is {person[0].age} years old.</p>"


@app.route("/api/v1/user", methods=['GET'])
def get_users():
    people = session.query(Person)
    result = ""
    for person in people:
        result = result + f"<p>{person.firstname} {person.lastname}'s gender is {person.gender} and he is {person.age} years old. His ID is {person.ssn}</p>"
    return result


@app.route("/")
def index():
    return ""
