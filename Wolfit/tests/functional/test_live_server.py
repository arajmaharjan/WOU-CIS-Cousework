import time

import pytest

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class TestLiveServer(object):
    @pytest.fixture(autouse=True)
    def execute(self, client):
        client.begin()
        yield
        client.end()

    def wait_for_element(self, client, element_id, text):
        start_time = time.time()
        while True:
            try:
                element = client.browser.find_element_by_id(element_id).text
                assert text in element
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.25)
