import time
import re
import requests
import random
from bs4 import BeautifulSoup

class ConfStat:

    def __init__(self):
        name_convert_f = open('scholar_syn.txt', 'r')
        self.name_convert_dict = {}
        wrong_info_f = open('stop_scholars.txt', 'r')
        self.wrong_info_list = []
        for line in name_convert_f.readlines():
            items = line.strip().split('\t')
            self.name_convert_dict[items[0]] = items[1]
        for line in wrong_info_f.readlines():
            self.wrong_info_list.append(line.strip().split('\t')[0])

    def merge(self, all_dict, merge_dict):
        for k, v in merge_dict.items():
            if k in all_dict:
                all_dict[k] += v
            else:
                all_dict[k] = v
        return all_dict

    def get_conf(self):
        all_dict = {}
        all_dict = self.merge(all_dict, self.get_ml_conf())
        all_dict = self.merge(all_dict, self.get_cv_conf())
        all_dict = self.merge(all_dict, self.get_nlp_conf())
        all_dict = self.merge(all_dict, self.get_dm_ir_conf())
        all_dict = self.merge(all_dict, self.get_robotics_conf())
        sort_all_dict = dict(sorted(all_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/all.txt', 'w')
        for k, v in sort_all_dict.items():
            f.write('%s\t%s\n' % (k, v))

    def get_ml_conf(self):
        start = time.clock()
        people_dict = {}
        
        # ICML, ICLR, NEUIPS
        for conf in ['icml2020', 'icml2019', 'icml2018', 'iclr2020', 'iclr2019', 'iclr2018', 'neuips2019', 'neuips2018']:
            fname = 'accept_list/' + conf + '.txt'
            print(fname)
            f = open(fname, 'r')
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                names = lines[i].strip().rstrip(':').split(', ')
                for name in names:
                    if name in self.name_convert_dict:
                        name = self.name_convert_dict[name]
                    if name in self.wrong_info_list:
                        continue
                    if name in people_dict:
                        people_dict[name] += 1
                    else:
                        people_dict[name] = 1

        sort_people_dict = dict(sorted(people_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/machine_learning_conf.txt', 'w')
        for name, num in sort_people_dict.items():
            f.write('%s\t%s\n' % (name, num)) 
        f.close()
        end = time.clock()
        print(end-start)
        return sort_people_dict
    
    def get_cv_conf(self):
        start = time.clock()
        people_dict = {}

        # CVPR, ICCV, ECCV
        for conf in ['cvpr2020', 'cvpr2019', 'cvpr2018', 'iccv2019', 'eccv2020', 'eccv2018']:
            fname = 'accept_list/' + conf + '.txt'
            print(fname)
            f = open(fname, 'r')
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                names = lines[i].strip().rstrip(':').split(', ')
                for name in names:
                    if name in self.name_convert_dict:
                        name = self.name_convert_dict[name]
                    if name in self.wrong_info_list:
                        continue
                    if name in people_dict:
                        people_dict[name] += 1
                    else:
                        people_dict[name] = 1
        
        sort_people_dict = dict(sorted(people_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/computer_vision_conf.txt', 'w')
        for name, num in sort_people_dict.items():
            f.write('%s\t%s\n' % (name, num)) 
        f.close()
        end = time.clock()
        print(end-start)
        return sort_people_dict
    
    def get_nlp_conf(self):
        start = time.clock()
        people_dict = {}
        # ACL, EMNLP, NAACL, COLING
        for conf in ['acl2020', 'acl2019', 'acl2018', 'emnlp2020', 'emnlp2019', 'emnlp2018', 'naacl2019', 'naacl2018', 'coling2020', 'coling2018']:
            fname = 'accept_list/' + conf + '.txt'
            print(fname)
            f = open(fname, 'r')
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                names = lines[i].strip().rstrip(':').split(', ')
                for name in names:
                    if name in self.name_convert_dict:
                        name = self.name_convert_dict[name]
                    if name in self.wrong_info_list:
                        continue
                    if name in people_dict:
                        people_dict[name] += 1
                    else:
                        people_dict[name] = 1
        
        sort_people_dict = dict(sorted(people_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/natural_language_processing_conf.txt', 'w')
        for name, num in sort_people_dict.items():
            f.write('%s\t%s\n' % (name, num)) 
        f.close()
        end = time.clock()
        print(end-start)
        return sort_people_dict
        
    def get_dm_ir_conf(self):
        start = time.clock()
        people_dict = {}

        # SIGKDD, ICDE, WSDM, CIKM, ICDM, SDM, WWW
        for conf in ['kdd2020', 'kdd2019', 'kdd2018', 'icde2020', 'icde2019', 'icde2018', 'wsdm2020', 'wsdm2019', 'wsdm2018', 'cikm2020', 'cikm2019', 'cikm2018', 'icdm2020', 'icdm2019', 'icdm2018', 'sdm2020', 'sdm2019', 'sdm2018', 'www2020', 'www2019', 'www2018']:
            fname = 'accept_list/' + conf + '.txt'
            print(fname)
            f = open(fname, 'r')
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                names = lines[i].strip().rstrip(':').split(', ')
                for name in names:
                    if name in self.name_convert_dict:
                        name = self.name_convert_dict[name]
                    if name in self.wrong_info_list:
                        continue
                    if name in people_dict:
                        people_dict[name] += 1
                    else:
                        people_dict[name] = 1

        # SIGIR 2020
        fname = 'accept_list/sigir2020.txt'
        print(fname)
        f = open(fname, 'r')
        lines = f.readlines()
        for i in range(1, len(lines), 2):
            names = lines[i].strip().split('; ')
            for name in names:
                name = name.split(':')[0]
                if name in self.name_convert_dict:
                    name = self.name_convert_dict[name]
                if name in self.wrong_info_list:
                    continue
                if name in people_dict:
                    people_dict[name] += 1
                else:
                    people_dict[name] = 1

        # SIGIR 2019
        fname = 'accept_list/sigir2019.txt'
        print(fname)
        f = open(fname, 'r')
        lines = f.readlines()
        for i in range(1, len(lines), 3):
            names = lines[i].strip().replace(' and ', ', ').split(', ')
            for name in names:
                if name in self.name_convert_dict:
                    name = self.name_convert_dict[name]
                if name in self.wrong_info_list:
                    continue
                if name in people_dict:
                    people_dict[name] += 1
                else:
                    people_dict[name] = 1
        
        # SIGIR 2018
        fname = 'accept_list/sigir2018.txt'
        print(fname)
        f = open(fname, 'r')
        lines = f.readlines()
        for i in range(2, len(lines), 4):
            names = lines[i].strip().split('; ')
            for name in names:
                name = name.split(' (')[0]
                if name in self.name_convert_dict:
                    name = self.name_convert_dict[name]
                if name in self.wrong_info_list:
                    continue
                if name in people_dict:
                    people_dict[name] += 1
                else:
                    people_dict[name] = 1
        
        sort_people_dict = dict(sorted(people_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/data_mining_and_information_retrieval_conf.txt', 'w')
        for name, num in sort_people_dict.items():
            f.write('%s\t%s\n' % (name, num)) 
        f.close()
        end = time.clock()
        print(end-start)
        return sort_people_dict

    def get_robotics_conf(self):
        start = time.clock()
        people_dict = {}

        # RSS, ICRA, IROS
        for conf in ['rss2019', 'rss2018', 'icra2020', 'icra2019', 'icra2018', 'iros2020', 'iros2019', 'iros2018']:
            fname = 'accept_list/' + conf + '.txt'
            print(fname)
            f = open(fname, 'r')
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                names = lines[i].strip().rstrip(':').split(', ')
                for name in names:
                    if name in self.name_convert_dict:
                        name = self.name_convert_dict[name]
                    if name in self.wrong_info_list:
                        continue
                    if name in people_dict:
                        people_dict[name] += 1
                    else:
                        people_dict[name] = 1
        
        sort_people_dict = dict(sorted(people_dict.items(), key=lambda item: item[1], reverse=True))
        f = open('conf/robotics_conf.txt', 'w')
        for name, num in sort_people_dict.items():
            f.write('%s\t%s\n' % (name, num)) 
        f.close()
        end = time.clock()
        print(end-start)
        return sort_people_dict

confstat = ConfStat()
confstat.get_conf()

