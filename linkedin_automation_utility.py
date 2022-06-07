###################################################################################
import os
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import os
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
###################################################################################
class Driver:
    chrome_options = Options ()
    chrome_options.add_experimental_option ("debuggerAddress", "127.0.0.1:9222")
    chrome_options.add_argument ("--disable-gpu")
    chrome_options.add_argument ("--disable-software-rasterizer")
    chrome_driver = r"./chromedriver"  # Change chrome driver path accordingly
    driver = webdriver.Chrome (chrome_driver, chrome_options=chrome_options)

    @classmethod
    def close_driver(cls, driver):
        try:
            driver.close ()
        except Exception as e:
            print (1, e)
        try:
            driver.quit ()
        except Exception as e:
            print (2, e)
###################################################################################
class FollowGroups:
    """
    Usage: Use it for following Groups
    ex: in main():
    Search.search (LN_profile_url="https://www.linkedin.com/in/tomal-ahmed-57b302241/", page_loading_wait_secs=10, search_term="java", filter_term="Groups")
    FollowGroups.run (no_of_pages=3, page_loading_wait_secs=10)
    """
    driver = Driver.driver

    @classmethod
    def click_next(cls, driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            try:
                if button.text == "Next":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
            except StaleElementReferenceException as e:
                pass
    @classmethod
    def follow_gropus(cls, driver = driver, page_loading_wait_secs=10):
        original_url_of_groups = driver.current_url
        time.sleep (page_loading_wait_secs)
        elems = Driver.driver.find_elements_by_xpath ("//a[@href]")
        all_grp_links = []
        for elem in elems:
            if "/groups/" in elem.get_attribute ("href"):
                all_grp_links.append (elem.get_attribute ("href"))
        all_grp_links = list (set (all_grp_links))

        def visit_grp(tab_url, driver=driver):
            print (f"Visiting Group: {tab_url}")
            driver.get (tab_url)
            time.sleep (page_loading_wait_secs)
            buttons = driver.find_elements_by_tag_name ('button')
            for button in buttons:
                if button.text == "Join":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
                    break
            time.sleep (int (page_loading_wait_secs / 2))

        for grp_link in all_grp_links:
            visit_grp (tab_url=grp_link)


        driver.get (original_url_of_groups)
        driver.refresh ()
        time.sleep (page_loading_wait_secs)

    @classmethod
    def run(cls, driver = driver, page_loading_wait_secs=10, no_of_pages =3):
        for page in range (no_of_pages):
            FollowGroups.follow_gropus(driver=driver, page_loading_wait_secs=page_loading_wait_secs)
            FollowGroups.click_next (driver=driver, page_loading_wait_secs=page_loading_wait_secs)

class Follow:
    """
    Usage: Use it for Schools, Companies
    ex: in main():

    Search.search (LN_profile_url="https://www.linkedin.com/in/tomal-ahmed-57b302241/", page_loading_wait_secs=10,  search_term="java", filter_term = "Schools")
    Follow.run (no_of_pages=3, page_loading_wait_secs=10)

    1. run:  google-chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile" --disable-gpu --disable-software-rasterizer
    2. Log in to LN and goto search (php etc.), filter companies using search_term = "Companies"
    3. run in main: FollowCompanies.run(no_of_pages=4, page_loading_wait_secs=10)

    """
    driver = Driver.driver
    @classmethod
    def click_next(cls, driver = driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            try:
                if button.text == "Next":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
            except StaleElementReferenceException as e:
                pass

    @classmethod
    def follow_companies(cls, driver = driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            driver.implicitly_wait (int (page_loading_wait_secs / 2))
            if button.text == "Follow":
                driver.execute_script ("arguments[0].click();", button)
        time.sleep (page_loading_wait_secs)

    @classmethod
    def run(cls, driver = driver, page_loading_wait_secs=10, no_of_pages =3):
        for page in range (no_of_pages):
            Follow.follow_companies (driver=driver, page_loading_wait_secs=page_loading_wait_secs)
            Follow.click_next (driver = driver, page_loading_wait_secs=page_loading_wait_secs)


class Search:
    """
    Usage: Search a LN profile, search with a key term , go to filter result using filter term
    1.     Search.search( LN_profile_url="https://www.linkedin.com/in/tomal-ahmed-57b302241/", page_loading_wait_secs=10, search_term="django")
    """
    driver = Driver.driver

    @classmethod
    def search(cls, LN_profile_url="", driver= driver, page_loading_wait_secs=10, search_term="PhP", filter_term = "Companies"):
        driver.get(url=LN_profile_url)
        driver.refresh ()
        time.sleep (page_loading_wait_secs)
        inputs = driver.find_elements_by_tag_name ('input')
        inputs[0].clear ()
        inputs[0].send_keys (search_term)
        inputs[0].send_keys (Keys.ENTER)
        time.sleep (page_loading_wait_secs)

        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            if button.text == filter_term:
                driver.execute_script ("arguments[0].click();", button)
                time.sleep (page_loading_wait_secs)
                break

        time.sleep (page_loading_wait_secs)


class ConnectFollowPeople:
    """
    Usage:
    in main():

    Search.search (LN_profile_url="https://www.linkedin.com/in/tomal-ahmed-57b302241/", page_loading_wait_secs=10,  search_term="java", filter_term = "People")
    ConnectFollowPeople.run ( no_of_pages=3, page_loading_wait_secs=10)

    """
    driver = Driver.driver

    @classmethod
    def click_next(cls, driver = driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            try:
                if button.text == "Next":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
            except StaleElementReferenceException as e:
                pass

    @classmethod
    def connect(cls, driver = driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            driver.implicitly_wait (int (page_loading_wait_secs / 2))
            if button.text == "Connect":
                driver.execute_script ("arguments[0].click();", button)
                time.sleep (int (page_loading_wait_secs / 3))
                driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]/span").click()
                time.sleep (int(page_loading_wait_secs/2))

        time.sleep (page_loading_wait_secs)

    @classmethod
    def run(driver=driver, page_loading_wait_secs=10, no_of_pages=3):
        for page in range (no_of_pages):
            ConnectFollowPeople.connect (page_loading_wait_secs=page_loading_wait_secs)
            ConnectFollowPeople.click_next (page_loading_wait_secs=page_loading_wait_secs)



if __name__ == '__main__':
    pass

