"""Class for typing test which involves typing out a given passage"""

from time import sleep

from .test import Test


class Typing(Test):
    def run(self):
        self.detect_stop_thread()

        # Click start button
        passage_div = self.browser.find_element_by_css_selector(".letters.notranslate")

        passage = passage_div.text
        passage_div.send_keys(passage)

        sleep(0.5)  # Wait for result elements to load
        wpm = self.browser.find_element_by_css_selector(self.result_selector).text
        self.console.print(wpm)
        return int(wpm[:-3])
