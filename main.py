import time

from linkedin_automation_utility import Search, FollowGroups, Follow, ConnectFollowPeople

###################################################################################


if __name__ == '__main__':

    # Give different search terms here to grow network
    search_term_ls = ["Python", "Java", "Software development", "PhP","NLP","Natural Language Processing", "Machine Learning",
                      "Laravel","SDLC", "Test driven development", "Data science", "Data engineering", "Software testing",
                      "DevOps", "Network security", "Database", "MongoDB", "MySQL", "Redis", "Elasticsearch", "AWS",
                      "Django", "Javascript", "Wordpress","Git", "Github", "Docker","Postgres", "PyTorch", "Web development",
                      "microservices"]
    # Give LN account , first time log in with user pass manually
    linkedin_profile_url = "https://www.linkedin.com/in/tomal-ahmed-57b302241/"

    for search_term in search_term_ls:
        # Follow Groups
        Search.search (LN_profile_url= linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term, filter_term="Groups")
        FollowGroups.run (no_of_pages=3, page_loading_wait_secs=10)
        time.sleep(5)
        # Connect with people
        Search.search (LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term, filter_term="People")
        ConnectFollowPeople.run (no_of_pages=3, page_loading_wait_secs=10)
        time.sleep (5)
        # Connect with Schools
        Search.search (LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term, filter_term="Schools")
        Follow.run (no_of_pages=3, page_loading_wait_secs=10)
        time.sleep (5)
        # Follow Companies
        Search.search (LN_profile_url=linkedin_profile_url, page_loading_wait_secs=10, search_term=search_term, filter_term="Companies")
        Follow.run (no_of_pages=3, page_loading_wait_secs=10)

