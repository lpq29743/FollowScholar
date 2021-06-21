import time
import re
import requests
import random
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True, help='label')

def get_scholar_list(label):
    start = time.clock()
    f = open(label + '.txt', 'w')
    base_url = 'https://scholar.google.com'
    url = base_url + '/citations?view_op=search_authors&mauthors=label:' + label
    total_num = 0
    label_dict = {}
    while True:
        req = requests.get(url)
        soup = BeautifulSoup(req.content)
        items = soup.select('.gs_ai_t')
        for item in items:
            href = item.a['href']
            name = item.a.string
            affiliation = item.find_all(class_='gs_ai_aff')[0].string
            citation = re.findall(r'\d+', item.find_all(class_='gs_ai_cby')[0].string)[0]
            scholar_labels = item.find_all(class_='gs_ai_one_int')
            cnt = 0
            is_major_area = False
            for scholar_label in scholar_labels:
                cnt += 1
                if scholar_label.string.lower().replace(' ', '_') == label and cnt <= 2:
                    is_major_area = True
                if scholar_label.string.lower() in label_dict:
                    label_dict[scholar_label.string.lower()] += 1
                else:
                    label_dict[scholar_label.string.lower()] = 1
            if is_major_area:
                f.write('%s\t%s\t%s\t%s\n' % (href, name, affiliation, citation))
                total_num += 1
        url = base_url + re.findall("window.location='(.+?)'", soup.select('.gsc_pgn_pnx')[0]['onclick'])[0].replace('\\x3d', '=').replace('\\x26', '&')
        print('Processing %s' % url)
        if int(citation) < 3000 or total_num >= 500:
            break
        delay_time = random.randint(25, 35)
        time.sleep(delay_time)
    label_dict = {k: v for k, v in label_dict.items() if v >= 50}
    print(dict(sorted(label_dict.items(), key=lambda item: item[1], reverse=True)))
    end = time.clock()
    print(total_num)
    print(end-start)
        
if __name__ == '__main__':
    args = parser.parse_args()
    get_scholar_list(args.label)

