from flask import Blueprint

from app import util, sqlite_session
from dto.UserDTO import PersonDTO
from dto.UtilDTO import UtilDTO
from common.Common import Common

bp_index = Blueprint('user', __name__)


@bp_index.route(Common.api_prefix + "user", methods=['POST'])
def add_user():
    person = PersonDTO(util.person_counter, "Micha", "Schmitt", "m", 20)
    util.person_counter = util.person_counter + 1
    sqlite_session.add(person)
    to_update = sqlite_session.query(UtilDTO).filter_by(ssn=1).first()
    to_update.person_counter = util.person_counter
    sqlite_session.commit()
    return ""


@bp_index.route(Common.api_prefix + "user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    person = sqlite_session.query(PersonDTO).filter(PersonDTO.ssn == user_id)
    return f"<p>{person[0].firstname} {person[0].lastname}'s gender is {person[0].gender} and he is {person[0].age} years old.</p>"


@bp_index.route(Common.api_prefix + "user", methods=['GET'])
def get_users():
    people = sqlite_session.query(PersonDTO)
    result = ""
    for person in people:
        result = result + f"<p>{person.firstname} {person.lastname}'s gender is {person.gender} and he is {person.age} years old. His ID is {person.ssn}</p>"
    return result
