"""Class for number memory test which involves quickly memorizing a string of numbers
and repeating it from memory after it disappears"""

from time import sleep

from .test import Test


class Number(Test):
    number_selector = ".big-number"
    input_selector = ".css-1qvtbrk.e19owgy78 > input"
    max_level = 50

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Click start button
        self.browser.find_element_by_css_selector(self.button_selector).click()

        # Level loop
        # Add max since it's unable to read all squares to click around level 118
        for level in range(1, self.max_level + 1):
            sleep(0.1)  # Wait a bit to ensure element is loaded
            number = self.browser.find_element_by_css_selector(
                self.number_selector
            ).text

            input_form = None
            while not input_form:
                input_form = self.browser.find_elements_by_css_selector(
                    self.input_selector
                )

            if self.stop_pressed:
                input_form[0].send_keys("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                self.browser.find_element_by_css_selector(self.button_selector).click()
                break

            input_form[0].send_keys(number)

            self.browser.find_element_by_css_selector(self.button_selector).click()
            sleep(1)
            self.browser.find_element_by_css_selector(self.button_selector).click()

        return level
