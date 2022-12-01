from flask import Flask
from flask_testing import LiveServerTestCase
from tests.data import Data
from .utils import Utils
import server


class TestAuthentication:

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile('test_config.py')
        self.app.config['FLASK_APP'] = "server.py"
        return self.app

    def test_signup_ok(self):
        """
        Try first with a known user and access to website
        """
        utils = Utils()

        utils.enter_email(Data.first_club['email'])
        utils.click_button()

        title = utils.get_h2()

        assert title == f"Welcome, {Data.first_club['email']}"

        utils.close()

    def test_signup_unknown_user(self):
        """
        Try first with a fake user and get a message error
        """
        utils = Utils()

        utils.enter_email("emmanuel.albisser@gmail.com")
        utils.click_button()

        flash = utils.get_flash()

        assert "You are not registered. You can't connect." == flash

        utils.close()
