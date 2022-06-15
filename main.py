import os
import time

from linkedin_automation_utility import Search, FollowGroups, Follow, ConnectFollowPeople

###################################################################################

def get_linkedin_search_terms_from_file(file_path="linkedin_search_terms.txt"):
    res = []
    with open(file_path) as search_terms_file:
        for _search_term in search_terms_file:
            if '#' not in _search_term:
                res.append(_search_term.strip())
    return res


def get_linkedin_profile_from_file(file_path="linkedin_profile.txt"):
    res = []
    with open(file_path) as linkedin_profile_file:
        res = linkedin_profile_file.readlines()
    return res[0]


def get_linkedin_activities_from_file(file_path="linkedin_ac"):
    res = []
    with open(file_path) as search_terms_file:
        for _search_term in search_terms_file:
            if '#' not in _search_term:
                res.append(_search_term.strip())
    return res


if __name__ == '__main__':
    # Give different search terms here to grow network
    search_term_ls = get_linkedin_search_terms_from_file(file_path="linkedin_search_terms.txt")
    # Give LN account , first time log in with user pass manually
    linkedin_profile_url = get_linkedin_profile_from_file(file_path='linkedin_profile.txt')
    linkedin_activities = get_linkedin_activities_from_file(file_path='linkedin_activities.txt')

    print(search_term_ls)
    print(linkedin_profile_url)
    print(linkedin_activities)
    # exit(0)

    for search_term in search_term_ls:
        # Follow Groups
        if "Follow Groups" in linkedin_activities:
            Search.search(LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term,
                          filter_term="Groups")
            FollowGroups.run(no_of_pages=3, page_loading_wait_secs=10)
            time.sleep(5)
        # Connect with people
        if "Connect with people" in linkedin_activities:
            print("Connect with people")

            Search.search(LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term,
                          filter_term="People")
            ConnectFollowPeople.run(no_of_pages=3, page_loading_wait_secs=10)
            time.sleep(5)
        # Connect with Schools
        if "Connect with Schools" in linkedin_activities:
            print("Connect with Schools")

            Search.search(LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term,
                          filter_term="Schools")
            Follow.run(no_of_pages=3, page_loading_wait_secs=10)
            time.sleep(5)
        # Follow Companies
        if "Follow Companies" in linkedin_activities:
            print("Follow Companies")

            Search.search(LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term,
                          filter_term="Companies")
            Follow.run(no_of_pages=3, page_loading_wait_secs=10)
