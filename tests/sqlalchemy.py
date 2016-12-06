from sqlalchemy import create_engine, event, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('user.id'))

    parent = relationship(
        'UserModel', backref='children', remote_side=[id], uselist=False)


def make_engine():
    """Return an engine instance."""
    return create_engine('sqlite://')


def make_session(engine):
    """Return a SQLAlchemy session factory."""
    return sessionmaker(bind=engine)()


class SQLAlchemyTestMixin(object):

    def setUp(self):
        """Create a save point and start the session."""
        self.engine = engine
        self.session = self.make_session()
        self.session.begin_nested()

    def make_session(self):
        return make_session(self.engine)

    def tearDown(self):
        """Close the session and rollback to the previous save point."""
        self.session.rollback()
        self.session.close()

    @classmethod
    def setUpClass(cls):
        """Create the database."""
        global engine

        engine = make_engine()

        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            dbapi_connection.isolation_level = None

        @event.listens_for(engine, "begin")
        def do_begin(conn):
            conn.execute("BEGIN")

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        """Destroy the database."""
        engine.dispose()
