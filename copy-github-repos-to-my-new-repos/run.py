import os

with open ('input.txt', 'r') as f:
    for line in f:
        line = line.strip ()
        # old_repo_url, new_repo_url, commit_msg = line.split (' ')
        ls = line.split (':::')
        old_repo_url, new_repo_url, commit_msg = ls[0], ls[1], ls[2]
        commit_msg = commit_msg.replace(' ','_')

        # print(old_repo_url, new_repo_url, commit_msg)
        print(f'RUNNING COMMAND:\npython3 github_run.py --repo {old_repo_url} --newrepo {new_repo_url} --message "{commit_msg}"')
        os.system(f'python3 github_run.py --repo {old_repo_url} --newrepo {new_repo_url} --message "{commit_msg}"')
