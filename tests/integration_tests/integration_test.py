class TestIntegration:

    def test_index_should_return_status_code_200(self, gudlft_client):
        response = gudlft_client.get('/')
        assert response.status_code == 200

    def test_logout(self, gudlft_client):
        response = gudlft_client.get('/logout')
        assert response.status_code == 302
