import os
import sys, argparse
import requests
from bs4 import BeautifulSoup, Tag


def generate_md_file_from_html(url=None, source=None):
    out_file_name = 'tmp_out.md'
    last_file = 'out.md'

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
                if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol', 'pre']: # Add tags to collect inner text from html source.
                    chld = str (child)
                    print (chld.strip (), file=open (out_file_name, 'a+')) # print valid tags

                walker (child)

    walker (soup=tmp_soup)

    with open (out_file_name) as f:  # stripping lines of the file
        for lin in f:
            print (lin.strip (), file=open (last_file, 'a+'))

    print (f'Check file {last_file} for final md file.')


if __name__ == '__main__':
    '''Provide url or offline html source file_path    
    --url: give online page url
    or give 
    --source: offline html file e.g. index.html
    '''
    argument_parser = argparse.ArgumentParser ()
    argument_parser.add_argument ("--url", required=False)
    argument_parser.add_argument ("--source", required=False)
    args = argument_parser.parse_args ()
    if args.url:
        generate_md_file_from_html (url=args.url)
    elif args.source:
        generate_md_file_from_html (source=args.source)
    else:
        raise f'Error getting source html'
