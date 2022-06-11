import time
from linkedin_automation_utility import Driver
from selenium.common.exceptions import StaleElementReferenceException
###################################################################################

class ApplyJobs:
    """
    Usage: Use it for following Groups
    ex: in main():
    Search.search (LN_profile_url="https://www.linkedin.com/in/tomal-ahmed-57b302241/", page_loading_wait_secs=10, search_term="java", filter_term="Groups")
    FollowGroups.run (no_of_pages=3, page_loading_wait_secs=10)
    """
    driver = Driver.driver

    @classmethod
    def get_job_links(cls, LN_job_profile_url, driver=driver):
        driver.get (url=LN_job_profile_url)
        driver.refresh ()
        time.sleep (page_loading_wait_secs)

        elems = Driver.driver.find_elements_by_xpath ("//a[@href and @tabindex and @class='disabled ember-view job-card-container__link job-card-list__title']")
        all_grp_links = []
        for elem in elems:
            all_grp_links.append (elem.get_attribute ("href"))
        all_grp_links = list (set (all_grp_links))
        return all_grp_links

    @classmethod
    def easy_apply(cls, driver=driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            try:
                if button.text == "Easy Apply":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
            except StaleElementReferenceException as e:
                pass

    @classmethod
    def check_form_if_blank(cls, driver=driver, page_loading_wait_secs=10):
        forms = driver.find_elements_by_tag_name ('p')
        for form in forms:
            try:
                if form.text == "Please enter a valid answer":
                    return True
            except StaleElementReferenceException as e:
                pass
        return False

    @classmethod
    def check_if_already_applied_for_job(cls, driver=driver, page_loading_wait_secs=10):
        forms = driver.find_elements_by_tag_name ('span')
        for form in forms:
            try:
                if form.text == "Application submitted":
                    return True
            except StaleElementReferenceException as e:
                pass
        return False


    @classmethod
    def click_popup_next(cls, driver=driver, page_loading_wait_secs=10):
        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            # print(button.text)
            try:
                if button.text == "Submit application":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
                    return "Submit application"
                if button.text == "Next":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
                    return "Next"
                if button.text == "Review":
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
                    return "Review"

            except StaleElementReferenceException as e:
                pass
        return False

    @classmethod
    def click_next_job_page(cls, driver=driver, page_loading_wait_secs=10, page_no=2):

        buttons = driver.find_elements_by_tag_name ('button')
        for button in buttons:
            try:
                if button.text== str(page_no):
                    driver.execute_script ("arguments[0].click();", button)
                    time.sleep (page_loading_wait_secs)
            except StaleElementReferenceException as e:
                pass

if __name__ == '__main__':
    page_loading_wait_secs = 10
    job_apply_base_url = "https://www.linkedin.com/jobs/search/?distance=25.0&f_AL=true&f_EA=true&f_JT=F%2CP%2CC&f_TPR=r604800&f_WT=2&geoId=92000000&keywords={}&sortBy=R"

    # Give different search terms here to grow network
    # search_term_ls = ["Software tester", "Python", "Java", "Software development", "PhP","NLP","Natural Language Processing", "Machine Learning",
    #                   "Laravel","SDLC", "Test driven development", "Data science", "Data engineering", "Software testing",
    #                   "DevOps", "Network security", "Database", "MongoDB", "MySQL", "Redis", "Elasticsearch", "AWS",
    #                   "Django", "Javascript", "Wordpress","Git", "Github", "Docker","Postgres", "PyTorch", "Web development",
    #                   "microservices", "Agile development"]

    search_term_ls = ["Laravel developer", "PhP developer", "Wordpress developer"]


    for search_term in search_term_ls:
        ls_jobs_links = ApplyJobs.get_job_links(LN_job_profile_url=job_apply_base_url.format(search_term.replace(" ", "%20")))
        ApplyJobs.click_next_job_page (page_no=2, page_loading_wait_secs=6)
        ls_jobs_links += ApplyJobs.get_job_links (LN_job_profile_url=Driver.driver.current_url)
        ApplyJobs.click_next_job_page (page_no=3, page_loading_wait_secs=6)
        ls_jobs_links += ApplyJobs.get_job_links (LN_job_profile_url=Driver.driver.current_url)

        # print(ls_jobs_links)
        # break

        # print(f"Total: {len(ls_jobs_links)}")
        for idx, job_link in enumerate(ls_jobs_links):
            ApplyJobs.driver.get (url=job_link)
            ApplyJobs.driver.refresh ()
            time.sleep (4)
            ApplyJobs.easy_apply (page_loading_wait_secs=6)
            ret = ApplyJobs.click_popup_next (page_loading_wait_secs=6)
            if ret == "Review":
                if ApplyJobs.check_form_if_blank(page_loading_wait_secs=6):
                    break
            apply_status = "      XXX   NOT APPLIED"
            if ret == "Submit application":
                apply_status  = "APPLIED"
            False_count = 0
            while(ret != "Submit application" ):

                ret = ApplyJobs.click_popup_next (page_loading_wait_secs=6)
                print(ret)
                if ret == "Review" and ApplyJobs.check_form_if_blank(page_loading_wait_secs=6):
                    break
                if ret == "Next" and ApplyJobs.check_form_if_blank(page_loading_wait_secs=6):
                    break
                if ApplyJobs.check_if_already_applied_for_job(page_loading_wait_secs=6):
                    break
                if ret == False:
                    break
                    # False_count += 1
                    # if False_count > 3:
                    #     print("BACKUP CALLING")
                    #     False_count = 0
                    #     ApplyJobs.driver.get (url=job_link)
                    #     ApplyJobs.driver.refresh ()
                    #     time.sleep (4)
                    #     ApplyJobs.easy_apply (page_loading_wait_secs=6)
                    #     ret = ApplyJobs.click_popup_next (page_loading_wait_secs=6)


            if ret == "Submit application":
                apply_status  = "APPLIED"
            print(f"{idx}: {apply_status}, Link: {job_link}")

        # break






