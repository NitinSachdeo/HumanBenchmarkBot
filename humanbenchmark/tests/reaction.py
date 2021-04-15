"""Class for reaction time test which involves clicking an area once it turns from red
to green"""

from time import sleep

from .test import Test


class Reaction(Test):
    area_selector = ".e18o0sx0.css-saet2v.e19owgy77"

    def run(self):
        self.detect_stop_thread()
        self.console.print("Press spacebar at anytime to fail at next level...")

        # Select reaction area and click to start test
        area = self.browser.find_element_by_css_selector(self.area_selector)
        area.click()

        # Level loop
        times = []
        for i in range(5):
            while "view-waiting" in area.get_attribute("class"):
                sleep(0.001)

            area.click()

            sleep(0.5)
            time_div = self.browser.find_elements_by_css_selector(
                f"{self.result_selector} > div"
            )

            if time_div:
                times.append(int(time_div[0].text[:-3]))

            area.click()

            if self.stop_pressed:
                return False

        sleep(0.5)
        overall = self.browser.find_element_by_css_selector(
            f"{self.result_selector}"
        ).text[:-2]

        times.append((5 * int(overall)) - sum(times))
        print(times)
        return times
