import server
import pytest
from tests.data import Data


class TestRefactoring:
    """
    class to test each internal function in server
    """

    @classmethod
    def setup_class(cls):
        """ method to re init server data"""
        server.clubs = server.load_clubs()
        server.competitions = server.load_competitions()

    def test_load_clubs(self):
        result = server.load_clubs()
        assert len(result) == 3
        assert result[0] == Data.first_club

    def test_load_competitions(self):
        result = server.load_competitions()
        assert len(result) == 4
        assert result[2] == Data.third_comp

    @pytest.mark.parametrize('value, criteria, points',
                             [("Simply Lift", 'name', "13"),
                              ("4", 'points', "4"),
                              ("kate@shelifts.co.uk", 'email', "12"),
                              ("emmanuel.albisser@gmail.com", 'email', None),
                              ("She Lifts", 'singer', None)])
    def test_get_club_with(self, criteria, value, points):
        """function returns an object club
        with club['criteria']==value"""
        result = server.get_club_with(criteria, value)
        assert type(result) is dict or result is None
        assert result == points or result['points'] == points

    def test_get_competition_with(self):
        # almost same function as previous one, only used on 'name'
        result = server.get_competition_with('name', "Spring Festival 2023")
        assert result == Data.third_comp
        result2 = server.get_competition_with('name', "Spring Festival 2022")
        assert result2 is None
