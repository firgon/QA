import pytest

import server
from .conftest import client as gudlft_client
from tests.data import Data


class TestWithdrawPoints:
    def test_withdraw_points(self, gudlft_client):
        club = server.clubs[0]
        points_before = club['points']
        response = gudlft_client.post('/purchasePlaces', data={
            'competition': Data.third_comp['name'],
            'club': club['name'],
            'places': 1
        })
        assert response.status_code == 200
        points_after = club['points']
        assert points_before - points_after == 1
