import pytest

from tests.data import Data
from .utils import Utils
import pytest


class TestRequiredPlacesCheck:

    @pytest.mark.parametrize('required_places, club, answer', [
        (-1, Data.first_club,
         "You can't book 0 or less places !"),  # negative
        (0, Data.first_club,
         "You can't book 0 or less places !"),  # zero
        (13, Data.first_club,
         "You can't book more than 12"),  # more than 12
        (8, Data.first_club, 'Great-booking complete!'),
        (8, Data.first_club,
         "You don't have enough points to book 8 places !"),
        (8, Data.third_club,
         "Great-booking complete!"),

    ])
    def test_required_place_check(self, required_places, club, answer):
        """
        Connect and book x places,
        check that the response corresponds to what is expected
        """
        utils = Utils()

        utils.enter_email(club['email'])
        utils.click_button()

        utils.click_book_link()

        utils.enter_required_places(required_places)
        utils.click_button()

        assert answer in utils.get_flash()

        utils.close()


