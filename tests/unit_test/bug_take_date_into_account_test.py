import server
import pytest
from tests.data import Data


class TestTakeDateIntoAccount:

    @pytest.mark.parametrize('competition, boolean', [
        (Data.first_fake_comp, False),
        (Data.third_comp, True)
    ])
    def test_check_competition_date(self, competition, boolean):
        assert server.check_competition_date(competition) == boolean
