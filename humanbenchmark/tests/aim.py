"""Class for aim test which involves clicking randomly appearing targets quickly"""

from time import sleep

from .test import Test


class Aim(Test):
    # Super jank selector but it works, required due to weird overlapping of divs within
    # target element
    target_selector = "div[style='width: 100px; height: 2px;'].css-17nnhwz.e6yfngs4"
    rounds = 31

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to return to test select...")

        # Level loop
        for i in range(self.rounds):
            sleep(0.01)
            self.browser.find_element_by_css_selector(self.target_selector).click()

            if self.stop_pressed:
                return False

        return True
