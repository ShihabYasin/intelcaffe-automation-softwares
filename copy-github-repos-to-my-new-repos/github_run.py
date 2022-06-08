import argparse
import os
import shutil
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from github import Github

path = os.getcwd()
access_token = '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'

def create__github_project(project_name):
    newpath = os.path.join(path, project_name)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    user = Github(access_token).get_user()
    repo = user.create_repo(name=project_name, private=False)
    print(f"Succesfully created repository {project_name}")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser (description='Auto Github commit on repo')
    arg_parser.add_argument ('-r', '--repo', help='Give github repo link.')
    arg_parser.add_argument ('-n', '--newrepo', help='Give new github repo link.')
    arg_parser.add_argument ('-m', '--message', help='Give commit message.')

    args = arg_parser.parse_args ()
    repo =  args.repo
    newrepo = args.newrepo
    message = args.message
    repo_dir = Path (repo).resolve ().stem
    newrepo_dir = Path (newrepo).resolve ().stem



    if os.path.exists(repo_dir):
        os.system(f'rm -rf {repo_dir}')
    if os.path.exists(newrepo_dir):
        os.system(f'rm -rf {newrepo_dir}')

    try:
        create__github_project(project_name=newrepo_dir)
        os.system (f'git clone {newrepo}')
    except:
        print(f'Repo {newrepo} already exists, delete it first: ')
        exit(0)


    os.system (f'git clone {repo}')


    os.system(f'cp git_commit_auto_script.sh {newrepo_dir}')

    if os.path.exists (f'{repo_dir}/.git'):
        os.system(f'rm -rf {repo_dir}/.git')
    if os.path.exists (f'{repo_dir}/.gitignore'):
        os.system (f'rm -rf {repo_dir}/.gitignore')


    os.system(f'cp -r {repo_dir}/* {newrepo_dir}')

    newrepo  = newrepo.replace('https://github.com/','')
    newrepo = newrepo.replace ('http://github.com/', '')

    os.chdir(newrepo_dir)
    os.system('git init')

    # exit(0)
    os.system (f"./git_commit_auto_script.sh {newrepo} {message}")

    exit(0)


