import pytest
from .conftest import client as gudlft_client


class TestUnknownUser:
    @pytest.mark.parametrize('email, status_code',
                             [('emmanuel.albisser@gmail.com', 302),
                              ('john@simplylift.co', 200)])
    def test_post_show_summary_should_return_status_code_200(self,
                                                             gudlft_client,
                                                             email,
                                                             status_code):
        """ShowSummary route must be accessible only to identified users
        redirect (code:302) if email is not known"""

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
        """Same as previous test but with GET request"""
        response = gudlft_client.get(f'/showSummary/{name}')
        assert response.status_code == status_code
        if response.status_code == 200:
            assert f'<h2>Welcome, {email} </h2>' in response.data.decode()

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
