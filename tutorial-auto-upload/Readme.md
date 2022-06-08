### How to generate md files from web links:

2. Give input urls in input.txt
3. python3 run.py
4. Check ```out/``` folder for new md files
5. Edit md files to tune post
6. set these vars in ```get_multiple_post.py``` file 
```python
original_md_file_path_to_copy = 'out/application-logging-using-fluentd-elasticsearch-kibana-53540dcd768d.md'
title = "Application Logging with Fluentd Elasticsearch and Kibana"
last_post_date = '2019-03-10'
# original_category_ls = ['Docker', 'Elasticsearch','Python', 'Kibana']
category_ls = ['Docker', 'Elasticsearch', 'Kibana']
out_md_files_dir = 'out_md_files/'
```
6. run ```python3 get_multiple_post.py```
7. Check ```out_md_files``` for new posts , now post in github , cheers !!!


### To Upload on github website repo:
1. Give md files in ```md_files_to_upload_in_github_web``` run ```upload.py```.


## (Extra)
### Local site testing for md files ( if need to debug)
1. Check ```offline_jekyll_site_testing/Makefile``` to run.
2. Give md post file in ```offline_jekyll_site_testing/_posts/``` folder and edit live.