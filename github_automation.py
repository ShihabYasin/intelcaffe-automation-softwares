from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import StaleElementReferenceException
from linkedin_automation_utility import Search, FollowGroups, Follow, ConnectFollowPeople, Driver

###################################################################################

driver = Driver.driver


class FollowStarGithub:
    pass


def click_next(driver=driver, page_loading_wait_secs=10):
    if len (driver.find_elements_by_xpath ("//a[@href and @class='next_page']")) > 0:
        driver.find_elements_by_xpath ("//a[@href and @class='next_page']")[0].click ()
        time.sleep (page_loading_wait_secs)
        return driver.current_url
    else:
        return None


def follow(user_Github_profile_url="", page_loading_wait_secs=10, github_profile_url_to_follow="", driver=driver, no_of_pages=1):
    profile_name = github_profile_url_to_follow.rsplit ('/', 1)[-1].replace ('/', '')
    print (f"Following profile : {profile_name}")
    driver.get (url=user_Github_profile_url)
    time.sleep (int (page_loading_wait_secs / 2))
    driver.get (url=github_profile_url_to_follow)
    time.sleep (int (page_loading_wait_secs / 2))

    # Follow user
    driver.find_element_by_xpath (f"//form[@action='/users/follow?target={profile_name}']").submit ()
    time.sleep (int (page_loading_wait_secs / 2))
    driver.refresh ()
    time.sleep (int (page_loading_wait_secs / 2))

    def visit_repo(repo_url, driver=driver):
        print (f"Visiting Repo: {repo_url}")
        driver.get (repo_url)
        time.sleep (page_loading_wait_secs)
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            # print (button.text)
            # Giving star to repo
            if button.text.startswith ("Star"):
                driver.execute_script ("arguments[0].click();", button)
                time.sleep (page_loading_wait_secs)
                break

    def visit_repo_page(url, page_loading_wait_secs=10):
        driver.get (url=url)
        time.sleep (int (page_loading_wait_secs / 2))
        print (f"Visiting new page: {url}")
        elems = driver.find_elements_by_xpath ("//a[@href and @itemprop='name codeRepository']")
        all_repo_links = []
        for elem in elems:
            if elem.get_attribute ("href"):
                all_repo_links.append (elem.get_attribute ("href"))
        all_repo_links = list (set (all_repo_links))
        for repo_url in all_repo_links:
            visit_repo (repo_url=repo_url)

    # Goto user repo
    driver.find_elements_by_xpath ("//a[@data-tab-item='repositories']")[0].click ()
    time.sleep (int (page_loading_wait_secs / 2))
    ls_all_repos_pages = []
    ls_all_repos_pages.append (driver.current_url)  # getting current repo page in list
    while len (driver.find_elements_by_xpath ("//a[@href and @class='next_page']")) > 0:
        driver.find_elements_by_xpath ("//a[@href and @class='next_page']")[0].click ()
        time.sleep (page_loading_wait_secs)
        ls_all_repos_pages.append (driver.current_url)

    for page_url in ls_all_repos_pages:
        visit_repo_page (url=page_url, page_loading_wait_secs=page_loading_wait_secs)

    driver.get (user_Github_profile_url)
    time.sleep (page_loading_wait_secs)


if __name__ == '__main__':
    my_profile = "https://github.com/MySpaceOfGithub"  # From tthis github account
    github_profile_urls_to_follow = ["https://github.com/ShihabYasin"] # Give Github accounts , to follow + give star its repo
    for github_profile_url_to_follow in github_profile_urls_to_follow:
        follow (user_Github_profile_url=my_profile, no_of_pages=3, page_loading_wait_secs=10, github_profile_url_to_follow=github_profile_url_to_follow)
