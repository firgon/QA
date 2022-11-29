# from flask_testing import LiveServerTestCase
# from selenium import webdriver
# from server import app
#
#
# class TestAuthentication(LiveServerTestCase):
#
#     pass
#
#     def create_app(self):
#         return app
#
#     # def setUp(self) -> None:
#     #     self.browser = webdriver.Chrome("tests/functional_tests/chromedriver")
#     #
#     # def tearDown(self) -> None:
#     #     self.browser.close()
#
#     def test_signup(self):
#         # Ouvrir le navigateur avec le webdriver
#         self.browser = webdriver.Firefox()
#         self.browser.get('http://127.0.0.1:5000/')
#
#         assert self.browser.current_url == 'http://127.0.0.1:5000'
