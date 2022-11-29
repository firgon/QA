import server
import pytest
from tests.data import Data


class TestRequiredPlaces:

    @pytest.mark.parametrize('required, club, competition, bool_answer', [
        (-1, Data.first_club, Data.third_comp, False),  # negative
        (13, Data.first_club, Data.third_comp, False),  # more than 12
        (5, Data.second_club, Data.third_comp, False),  # more than points
        (6, Data.first_club, Data.third_comp, True),
        (6, Data.first_club, Data.first_fake_comp, False),  # more than places
        (3, Data.second_club, Data.third_comp, True),
        (3, None, Data.third_comp, False),
        (3, Data.second_club, None, False),
    ])
    def test_is_correct_required_places(self, required, club,
                                        competition, bool_answer):
        answer, message = \
            server.is_correct_required_places(required, club, competition)
        assert answer == bool_answer
