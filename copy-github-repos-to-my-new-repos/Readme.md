# How to Upload lots of Github repo auto to my repo.
0. Create and activate vir env.
```shell
python3 -m venv v3
pip install -r requirements.txt
```
1. Generate Your very very secret Github access token: https://catalyst.zoho.com/help/tutorials/githubbot/generate-access-token.html
DON'T LOOSE IT, DON'T SHARE WITH OTHER PEOPLE.
2. Change access_token = '************************************' accordingly in ```github_run.py```.
3. In input.txt give other's_github_url , my_repo_new_url, commmit msg
4. Demo command: ```python3 run.py```

ROUGH: YOU DO NOT NEED TO READ HERE:** 
1. https://lavanya-gowda.medium.com/automate-github-repository-creation-and-initialization-using-python-e611009bd219
2. CMD
```shell
python3 github_run.py --repo https://github.com/Tenrys/memory --newrepo https://github.com/ShihabYasin/test --message 'Updating new repo codebase.'
```
