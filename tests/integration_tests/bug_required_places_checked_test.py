import pytest
from .conftest import client as gudlft_client
from tests.data import Data


class TestRequiredPlacesChecked:
    @pytest.mark.parametrize('places, club, competition, answer', [
        (-1, Data.first_club, Data.third_comp,
         "You can&#39;t book 0 or less places !"),  # negative
        (0, Data.first_club, Data.third_comp,
         "You can&#39;t book 0 or less places !"),  # zero
        (13, Data.first_club, Data.third_comp,
         "You can&#39;t book more than 12 places !"),  # more than 12
        (5, Data.second_club, Data.third_comp,
         "You don&#39;t have enough points"),  # more than points
        (5, Data.first_club, Data.first_fake_comp,
         "You can&#39;t book in a past competition"),  # past competition
        (8, Data.first_club, Data.second_comp, 'Great-booking complete!')
    ])
    def test_purchase_places(self, gudlft_client,
                             places, club, competition,
                             answer):
        response = gudlft_client.post('/purchasePlaces', data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places
        })
        assert response.status_code == 200
        if answer not in response.data.decode():
            print(response.data.decode())
        assert answer in response.data.decode()
