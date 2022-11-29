import server
import pytest


class Data:
    second_club = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    first_club = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }

    third_club = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }

    first_fake_comp = {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "5"
    }

    second_comp = {
            "name": "Fall Classic 2023",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "13"
        }

    third_comp = {
        "name": "Spring Festival 2023",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "25"
    }


class TestServer:

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

    @pytest.mark.parametrize('competition, boolean', [
        (Data.first_fake_comp, False),
        (Data.third_comp, True)
    ])
    def test_check_competition_date(self, competition, boolean):
        assert server.check_competition_date(competition) == boolean
