import time
import re
import random
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True, help='label')

class ScholarStat:

    def __init__(self, label):
        self.label = label
        date = time.strftime("%Y-%m-%d", time.localtime())
        name_convert_f = open('scholar_syn.txt', 'r')
        self.name_convert_dict = {}
        wrong_info_f = open('stop_scholars.txt', 'r')
        self.wrong_info_list = []
        for line in name_convert_f.readlines():
            items = line.strip().split('\t')
            self.name_convert_dict[items[0]] = items[1]
        for line in wrong_info_f.readlines():
            self.wrong_info_list.append(line.strip().split('\t')[0])

    def get_conf_dict(self, conf_fname):
        conf_f = open(conf_fname, 'r')
        conf_lines = conf_f.readlines()
        conf_dict = {}
        for line in conf_lines:
            items = line.strip().split('\t')
            if len(items) != 2:
                continue
            name, cnt = items
            if name in self.name_convert_dict:
                name = self.name_convert_dict[name]
            if name in self.wrong_info_list:
                continue
            conf_dict[name] = int(cnt)
        return conf_dict

    def get_item(self):
        current_year = 2021
        scholar_labels = ['machine_learning', 'deep_learning', 'artificial_intelligence', 'manual', 'natural_language_processing', 'nlp', 'computational_linguistics', 'data_mining', 'information_retrieval', 'computer_vision', 'robotics']

        ml_conf_dict = self.get_conf_dict('conf_stat/machine_learning_conf.txt')
        cv_conf_dict = self.get_conf_dict('conf_stat/computer_vision_conf.txt')
        nlp_conf_dict = self.get_conf_dict('conf_stat/natural_language_processing_conf.txt')
        dm_ir_conf_dict = self.get_conf_dict('conf_stat/data_mining_and_information_retrieval_conf.txt')
        robotics_conf_dict = self.get_conf_dict('conf_stat/robotics_conf.txt')
        scholar_dict, conf_dict = {}, {}
        for scholar_label in scholar_labels:
            scholar_f = open('scholar_list/' + scholar_label + '.txt', 'r')
            scholar_citation_f = open('citation_stat/' + scholar_label + '_citation.txt', 'r')
            scholar_lines = scholar_f.readlines()
            scholar_citation_lines = scholar_citation_f.readlines()
            assert len(scholar_lines) == len(scholar_citation_lines), scholar_label
            for scholar_line, scholar_citation_line in zip(scholar_lines, scholar_citation_lines):
                items = scholar_line.strip().split('\t')
                name = items[1]
                affiliation = items[2]
                _, total_citation, five_years_citation, total_h_index, five_years_h_index, total_i10_index, five_years_i10_index, year, last_year_citation = scholar_citation_line.strip().split('\t')
                if name in self.name_convert_dict:
                    name = self.name_convert_dict[name]
                if name in self.wrong_info_list:
                    continue
                scholar_dict[name] = (affiliation, total_citation, five_years_citation, total_h_index, five_years_h_index, total_i10_index, five_years_i10_index, year, last_year_citation)
        
        if self.label == 'machine_learning':
            conf_dict = ml_conf_dict
        elif self.label == 'computer_vision':
            conf_dict = cv_conf_dict
        elif self.label == 'natural_language_processing':
            conf_dict = nlp_conf_dict
        elif self.label == 'data_mining_and_information_retrieval':
            conf_dict = dm_ir_conf_dict
        elif self.label == 'robotics':
            conf_dict = robotics_conf_dict

        # People not in the conf
        no_paper_cnt, no_max_paper_cnt, no_paper_cnt = 0, 0, 0
        data = []
        no_major_list, no_paper_list = [], []
        for name, info in scholar_dict.items():
            ml_conf_num = ml_conf_dict[name] if name in ml_conf_dict else 0
            cv_conf_num = cv_conf_dict[name] if name in cv_conf_dict else 0
            nlp_conf_num = nlp_conf_dict[name] if name in nlp_conf_dict else 0
            dm_ir_conf_num = dm_ir_conf_dict[name] if name in dm_ir_conf_dict else 0
            robotics_conf_num = robotics_conf_dict[name] if name in robotics_conf_dict else 0
            max_num = max(ml_conf_num, cv_conf_num, nlp_conf_num, dm_ir_conf_num, robotics_conf_num)
            if max_num == 0:
                no_paper_list.append(name)
                no_paper_cnt += 1
            elif name not in conf_dict:
                no_paper_cnt += 1
            elif name in conf_dict and conf_dict[name] < max_num:
                no_major_list.append(name)
                no_max_paper_cnt += 1
            else:
                affiliation, total_citation, five_years_citation, total_h_index, five_years_h_index, total_i10_index, five_years_i10_index, year, last_year_citation = info
                dm_ir_conf_num = dm_ir_conf_dict[name] if name in dm_ir_conf_dict else 0
                robotics_conf_num = robotics_conf_dict[name] if name in robotics_conf_dict else 0
                data.append([name, affiliation, float(total_citation), float(total_citation) / (current_year - float(year)), float(five_years_citation), float(five_years_citation) / (current_year - float(year)), float(last_year_citation), float(last_year_citation) / (current_year - float(year)), float(total_h_index), float(total_h_index) / (current_year - float(year)), float(five_years_h_index), float(five_years_h_index) / (current_year - float(year)), float(total_i10_index), float(total_i10_index) / (current_year - float(year)), float(five_years_i10_index), float(five_years_i10_index) / (current_year - float(year)), float(ml_conf_num), float(cv_conf_num), float(nlp_conf_num), float(dm_ir_conf_num), float(robotics_conf_num), float(year)])
        print('scholar list not majoring in the area:')
        print(no_major_list)
        print()
        print('scholar list without any paper:')
        print(no_paper_list[0:100])
        print()
        print('%s/%s scholars meets the requirement, %s scholars do not have any required paper, %s scholars do not major in this area.' % (len(scholar_dict) - no_paper_cnt - no_max_paper_cnt, len(scholar_dict), no_paper_cnt, no_max_paper_cnt))
        print()

        # People not in the scholar
        min_paper_num = 7
        print('scholar list missing with more than %s papers:' % (min_paper_num))
        for name, cnt in conf_dict.items():
            if name not in scholar_dict and cnt >= min_paper_num:
                print(name, end=', ')

        df = pd.DataFrame(data, columns=['name', 'affiliation', 'total_citation', 'average_total_citation', 'five_years_citation', 'average_five_years_ciatation', 'last_year_citation', 'average_last_year_citation', 'total_h_index', 'average_total_h_index', 'five_years_h_index', 'average_five_years_h_index', 'total_i10_index', 'average_total_i10_index', 'five_years_i10_index', 'average_five_years_h10_index', 'ml_paper', 'cv_paper', 'nlp_paper', 'dm_ir_paper', 'robotics_paper', 'year'])
        df.to_excel('scholar_stat/' + self.label + '.xlsx')

args = parser.parse_args()
scholarstat = ScholarStat(args.label)
scholarstat.get_item()
