# Important: Do not make this repo public, for business secret.


# LinkedIN-automation:
1. To run different LN activity: 
 
```./run_activity.sh```

Input: ```linkedin_search_terms.txt, linkedin_profile.txt, linkedin_activities.txt``` 


2. To run different LN job apply: 
 
```./run_job_apply.sh``` 

Input: ```linkedin_job_search_terms.txt```


### Deprecated:
````
## LinkedIN-automation (OLD):
Some linkedin automation task. (Portfolio Building etc.)

Usage: 
0. Create, activate virtual env from ```requirements.txt```
1. Run chrome to debug  in terminal:
```shell
google-chrome --remote-debugging-port=9222 --user-data-dir="~/ChromeProfile" --disable-gpu --disable-software-rasterizer
```
2. Then run ```python3 main.py``` in another terminal with appropriate setting. Log in associated LinkedIN account(given in code).
```text
Check out comments in main.py for detail.
```
## **AUTO LN JOB APPLY:** (manually login to LN)
```python3 apply_jobs_LN.py```

````


## Github automation: 

1. Check ```github_automation.py```, read comments.

## Github repo auto upload: 
Check ```copy-github-repos-to-my-new-repos/Readme.md```

## Tutorial Upload:
(md file based) auto tutorial upload from internet links (dumping content, process , upload)
Check ```tutorial-auto-upload/Readme.md```


