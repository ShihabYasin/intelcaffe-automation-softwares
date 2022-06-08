import datetime

#################  Set some vars here to generate different posts
import os

original_md_file_path_to_copy = 'out/_sending-confirmation-emails-with-flask-rq-and-ses.md'
title = "Sending Confirmation Emails with Flask, Redis Queue, and Amazon SES"
last_post_date = '2019-04-12'
# original_category_ls = ['Research','NLP','Algorithm','ML','Terraform','Projects','Python', 'AWS','VISION-AI','Selenium','Django','Celery','Docker','Elasticsearch','Flask','Redis','Kibana','DataStructure','MY-TECH-STACK',
# 'Certificates','DevOps']
category_ls = ['Flask', 'Redis', 'AWS']
out_md_files_dir = 'out_md_files/'
#################

# os.system(f'rm -rf {out_md_files_dir}/*')

def get_next_date(last_post_date='2019-03-13', batch_size=5):
    year, month, day = last_post_date.split ('-')
    date = datetime.datetime (int (year), int (month), int (day))
    ls = []
    for i in range (batch_size):
        date += datetime.timedelta (days=1)
        ls.append (str (date).replace (' 00:00:00', ''))
    return ls


layout = "post"
date = ""
category = ""
tag = ""

batch_size = len (category_ls)
new_post_dates = get_next_date (last_post_date, batch_size=batch_size)

for idx, category in enumerate (category_ls):
    mew_md_file_name = new_post_dates[idx] + '-' + title.replace (' ', '_') + f'_category_{category_ls[idx]}.md'
    date = new_post_dates[idx] + " 16:20:23 +0900"
    category = category_ls[idx]
    tag = category

    base_tag = f"""---
layout: {layout}
title: {title}
date: {date}
category: {category}
tag: {tag}
---

"""
    # print(new_post_dates[idx], category)

    # print (base_tag)

    lines = [base_tag]
    with open (original_md_file_path_to_copy, 'r') as f:
        lines.append (f.readlines ())

    with open (out_md_files_dir + mew_md_file_name, 'w') as f:
        for line in lines:
            f.writelines (line)

    print ('Done: ', mew_md_file_name)
    date = ""
