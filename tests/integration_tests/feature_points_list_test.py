import pytest
from .conftest import client as gudlft_client


class TestPointsList:
    def test_points_list(self, gudlft_client):
        for response in [gudlft_client.get('/point-display'),
                         gudlft_client.get(
                             '/point-display/admin@irontemple.com')]:
            assert response.status_code == 200
            assert '<h2>Points by club :</h2>' in response.data.decode()