"""Base test playing class"""

from abc import ABC, abstractclassmethod
from threading import Thread
import keyboard

from rich.console import Console
from selenium import webdriver


class Test(ABC):
    def __init__(self, browser: webdriver.Chrome, console: Console):
        self.browser = browser
        self.console = console

        self.stop_pressed = False

    def wait_for_stop_key(self, key="space"):
        keyboard.wait(key)
        self.stop_pressed = True

    def detect_stop_thread(self, key="space"):
        thread = Thread(target=self.wait_for_stop_key, args=(key,))
        thread.start()

    def start(self):
        self.run()

        save = (
            self.console.input(
                "Would you like to save your score? "
                "[bright_black]([u]Y[/u]/n)[/bright_black] "
            )
            .strip()
            .lower()
        )

        if save and save[0] == "n":
            return False

        self.browser.find_element_by_css_selector(".css-qm6rs9.e19owgy710").click()
        return True

    @abstractclassmethod
    def run(self):
        pass
