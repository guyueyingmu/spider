import time

from selenium.webdriver import ActionChains

import auth
from element import BasePageElement
from locators import *
from page.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    # The locator for search box where search string is entered
    locator = 'q'


class MainPage(BasePage):
    """Home page action methods come here. i.e. taobao.com"""
    search_text_element = SearchTextElement()

    def __init__(self, browser='chrome'):
        super().__init__(browser)

    def click_search_button(self):
        """Triggers the search"""
        elem = self.waitUntilFindElement(MainPageLocators.SEARCH_BUTTON)
        self.click(elem)

    def goto_login_page(self):
        elem = self.waitUntilFindElement(MainPageLocators.LOGIN)
        self.click(elem)

    def open_checkin_page(self):
        elem = self.waitUntilFindElement(MainPageLocators.CHECK_IN)
        self.click(elem)

    def get_nick_name(self):
        elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
        return elem.text

    def verify_login(self):
        try:
            elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
            print(elem.text)
        except Exception:
            print("Authentication Failure")


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""
    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found" not in self.driver.page_source


class LoginPage(BasePage):

    def use_password_login(self):
        elem = self.waitUntilFindElement(LoginPageLocators.PASSWORD_LOGIN)
        self.click(elem)

    def get_nick_name(self):
        elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
        return elem.text

    def authenticate(self):
        username = self.waitUntilFindElement(LoginPageLocators.USERNAME_INPUT)
        password = self.waitUntilFindElement(LoginPageLocators.PASSWORD_INPUT)
        confirm = self.waitUntilFindElement(LoginPageLocators.LOGIN_BUTTON)

        username.clear()
        self.type(username, auth.TAOBAO_USER)

        password.clear()
        self.type(password, auth.TAOBAO_PASS)

        time.sleep(2)
        if self.check_auth_block():
            self.click(confirm)

    def check_auth_block(self):
        flag = 0
        block = self.is_element_visible(LoginPageLocators.AUTH_BLOCK)
        if block:
            print("登陆出现滑动条")
            actions = ActionChains()
            # actions.click_and_hold(block)
            # actions.move_by_offset(298, 0)
            actions.drag_and_drop_by_offset(self.findElement(LoginPageLocators.AUTH_BLOCK), 298, 0)
            actions.perform()
            time.sleep(2)
            if '验证通过' in self.page_source():
                flag = 1
                return flag
            else:
                return flag
        else:
            print("登陆没有滑动条，直接登陆")
            flag = 1
            return flag


class CheckinPage(BasePage):

    def get_coin_balance(self):
        elem = self.waitUntilFindElement(CheckinPageLocators.COIN)
        print('Balance: ' + elem.text)
        return elem.text

    def check_in(self):
        print('成功签到')


class OverlapPage(BasePage):

    def close_block(self):
        self.refresh()
        close = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#ks-content-ks-component126 > div.coin-overlay-content > span'))
        )
        if close:
            print("签到出现滑动条")
            self.click(close)

    def check_block(self):
        flag = 0
        time.sleep(10)
        block = self.is_element_visible(OverlapPageLocators.BLOCK)
        if block:
            print("签到出现滑动条")
            actions = ActionChains()
            actions.click_and_hold(block)
            actions.move_by_offset(298, 0)
            # actions.drag_and_drop_by_offset(block, 280, 0)
            actions.perform()
            time.sleep(2)
            if '验证通过' in self.page_source():
                flag = 1
                return flag
            else:
                return flag
        else:
            print("签到没有滑动条，直接签到")
            flag = 1
            return flag
