from application import db
from sqlalchemy.orm import sessionmaker


def databases_conection(func):

    def wrapped(*args, **kwargs):

        Session = sessionmaker(bind=db.get_engine())
        session = Session()
        kwargs['session'] = session

        return func(*args, **kwargs)

    return wrapped