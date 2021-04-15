"""Class for visual memory game which involves quickly memorizing shaded squares and
clicking all of them once they disappear"""

from time import sleep

from .test import Test


class Chimp(Test):
    number_tile_selector = ".css-19b5rdt"
    start_level = 4
    max_level = 40

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Click start button
        self.browser.find_element_by_css_selector(self.button_selector).click()
        # Level loop
        # Add max since it's unable to read all squares to click around level 118
        for level in range(self.start_level, self.max_level + 1):
            self.console.print(f"Level: {level}")
            sleep(0.5)
            numbers = {}
            elements = self.browser.find_elements_by_css_selector(
                self.number_tile_selector
            )

            for element in elements:
                numbers[int(element.text)] = element

            for i in range(1, len(elements) + 1):
                numbers[i].click()
            sleep(0.1)

            if level < self.max_level:
                self.browser.find_element_by_css_selector(self.button_selector).click()

            if self.stop_pressed:
                self.fail()
                break

        return level

    def fail(self):
        for strike in range(3):
            elements = self.browser.find_elements_by_css_selector(
                self.number_tile_selector
            )

            for element in elements:
                if element.text != "1":
                    element.click()
                    break
            sleep(0.1)

            if strike < 2:
                self.browser.find_element_by_css_selector(self.button_selector).click()
