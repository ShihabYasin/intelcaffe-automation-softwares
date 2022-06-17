import datetime
import os
import shutil
import time
import random
import pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from linkedin_automation_utility import Driver


def get_a_random_file(dir):
    return random.choice (os.listdir (dir))


class LeetCode:
    """LeetCode code submission automation

    This will help submitting leet solns auto
    """
    driver = Driver.driver
    leetcode_solution_dir: str = "./LeetCode_solutions"
    submission_problems_dir = "./problems"
    leetcode_problems_base_url = "https://leetcode.com/problems/"

    class SUBMISSION_LANG_AVAILABLE:
        Python3 = "Python3"
        Cpp = "Cpp"

    page_loading_wait_secs = 8
    HOURS_TO_DELAY = 6
    MINUTES_IN_AN_HOUR = 60
    SECONDS_IN_A_MINUTE = 60

    @classmethod
    def get_time_stamp(cls):
        return str (datetime.datetime.now ())

    @classmethod
    def leetcode_url_from_filename(cls, leet_soln_filename=""):
        try:
            return (cls.leetcode_problems_base_url + leet_soln_filename.split ('.')[1].strip ().replace (' ', '-')).lower ()
        except:
            return None

    @classmethod
    def search(cls, problem_url=""):
        cls.driver.get (url=problem_url)
        cls.driver.refresh ()
        time.sleep (cls.page_loading_wait_secs)

    @classmethod
    def get_problem_weight(cls):
        elems = Driver.driver.find_elements_by_xpath ("//div[@diff]")
        for elem in elems:
            return elem.get_attribute ("diff")

    @classmethod
    def select_submission_lang(cls, lang):
        dropdown = Driver.driver.find_elements_by_xpath ("//div[@class='ant-select-selection-selected-value']")
        dropdown[0].click ()
        time.sleep (3)
        if lang == cls.SUBMISSION_LANG_AVAILABLE.Python3:
            print ("In Python")
            lang_select = LeetCode.driver.find_elements_by_xpath ("//li[@data-cy='lang-select-Python3' and @role='option']")
            print (type (lang_select[0]))
            print (lang_select)
            lang_select[0].click ()
        elif lang == cls.SUBMISSION_LANG_AVAILABLE.Cpp:
            print ("In Cpp")
            lang_select = LeetCode.driver.find_elements_by_xpath ("//li[@data-cy='lang-select-C++']")
            lang_select[0].click ()
        time.sleep (3)

    @classmethod
    def insert_code(cls, code_string=""):
        code_filed = Driver.driver.find_elements_by_xpath ("//div[@class ='CodeMirror-lines']")
        code_filed[0].click ()
        actions = ActionChains (cls.driver)
        actions.key_down (Keys.CONTROL).perform ()
        actions.send_keys ("a").perform ()
        actions.send_keys ("x").perform ()
        actions.key_up (Keys.CONTROL).perform ()
        time.sleep (2)
        pyperclip.copy (code_string)
        actions.key_down (Keys.CONTROL).perform ()
        actions.send_keys ("v").perform ()
        time.sleep (2)

    @classmethod
    def get_code(cls, leet_soln_file, file_extension=".py"):
        code_str = ''
        for code_file in os.listdir (os.path.join (LeetCode.leetcode_solution_dir, leet_soln_file)):
            # print (code_file)
            if code_file.endswith (file_extension):
                with open (os.path.join (LeetCode.leetcode_solution_dir, leet_soln_file, code_file)) as f:
                    for line in f:
                        if line.strip ():
                            code_str += line
                    return code_str
        return code_str

    @classmethod
    def get_wrong_code(cls, code_string):
        code_lines = code_string.split ('\n')
        try:
            line_idx_to_del = random.randint (1, len (code_lines) - 1)
            # print ("DEL: ", line_idx_to_del, code_lines[line_idx_to_del])
            del code_lines[line_idx_to_del]
            return "\n".join (line for line in code_lines)
        except:
            return code_string

    @classmethod
    def submit(cls):
        buttons = cls.driver.find_elements_by_tag_name ('button')
        for button in buttons:
            if button.text == "Submit":
                cls.driver.execute_script ("arguments[0].click();", button)

    @classmethod
    def simulate_wrong_code_submission(cls, correct_code_string, try_times=5):
        for submission_cnt in range (random.randint (1, try_times)):
            wrong_code_string = cls.get_wrong_code (code_string=correct_code_string)
            cls.insert_code (code_string=wrong_code_string)
            time.sleep (random.randint (3, 8))
            cls.submit ()
            time.sleep (random.randint (3, 10))

    @classmethod
    def simulate_correct_code_submission(cls, correct_code_string):
        try:
            cls.insert_code (code_string=correct_code_string)
            time.sleep (2)
            cls.submit ()
            time.sleep (random.randint (1, 10))
        except:
            return False
        return True


if __name__ == '__main__':
    while True:
        if not os.listdir (LeetCode.leetcode_solution_dir):
            break
        leet_soln_file = get_a_random_file (dir=LeetCode.leetcode_solution_dir)
        try:
            LeetCode.HOURS_TO_DELAY = random.randint (6, 9)
            leetcode_url = LeetCode.leetcode_url_from_filename (leet_soln_filename=leet_soln_file)
            if leetcode_url is not None:
                LeetCode.search (problem_url=leetcode_url)
            else:
                raise Exception
            problem_weight = str (LeetCode.get_problem_weight ())
            LeetCode.select_submission_lang (lang=LeetCode.SUBMISSION_LANG_AVAILABLE.Python3)
            correct_code_string = LeetCode.get_code (leet_soln_file=leet_soln_file)
            if correct_code_string and problem_weight != "hard":
                LeetCode.simulate_wrong_code_submission (correct_code_string=correct_code_string, try_times=4)
                if LeetCode.simulate_correct_code_submission (correct_code_string=correct_code_string):
                    shutil.rmtree (os.path.join (LeetCode.leetcode_solution_dir, leet_soln_file))
                    print (f"{LeetCode.get_time_stamp ()}   DONE:  ==>  URL: {leetcode_url}, File: {leet_soln_file}", file=open ('log.txt', 'a'))
                else:
                    print (f"{LeetCode.get_time_stamp ()}   PROBLEM: ==>  URL: {leetcode_url}, File: {leet_soln_file}", file=open ('log.txt', 'a'))
                    shutil.move (os.path.join (LeetCode.leetcode_solution_dir, leet_soln_file), LeetCode.submission_problems_dir)
            elif problem_weight == "hard":
                print (f"{LeetCode.get_time_stamp ()}   {problem_weight.upper ()} ==>  URL: {leetcode_url}, File: {leet_soln_file}", file=open ('log.txt', 'a'))
                shutil.move (os.path.join (LeetCode.leetcode_solution_dir, leet_soln_file), LeetCode.submission_problems_dir)
                continue

            time.sleep (LeetCode.HOURS_TO_DELAY * LeetCode.MINUTES_IN_AN_HOUR * LeetCode.SECONDS_IN_A_MINUTE)
            # time.sleep (10)

        except:
            print (f"{LeetCode.get_time_stamp ()}   EXCEPTION URL: {LeetCode.driver.current_url}, File: {leet_soln_file}", file=open ('log.txt', 'a'))
            continue
