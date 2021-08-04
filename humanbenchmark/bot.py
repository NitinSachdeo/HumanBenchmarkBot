#!/usr/bin/env python
"""Entrypoint file for bot interface"""

from collections import OrderedDict
from dataclasses import dataclass, field
from time import sleep

from rich.console import Console
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from tests import Aim, Chimp, Memory, Number, Reaction, Sequence, Typing, Verbal
from tests.test import Test


# Constants
@dataclass  # We use a dataclass instead of dict simply so we can access values
class Endpoints:  # as attributes instead of keys, I think it looks better :)
    login: str = "login"
    dashboard: str = "dashboard"
    test: str = "tests"
    test_list: OrderedDict[str, Test] = field(
        default_factory=lambda: OrderedDict(
            (
                ("aim", Aim),
                ("chimp", Chimp),
                ("memory", Memory),
                ("number-memory", Number),
                ("reactiontime", Reaction),
                ("sequence", Sequence),
                ("typing", Typing),
                ("verbal-memory", Verbal),
            )
        )
    )


URL = "https://humanbenchmark.com"
ENDPOINTS = Endpoints()


class Bot:
    def __init__(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.console = Console()

        self.browser.get(URL)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.browser.quit()

    def start(self):
        login = (
            self.console.input(
                "Would you like to login to an account? "
                "[bright_black](y/[u]N[/u])[/bright_black] "
            )
            .strip()
            .lower()
        )

        if login and login[0] == "y":
            self.console.print("Redirecting to login page...")
            self.login()
        else:
            self.console.print("Continuing with anonymous session")

        while True:
            if self.browser.current_url != f"{URL}/{ENDPOINTS.dashboard}":
                self.browser.get(f"{URL}/{ENDPOINTS.dashboard}")
            self.test_select()

    def login(self):
        self.browser.get(f"{URL}/{ENDPOINTS.login}")

        username_field = self.browser.find_element_by_name("username")
        password_field = self.browser.find_element_by_name("password")

        while True:
            self.clear_field(username_field)
            self.clear_field(password_field)

            username = self.console.input("Username: ")
            username_field.send_keys(username)
            password = self.console.input("Password: ", password=True)
            password_field.send_keys(password)

            # Find submit button and click
            self.browser.find_element_by_xpath(
                "//input[@type='submit' and @value='Login']"
            ).click()

            sleep(1)
            error = self.browser.find_elements_by_css_selector(".login-error-message")

            if not error:
                self.console.print(
                    "[green]Succesfully logged in as "
                    f"[b white]{username}[/b white]![/green]"
                )
                return True

            self.console.print("[red]Failed to login![red]")
            retry = (
                self.console.input(
                    "Continue without logging in? "
                    "[bright_black]([u]Y[/u]/n)[/bright_black] "
                )
                .strip()
                .lower()
            )

        if retry and retry[0] != "n":
            return False

        self.console.print("Try logging in again...")

    def test_select(self):
        self.console.print("[u]Available Tests[/u]")
        for i, test in enumerate(ENDPOINTS.test_list.keys(), 1):
            self.console.print(f"\t[b]{i}.[/b] {test.title()}")

        selected_test = (
            self.console.input(
                "Select a test to take: "
                f"[bright_black](1-{len(ENDPOINTS.test_list)})[/bright_black] "
            )
            .strip()
            .lower()
        )

        if selected_test.isdigit():
            selected_index = int(selected_test)
            if selected_index not in range(1, len(ENDPOINTS.test_list) + 1):
                self.console.print("[red]Invalid number[/red]")
                return False

            selected_test = list(ENDPOINTS.test_list.keys())[selected_index - 1]
        elif selected_test not in ENDPOINTS.test_list.keys():
            self.console.print(f"[red]No test named {selected_test} available[/red]")
            return False

        self.browser.get(f"{URL}/{ENDPOINTS.test}/{selected_test}")

        # Spawn test handler in seperate thread and wait for esc to cancel or return
        test_instance = ENDPOINTS.test_list[selected_test](self.browser, self.console)
        test_instance.start()
        del test_instance

        return True

    @staticmethod
    def clear_field(field):
        """Replacement method since field.clear() doesn't work sometimes

        Args:
            field: an element returned by selenium
        """
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)


if __name__ == "__main__":
    with Bot() as bot:
        bot.start()
