"""Class for visual memory game which involves quickly memorizing shaded squares and
clicking all of them once they disappear"""

from time import sleep

from .test import Test


class Memory(Test):
    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Click start button
        self.browser.find_element_by_css_selector(".css-de05nr.e19owgy710").click()

        # Level loop
        # Add max since it's unable to read all squares to click around level 118
        for level in range(1, 101):
            sleep(0.5)  # Wait half a second for squares to light up
            squares = self.browser.find_elements_by_css_selector("div.square-row div")

            indicator = None
            for i, square in enumerate(squares):
                if "active" not in square.get_attribute("class"):
                    squares[i] = None
                elif indicator is None:
                    indicator = square

            while "active" in indicator.get_attribute("class"):
                sleep(0.1)
            sleep(0.5)  # Extra wait to prevent element not interactable error

            for square in filter(None, squares):
                square.click()

            level += 1
            level_div = self.browser.find_element_by_xpath(
                "//div[starts-with(string(), 'Level:') and @class='score']"
            )
            # Wait till level counter increments
            while int(level_div.text.split(" ")[-1]) != level:
                sleep(0.1)

            if self.stop_pressed:
                break

        self.console.print("[red]Ending game![/red]")
        self.fail()

        return level

    def fail(self):
        lives = 3

        while True:
            sleep(0.5)  # Then another half a second for squares to light up

            squares = self.browser.find_elements_by_css_selector("div.square-row div")
            indicator = None
            for i, square in enumerate(squares):
                if "active" in square.get_attribute("class"):
                    if indicator is None:
                        indicator = square

                    squares[i] = None

            while "active" in indicator.get_attribute("class"):
                sleep(0.1)
            sleep(0.5)  # Extra wait to prevent element not interactable error

            for square in list(filter(None, squares))[:3]:
                square.click()

            lives -= 1
            if lives == 0:
                return

            lives_div = self.browser.find_element_by_xpath(
                "//div[starts-with(string(), 'Lives:') and @class='score']"
            )
            # Wait till lives decrement
            while int(lives_div.text.split(" ")[-1]) != lives:
                sleep(0.1)
