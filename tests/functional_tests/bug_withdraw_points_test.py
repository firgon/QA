from tests.data import Data
from .utils import Utils


class TestWithdrawPoints:

    def test_withdraw_points(self):
        """
        Connect and book 2 places,
        check that point amount of the club decrease by 2
        """
        utils = Utils()

        utils.enter_email(Data.first_club['email'])
        utils.click_button()

        points_before = utils.get_points()

        utils.click_book_link()

        utils.enter_required_places(2)
        utils.click_button()

        points_after = utils.get_points()

        assert points_before - points_after == 2

        utils.close()


