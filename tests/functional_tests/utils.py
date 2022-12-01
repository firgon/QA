from selenium import webdriver
from selenium.webdriver.common.by import By
import server


class Utils:

    def __init__(self):

        self.browser = webdriver.Chrome()
        self.browser.get('http://127.0.0.1:5000/')

    def close(self):
        self.browser.close()

    def enter_email(self, email: str):
        """enter email on route '/' page """
        text_input = self.browser.find_element(By.NAME, 'email')
        text_input.send_keys(email)

    def click_button(self):
        button = self.browser.find_element(By.TAG_NAME, 'button')
        button.click()

    def click_book_link(self):
        link = self.browser.find_element(By.LINK_TEXT, 'Book Places')
        link.click()

    def enter_required_places(self, required_places: int):
        """enter a number in places input on book page"""
        places_input = self.browser.find_element(By.NAME, 'places')
        places_input.send_keys(required_places)

    def get_flash(self) -> str:
        return self.browser.find_element(By.TAG_NAME, 'li').text

    def get_h2(self) -> str:
        return self.browser.find_element(By.TAG_NAME, 'h2').text

    def get_points(self) -> int:
        return int(self.browser.find_element(By.ID, "points").text)
