import os
import sys, argparse
import requests
from bs4 import BeautifulSoup, Tag
from pathlib import Path


def generate_md_file_from_html(url=None, source=None, last_file='out.md'):
    '''

    :param url: Online url link OR give html offline source
    :param source: Give source as offline html file OR online url
    :param last_file:
    :return:
    '''
    out_file_name = 'tmp_out.md'

    os.system (f'rm -rf {out_file_name}')
    os.system (f'rm -rf {last_file}')

    tmp_soup = ''
    if url is not None:
        r = requests.get (url)
        tmp_soup = r.text
        tmp_soup = BeautifulSoup (tmp_soup, 'html.parser')
    elif source is not None:
        with open (source) as fp:
            tmp_soup = BeautifulSoup (fp, 'html.parser')
    else:
        raise 'Error getting source html'

    if tmp_soup == '':
        raise 'Error getting source html'

    def walker(soup):
        if soup.name is not None:
            for child in soup.children:
                # process node
                # print( str (child.name) + ":" + str (type (child)))
                if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol', 'pre']:  # Add tags to collect inner text from html source.
                    chld = str (child)
                    print (chld.strip (), file=open (out_file_name, 'a+'))  # print valid tags

                walker (child)

    walker (soup=tmp_soup)

    with open (out_file_name) as f:  # stripping lines of the file
        for lin in f:
            print (lin.strip (), file=open (last_file, 'a+'))

    print (f'Check file {last_file} for final md file.')
    os.system (f'rm -rf {out_file_name}')


def driver(input_file='input.txt', out_file_dir='out/'):
    with open (input_file, 'r') as f:
        for url in f:
            url = url.strip()
            out_file = Path (url).resolve ().stem +'.md'
            os.system(f'rm -rf {out_file}')

            try:
                generate_md_file_from_html (url=url, last_file=out_file_dir+out_file)
            except:
                raise f'Error getting source html'


if __name__ == '__main__':
    driver (input_file='input.txt')
