#!/usr/bin/env python
"""Entrypoint file for bot interface"""

from collections import OrderedDict
from dataclasses import dataclass, field
from time import sleep

from rich.console import Console

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Constants
@dataclass  # We use a dataclass instead of dict simply so we can access values
class Endpoints:  # as attributes instead of keys, I think it looks better :)
    login: str = "login"
    dashboard: str = "dashboard"
    test: str = "tests"
URL = "https://humanbenchmark.com"
ENDPOINTS = Endpoints()


class Bot:
    def __init__(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.console = Console()

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
            .lower()[0]
        )

        if login == "y":
            self.console.print("Redirecting to login page...")
            self.login()
        else:
            self.console.print("Continuing with anonymous session")
            self.browser.get(f"{URL}/{ENDPOINTS.dashboard}")


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
            error = self.browser.find_elements_by_class_name("login-error-message")

            if not error:
                self.console.print(
                    "[green]Succesfully logged in as "
                    f"[b white]{username}[/b white]![/green]"
                )
                return True

            self.console.print("[red]Failed to login![red]")
            retry = self.console.input(
                "Continue without logging in? "
                "[bright_black]([u]Y[/u]/n)[/bright_black] "
            )

        if retry.strip().lower()[0] == "y":
            return False
        else:
            self.console.print("Try logging in again...")


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
