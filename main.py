import logging

from flask import Flask

from sqlalchemy import create_engine, ForeignKey, String, Integer, Column, VARCHAR, CHAR, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
Base = declarative_base()

ct = 30


class Person(Base):
    __tablename__ = "people"
    ssn = Column("ssn", Integer, primary_key=True)
    firstname = Column("firstname", VARCHAR)
    lastname = Column("lastname", VARCHAR)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, first, last, gender, age):
        self.ssn = ssn
        self.first = first
        self.last = last
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"({self.ssn} {self.first} {self.last} {self.gender} {self.age})"


engine = create_engine('postgresql://micha:a0cb03f17886@localhost:5432/data')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route("/user", methods=['POST'])
def add_user():
    global ct
    person = Person(ct, "Micha", "Schmitt", "m", 20)
    session.add(person)
    session.commit()
    ct = ct + 1
    return ""


@app.route("/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    person = session.query(Person).filter(Person.ssn == user_id)
    return f"<p>{person[0].firstname} {person[0].lastname}'s gender is {person[0].gender} and he is {person[0].age} years old.</p>"


@app.route("/user", methods=['GET'])
def get_users():
    people = session.query(Person)
    logging.log()
    result = ""
    for person in people:
        result = result + f"<p>{person.firstname} {person.lastname}'s gender is {person.gender} and he is {person.age} years old. His ID is {person.ssn}</p>"
    return result
