
from unittest import TestCase
import os
from app import app
from db import db

"""
THIS CLASS IS THE PARENT CLASS TO NON-UNIT TEST
ALLOWS FOR INSTANTIATION OF DATABASE DYNAMICALLY
ENSURES THAT IT A NEW, BLANK DATABASE EACH TIME

1. SET UP THE DATABASE AND GIVE THE TEST CLIENT
"""

class SystemBaseTest(TestCase):
    # runs for each test case
    @classmethod
    def setUpClass(cls) -> None:
        # make sure DB exists
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///')
        app.config['DEBUG'] = False
        #  propagate exceptions bubble exceptions thrown hierarchically
        app.config['PROPAGATE-EXCEPTIONS'] = True

        with app.app_context():
            db.init_app(app)
    # runs for each test method

    def setUp(self) -> None:
        # make sure DB exists
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///')

        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self) -> None:
        # ensure the DB is blanked and dropped
        with app.app_context():
            db.session.remove()
            db.drop_all()

