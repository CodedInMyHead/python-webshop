from sqlalchemy.ext.declarative import declarative_base


class Common:
    __tablename__ = "common"
    base = declarative_base()
    api_prefix = "/api/v1/"
