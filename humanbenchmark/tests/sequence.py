"""Class for memory game which involves remember the pattern in which squares on 3x3
grid blink and repeating the pattern after"""

from time import sleep

from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
)

from .test import Test


class Sequence(Test):
    max_level = 50

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Click start button
        self.browser.find_element_by_css_selector(self.button_selector).click()

        tiles = self.browser.find_elements_by_css_selector(self.tile_selector)

        # Level loop
        # Add max since it's unable to read all squares to click around level 118
        for level in range(1, self.max_level + 1):
            sequence = []

            sleep(0.5)  # Wait half a second for first square to light up

            while len(sequence) < level:
                active = None

                for i, tile in enumerate(tiles):
                    if "active" in tile.get_attribute("class"):
                        sequence.append(i)
                        active = tile
                        break

                while active and "active" in active.get_attribute("class"):
                    sleep(0.1)

            # Check for stop code before starting to write out pattern
            if self.stop_pressed:
                self.fail()
                break

            # Update console with newest sequence digit
            self.console.print(sequence[-1] + 1, end=", ")

            for i in sequence:
                sleep(0.1)
                tiles[i].click()

        return level

    def fail(self):
        tile = self.browser.find_element_by_css_selector(self.tile_selector)

        try:  # Click until element is no longer available to click
            while True:
                tile.click()
                sleep(0.1)
        except (ElementNotInteractableException, StaleElementReferenceException):
            pass
