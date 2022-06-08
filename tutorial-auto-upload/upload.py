import glob
import os
import shutil
import time

import requests
from pathlib import Path

localgit_repo_dir = '/home/tigerit/MyGithub/shihabyasin.github.io'
md_files_to_upload_in_github_web = 'md_files_to_upload_in_github_web'
log_file = 'log.txt'
curr_dir = os.getcwd()

ls_md_files_to_upload = sorted(glob.glob(md_files_to_upload_in_github_web+ '/*.md'))


def git_push():
    os.chdir(localgit_repo_dir)
    print('Github push started  ... ') # , file=open(log_file, 'a'))
    os.system('./git_commit_auto_script.sh')
    print ('Github push completed ...') # , file=open(log_file, 'a'))
    os.chdir(curr_dir)


for md_file_path in ls_md_files_to_upload: # get all md files
    ## Copy to main repo
    shutil.copy(md_file_path, os.path.join(localgit_repo_dir, '_posts'))
    md_file_name = os.path.basename(md_file_path)

    ## Generate new url to check here
    with open(md_file_path,'r') as f:
        md_file_lines = f.readlines()[:7]
    category = (md_file_lines[4].replace('\n','').replace('category: ','')).strip().lower()
    date ='/'.join (((md_file_lines[3].replace('\n','')).split(' ')[1]).split('-'))
    html_file_name = (md_file_lines[2].replace('\n','').replace('title: ','') + ' category ' + category.title() + '.html').replace(' ','_')
    generated_url_to_check = 'https://shihabyasin.github.io/' + category + '/' + date + '/' + html_file_name
    print(f'Working on: {generated_url_to_check}')
    # continue

    ## Git push here
    git_push()

    ## Wait and see if website updated
    time.sleep(60*3)
    response = requests.get (generated_url_to_check)
    website_exists  =True
    if response.status_code == 200:
        print (f'Web site exists: {generated_url_to_check}') # , file=open(log_file, 'a'))
        shutil.move (md_file_path, 'md_files_to_upload_in_github_web/copied')
    else:
        website_exists = False
        print (f'Web site does not exist: {generated_url_to_check}') # , file=open(log_file, 'a'))

        file_path_in_local_repo = os.path.join (localgit_repo_dir, '_posts' , md_file_name)
        if os.path.isfile(file_path_in_local_repo):
            os.remove(file_path_in_local_repo)
            print(f"Deleting: {file_path_in_local_repo}") # , file=open(log_file, 'a'))

        else:
            print(f"File: {file_path_in_local_repo} not found.") # , file=open(log_file, 'a'))

        shutil.move (md_file_path, 'md_files_to_upload_in_github_web/problem')
        git_push()
        time.sleep(20)










