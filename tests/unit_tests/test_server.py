import server
from tests.conftest import client as gudlft_client
import pytest


class TestServer:
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

    first_fake_competition = {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "5"
    }

    third_competition = {
        "name": "Spring Festival 2023",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "25"
    }

    def test_load_clubs(self):
        result = server.load_clubs()
        assert len(result) == 3
        assert result[0] == self.first_club

    def test_load_competitions(self):
        result = server.load_competitions()
        assert len(result) == 4
        assert result[2] == self.third_competition

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
        assert result == self.third_competition

    @pytest.mark.parametrize('required, club, competition, bool_answer', [
        (-1, first_club, third_competition, False),  # negative
        (13, first_club, third_competition, False),  # more than 12
        (5, second_club, third_competition, False),  # more than points
        (6, first_club, third_competition, True),
        (6, first_club, first_fake_competition, False),  # more than places
        (3, second_club, third_competition, True),
    ])
    def test_is_correct_required_places(self, required, club,
                                        competition, bool_answer):
        answer, message = \
            server.is_correct_required_places(required, club, competition)
        assert answer == bool_answer

    @pytest.mark.parametrize('competition, boolean', [
        (first_fake_competition, False),
        (third_competition, True)
    ])
    def test_check_competition_date(self, competition, boolean):
        assert server.check_competition_date(competition) == boolean

    def test_index_should_return_status_code_200(self, gudlft_client):
        response = gudlft_client.get('/')
        assert response.status_code == 200

    def test_is_correct_required_places_but_not_enough(self):
        pass

    @pytest.mark.parametrize('email, status_code',
                             [('emmanuel.albisser@gmail.com', 302),
                              ('john@simplylift.co', 200)])
    def test_show_summary_should_return_status_code_200(self,
                                                        gudlft_client,
                                                        email,
                                                        status_code):
        response = gudlft_client.post('/showSummary',
                                      data={'email': email})
        assert response.status_code == status_code
