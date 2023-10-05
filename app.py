from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.common import common
from dto.UtilDTO import UtilDTO


def __init__(self):
    self.sqlite_session, self.util = create_engines()


def create_app():
    app_flask = Flask(__name__)
    return app_flask


app = create_app()


def create_engines(self):
    engine = create_engine('sqlite:///data.db')
    common.base.metadata.create_all(bind=engine)
    sm = sessionmaker(bind=engine)
    session = sm()
    temp_util = self.sqlite_session.query(UtilDTO).filter_by(ssn=1).first()
    if temp_util is None:
        temp_util = UtilDTO(1, 0)
        self.sqlite_session.add(temp_util)
        self.sqlite_session.commit()
    return session, temp_util


@app.route("/")
def index():
    return render_template('index.html')
