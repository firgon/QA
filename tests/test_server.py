from server import load_clubs, load_competitions
from tests.conftest import client as gudlft_client
import pytest


class TestServer:

    def test_load_clubs(self):
        result = load_clubs()
        assert len(result) == 3
        assert result[0] == {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        }

    def test_load_competitions(self):
        result = load_competitions()
        assert len(result) == 2
        assert result[1] == {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }

    def test_index_should_return_status_code_200(self, gudlft_client):
        response = gudlft_client.get('/')
        assert response.status_code == 200

    @pytest.mark.parametrize('email, status_code',
                             [('emmanuel.albisser@gmail.com', 403),
                              ('john@simplylift.co', 200)])
    def test_show_summary_should_return_status_code_200(self,
                                                        gudlft_client,
                                                        email,
                                                        status_code):
        response = gudlft_client.post('/showSummary',
                                      data={'email': email})
        assert response.status_code == status_code
