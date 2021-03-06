# Import the database object (db) from the main application module
from server import db

# SQLAlchemy Exceptions
from sqlalchemy import exc as SQLexc

# UUID type for SQLAlchemy
from misc.uuid import UUID
import uuid

# Required for timestamps
import datetime as dt


class User(db.Model):
    user_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)

    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # password = db.Column(db.String(180))

    first_name = db.Column(db.String(120), default='')
    last_name = db.Column(db.String(120), default='')

    # Note: This data is entirely optional
    blog_url = db.Column(db.String(120), default='')
    profile_fb = db.Column(db.String(120), default='')
    profile_twitter = db.Column(db.String(120), default='')

    # Note: The UTC timestamps will be converted to correct timezones
    # by the client
    created_on = db.Column(db.DateTime, default=dt.datetime.utcnow())
    last_login_on = db.Column(db.DateTime, default=dt.datetime.utcnow())

    def __init__(self, username, email):
        self.username = username
        self.email = email
        # self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def new(username, email):
        """
        Add a new user to the database
        """
        new_user = User(username, email)
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLexc.IntegrityError as e:
            # Todo: Raise a proper exception
            # that the view will catch
            # raise(e)
            db.session.rollback()

    def update(self, **kwargs):
        """
        Update a user's data to new values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    @property
    def json(self):
        """
        Return the user's data in json form
        """
        json = {}
        for prop, val in vars(self).items():
            if not prop.startswith('_'):
                json.update({prop: str(val)})
        return json
