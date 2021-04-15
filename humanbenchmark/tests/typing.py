"""Class for typing test which involves typing out a given passage"""

from .test import Test


class Typing(Test):
    def run(self):
        self.detect_stop_thread()

        # Click start button
        passage_div = self.browser.find_element_by_css_selector(".letters.notranslate")

        passage = passage_div.text
        passage_div.send_keys(passage)

        wpm = self.browser.find_element_by_css_selector(".css-1qvtbrk.e19owgy78").text
        print(wpm)
        return int(wpm[-3:])
