"""Base test playing class"""

from abc import ABC, abstractclassmethod
from threading import Thread
import keyboard

from rich.console import Console
from selenium import webdriver


class Test(ABC):
    tile_selector = "div.square"
    button_selector = ".css-de05nr.e19owgy710"
    save_button_selector = ".css-qm6rs9.e19owgy710"
    result_selector = ".css-1qvtbrk.e19owgy78"

    def __init__(self, browser: webdriver.Chrome, console: Console):
        self.browser = browser
        self.console = console

        self.stop_pressed = False

    def wait_for_stop_key(self, key="space"):
        keyboard.wait(key)
        self.stop_pressed = True
        self.console.print("[red]Ending game![/red]")

    def detect_stop_thread(self, key="space"):
        thread = Thread(target=self.wait_for_stop_key, args=(key,))
        thread.start()

    def start(self):
        if not self.run():
            return

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

        self.browser.find_element_by_css_selector(self.save_button_selector).click()
        return True

    @abstractclassmethod
    def run(self):
        pass
