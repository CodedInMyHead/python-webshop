from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.Common import Common
from dto.UtilDTO import UtilDTO


def create_app():
    app_flask = Flask(__name__)
    return app_flask


def create_engines():
    engine = create_engine('sqlite:///data.db')
    Common.base.metadata.create_all(bind=engine)
    sm = sessionmaker(bind=engine)
    session = sm()
    temp_util = session.query(UtilDTO).filter_by(ssn=1).first()
    if temp_util is None:
        temp_util = UtilDTO(1, 0)
        session.add(temp_util)
        session.commit()

    return session, temp_util


app = create_app()
sqlite_session, util = create_engines()


@app.route("/")
def index():
    return render_template('index.html')
