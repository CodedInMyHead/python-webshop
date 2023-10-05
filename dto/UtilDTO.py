from sqlalchemy import Column, Integer
from common.common import common


class UtilDTO(common.base):
    __tablename__ = "util"
    ssn = Column("ssn", Integer, primary_key=True)
    person_counter = Column("person_counter", Integer)

    def __init__(self, ssn, person_counter):
        self.ssn = ssn
        self.person_counter = person_counter

    def __repr__(self):
        return f"({self.ssn} {self.person_counter})"