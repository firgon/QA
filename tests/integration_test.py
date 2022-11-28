from tests.conftest import client as gudlft_client
import pytest

from tests.unit_test import Data


class TestIntegration:

    def test_index_should_return_status_code_200(self, gudlft_client):
        response = gudlft_client.get('/')
        assert response.status_code == 200

    def test_is_correct_required_places_but_not_enough(self):
        pass

    @pytest.mark.parametrize('email, status_code',
                             [('emmanuel.albisser@gmail.com', 302),
                              ('john@simplylift.co', 200)])
    def test_post_show_summary_should_return_status_code_200(self,
                                                             gudlft_client,
                                                             email,
                                                             status_code):
        response = gudlft_client.post('/showSummary',
                                      data={'email': email})
        assert response.status_code == status_code
        if response.status_code == 200:
            assert f'<h2>Welcome, {email} </h2>' in response.data.decode()

    @pytest.mark.parametrize('name, email, status_code',
                             [('emmanuel.albisser', None, 302),
                              ('Simply Lift', 'john@simplylift.co', 200)])
    def test_get_show_summary_should_return_status_code_200(self,
                                                            gudlft_client,
                                                            name,
                                                            email,
                                                            status_code):
        response = gudlft_client.get(f'/showSummary/{name}')
        assert response.status_code == status_code
        if response.status_code == 200:
            assert f'<h2>Welcome, {email} </h2>' in response.data.decode()

    def test_points_list(self, gudlft_client):
        for response in [gudlft_client.get('/point-display'),
                         gudlft_client.get(
                             '/point-display/admin@irontemple.com')]:
            assert response.status_code == 200
            assert '<h2>Points by club :</h2>' in response.data.decode()

    def test_book_ok(self, gudlft_client):
        response = \
            gudlft_client.get('/book/Spring%20Festival%202023/Iron%20Temple')
        assert response.status_code == 200
        assert '<h2>Spring Festival 2023</h2>' in response.data.decode()

    def test_book_not_ok(self, gudlft_client):
        """test book page with an unknown club"""
        response = \
            gudlft_client.get('/book/Spring%20Festival%202023/EmmanuelAlbis')
        assert response.status_code == 200
        assert 'Something went wrong-please try again' \
               in response.data.decode()

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
        (6, Data.first_club, Data.third_comp, 'Great-booking complete!'),
        (3, Data.second_club, Data.third_comp, 'Great-booking complete!')
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
        assert answer in response.data.decode()

    def test_logout(self, gudlft_client):
        response = gudlft_client.get('/logout')
        assert response.status_code == 302
