from flask_testing import LiveServerTestCase
from tests.data import Data
from .utils import Utils
import server


class TestAuthentication(LiveServerTestCase):

    def create_app(self):
        return server.app

    def test_signup(self):
        """
        Try first with a fake user get a message error,
        try then with a known user and access to website
        """
        utils = Utils()

        utils.enter_email("emmanuel.albisser@gmail.com")
        utils.click_button()

        flash = utils.get_flash()

        assert "You are not registered. You can't connect." == flash

        utils.enter_email(Data.first_club['email'])
        utils.click_button()

        title = utils.get_h2()

        assert title == f"Welcome, {Data.first_club['email']}"

        utils.close()
