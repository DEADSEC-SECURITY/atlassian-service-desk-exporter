#  Copyright (c) 2023.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

# Built-In Imports
import time
import urllib.parse
from datetime import timedelta
from pathlib import Path
from typing import List

# 3rd-Party Imports
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumprint import SeleniumPDF
from webdrivermanager import ChromeDriverManager

# Local Imports
from utils.helpers import check_chromedriver_installed
from utils.types import Url


if not check_chromedriver_installed():
    ChromeDriverManager().download_and_install()


class AtlassianServiceDeskExporter(SeleniumPDF):
    """
    Exports tickets from the Atlassian ServiceDesk platform
    """

    _start_time: float

    _driver: Chrome

    _atlassian_domain: Url
    __email: str
    __password: str
    _export_folder_destination: Path

    def __init__(
            self,
            atlassian_domain: Url,
            email: str,
            password: str,
            export_folder_destination: Path = Path.cwd(),
            *args, **kwargs
    ):
        self._start_time = time.time()

        super().__init__(disable_headless=True, *args, **kwargs)

        self._atlassian_domain = atlassian_domain
        self.__email = email
        self.__password = password

        self._export_folder_destination = export_folder_destination
        self._export_folder_destination.mkdir(parents=True, exist_ok=True)

        self._driver = self.driver.driver

        self.cdriver.maximize_window()
        self._login()

    @property
    def cdriver(self) -> Chrome:
        return self._driver

    @property
    def export_folder_destination(self) -> Path:
        return self._export_folder_destination

    def _get_atlassian_login(self) -> Url:
        """
        Creates the login url for _login

        :return:
        """
        return urllib.parse.urljoin(self._atlassian_domain, 'servicedesk/customer/user/login')

    def _get_tickets_url(self, page: int = 1) -> Url:
        """
        Creates the tickets urls for _get_tickets

        :return:
        """
        full_url = urllib.parse.urljoin(self._atlassian_domain, 'servicedesk/customer/user/requests')
        query_params = urllib.parse.urlencode({'page': str(page), 'reporter': 'all', 'sNames': 'all'})
        return f"{full_url}?{query_params}"

    def _wait_for_url_to_change(self, url: Url, timeout: int = 30) -> bool:
        """
        Waits for the URL to change

        :param url: The url to change from
        :return: True if changed, False if not
        """
        try:
            WebDriverWait(self.cdriver, timeout).until_not(
                EC.url_contains(url)
            )
            return True
        except TimeoutException:
            return False

    def _get_xpath(self, xpath: str, timeout: int = 30, not_exists_ok: bool = False) -> WebElement | None:
        """
        Gets the XPATH given. Always waits for it to become available first

        :return: None when element not found
        """
        try:
            return WebDriverWait(self.cdriver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException as error:
            if not_exists_ok:
                return
            raise error

    def _login(self):
        """
        Logins to Atlassian

        :return:
        """
        self.cdriver.get(self._get_atlassian_login())
        self._get_xpath('//*[@id="user-email"]').send_keys(self.__email)
        self._get_xpath('//*[@id="login-button"]').click()
        self._get_xpath('//*[@id="user-password"]').send_keys(self.__password)

        current_url = self.cdriver.current_url

        self._get_xpath('//*[@id="login-form"]').submit()

        if not self._wait_for_url_to_change(current_url, timeout=5):
            return self._login()

    def _get_tickets(self) -> List[Url]:
        """
        Gets all tickets urls

        :return:
        """
        ticket_urls = []

        current_page = 1
        while True:
            self.cdriver.get(self._get_tickets_url(current_page))
            table = self._get_xpath(
                '/html/body/span[2]/div[2]/div/div/div[2]/main/div/section/div[4]/div/div/div[1]/table/tbody',
                not_exists_ok=True
            )
            if not table:
                break
            tickets = table.find_elements(By.TAG_NAME, "tr")
            for ticket in tickets:
                anchors = ticket.find_elements(By.TAG_NAME, "a")
                ticket_urls.append(anchors[0].get_attribute("href"))

            current_page += 1
        return ticket_urls

    def _expand_ticket_thread(self):
        """
        Each ticket if it has more than a certain amount of messages it will display a button to show more, this
        function will click that button until the full thread is displayed.

        :return:
        """
        while True:
            show_more = self._get_xpath(
                '//*[@id="root"]/div[2]/div/div/div[2]/main/div/div[2]/div[1]/div[2]/div[1]/button',
                timeout=2, not_exists_ok=True
            )
            if not show_more:
                break
            show_more.click()

    def _get_file_name(self, ticket: Url) -> str:
        """
        Generates the name for the pdf ticket exported

        :return:
        """
        return self.export_folder_destination.joinpath(f'{ticket.split("/")[-1]}.pdf').as_posix()

    def export(self):
        """
        Exports each ticket into a PDF

        :return:
        """
        tickets = self._get_tickets()
        for ticket in tickets:
            self.cdriver.get(ticket)
            self._expand_ticket_thread()
            self.convert_current_page_to_pdf(self._get_file_name(ticket))

        print('------- Export Stats -------')
        print(f'Exported {len(tickets)} tickets')
        print(f'Took {timedelta(self._start_time - time.time())}')
        print(f'Exported tickets saved in {self._export_folder_destination}')
        print('----------------------------')


if __name__ == '__main__':
    AtlassianServiceDeskExporter(
        atlassian_domain='YOUR_DOMAIN',
        email='YOUR_EMAIL',
        password='YOUR_PASSWORD',
        export_folder_destination=Path.cwd().joinpath('export')
    ).export()
