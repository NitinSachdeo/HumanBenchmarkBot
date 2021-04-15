"""Class for verbal memory test which involves seeing a series of words and being able
to recall whether that word had come up before or not"""

from time import sleep

from .test import Test


class Verbal(Test):
    word_selector = ".word"
    text_button_selector = (
        "//button[starts-with(string(), '{0}') and contains(@class, 'e19owgy710')]"
    )
    max_level = 500
    strikes = 3

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Click start button
        sleep(0.5)  # For some reason this page requires some time before clicking start
        self.browser.find_element_by_css_selector(self.button_selector).click()

        # Level loop
        # Add max since it's unable to read all squares to click around level 118
        words = set()
        rounds = 0
        while True:
            sleep(0.1)
            word = self.browser.find_element_by_css_selector(self.word_selector).text

            # XOR used to invert output if stop code sent
            if (word in words) ^ (self.stop_pressed):
                self.browser.find_element_by_xpath(
                    self.text_button_selector.format("SEEN")
                ).click()
            else:
                words.add(word)
                self.browser.find_element_by_xpath(
                    self.text_button_selector.format("NEW")
                ).click()

            if self.stop_pressed:
                self.strikes -= 1
                if self.strikes == 0:
                    break
            else:
                rounds += 1

            if rounds == self.max_level:
                self.stop_pressed = True

        return rounds
