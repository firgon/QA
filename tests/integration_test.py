from tests.conftest import client as gudlft_client
import pytest


class TestIntegration:

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
        if response.status_code == 200:
            assert f'<h2>Welcome, {email} </h2>' in response.data.decode()

    def test_points_list(self, gudlft_client):
        for response in [gudlft_client.get('/point-display'),
                         gudlft_client.get(
                             f'/point-display/admin@irontemple.com')]:
            assert response.status_code == 200
            assert '<h2>Points by club :</h2>' in response.data.decode()
