import os
import time
import re
import requests
import random
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True, help='label')

def get_citation_stat(label):
    start = time.clock()
    base_url = 'https://scholar.google.com'
    if os.path.exists('citation_stat/' + label + '_citation.txt'):
        fr = open('citation_stat/' + label + '_citation.txt', 'r')
        process_dict = {line.strip().split('\t')[0]: 0 for line in fr.readlines()}
        fa = open('citation_stat/' + label + '_citation.txt', 'a')
    else:
        process_dict = {}
        fa = open('citation_stat/' +label + '_citation.txt', 'w')
    fr = open('scholar_list/' + label + '.txt', 'r')
    lines = fr.readlines()
    for line in lines:
        infos = line.strip().split()
        if infos[0] in process_dict:
            continue
        url = base_url + infos[0]
        print(url)
        req = requests.get(url)
        soup = BeautifulSoup(req.content)

        items = soup.select('.gsc_rsb_std')
        if len(items) == 0:
            continue
        all_citation = items[0].string
        five_years_citation = items[1].string
        all_hindex = items[2].string
        five_years_hindex = items[3].string
        all_i10index = items[4].string
        five_years_i10index = items[5].string

        items = soup.select('.gsc_g_t')
        first_year = items[0].string

        items = soup.select('.gsc_g_al')
        last_year_citation = items[-1].string

        fa.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (infos[0], all_citation, five_years_citation, all_hindex, five_years_hindex, all_i10index, five_years_i10index, first_year, last_year_citation))

        delay_time = random.randint(25, 35)
        time.sleep(delay_time)
    end = time.clock()
    print(end-start)

if __name__ == '__main__':
    args = parser.parse_args()
    get_citation_stat(args.label)

