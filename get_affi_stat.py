import time
import re
import random
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

class AffiStat:

    def __init__(self):
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.affi_syn = {}
        f = open('affi_syn.txt', 'r')
        for line in f.readlines():
            k, v = line.strip().split('\t')
            self.affi_syn[k] = v
        self.affi_mv = {}
        f = open('affi_stop_words.txt', 'r')
        for line in f.readlines():
            self.affi_mv[line.strip('\n')] = ' '
        self.affi_list = {}
        f = open('affi_list.txt', 'r')
        for line in f.readlines():
            affi, region, country, typ = line.strip('\n').split('\t')
            self.affi_list[affi] = (region, country, typ)

    def get_item(self):
        scholar_labels = ['machine_learning', 'deep_learning', 'artificial_intelligence', 'manual', 'natural_language_processing', 'nlp', 'computational_linguistics', 'data_mining', 'information_retrieval', 'computer_vision', 'robotics']

        citation_dict = {}
        for scholar_label in scholar_labels:
            citation_f = open('citation_stat/' + scholar_label + '_citation.txt', 'r')
            citation_lines = citation_f.readlines()
            for citation_line in citation_lines:
                items = citation_line.strip().split('\t')
                if items[0] not in citation_dict:
                    citation_dict[items[0]] = int(items[1])
        
        scholar_dict = {}
        for scholar_label in scholar_labels:
            scholar_f = open('scholar_list/' + scholar_label + '.txt', 'r')
            scholar_lines = scholar_f.readlines()
            for scholar_line in scholar_lines:
                items = scholar_line.strip().split('\t')
                if items[0] not in scholar_dict:
                    scholar_dict[items[0]] = scholar_line

        f = open('scholar_list/all.txt', 'w')
        affi_dict = {k: (0, [], 0) for k in self.affi_list}
        region_dict = {}
        country_dict = {}
        for _, scholar_line in scholar_dict.items():
            f.write(scholar_line)
            items = scholar_line.strip().split('\t')
            affiliation = items[2].lower()
            citation = citation_dict[items[0]]
            for k, v in self.affi_syn.items():
                if k in affiliation:
                    affiliation = affiliation.replace(k, v)
            for item in self.affi_mv:
                if re.search(item, affiliation):
                    affiliation = re.sub(item, ' ', affiliation)
            affiliation = affiliation.strip()
            affiliation = re.sub(' +', ' ', affiliation)
            if len(set(affiliation.split(' '))) == 1:
                affiliation = affiliation.split(' ')[0]
            if affiliation.split(' ')[0] in self.affi_list:
                affiliation = affiliation.split(' ')[0]
            if affiliation in affi_dict:
                num, l, total_citation = affi_dict[affiliation]
                num += 1
                l.append(items[2].lower())
                total_citation += citation
                affi_dict[affiliation] = (num, l, total_citation)

                region, country, _ = self.affi_list[affiliation]
                if region in region_dict:
                    num, total_citation = region_dict[region]
                    num += 1
                    total_citation += citation
                    region_dict[region] = (num, total_citation)
                else:
                    region_dict[region] = (1, citation)
                if country in country_dict:
                    num, total_citation = country_dict[country]
                    num += 1
                    total_citation += citation
                    country_dict[country] = (num, total_citation)
                else:
                    country_dict[country] = (1, citation)
            else:
                # affi_dict[affiliation] = (1, [items[2].lower()])
                print('%s for %s cannot be found' % (affiliation, items[2].lower()))
        print('%s scholars from %s affiliations are found!' % (len(scholar_dict), len(affi_dict)))
        del region_dict['unk']
        del country_dict['unk']
        print('affiliation ranking by scholar number:')
        affi_dict = {k: v for k, v in sorted(affi_dict.items(), key=lambda item: item[1], reverse=True)}
        for i, (k, v) in enumerate(affi_dict.items()):
            print(i + 1, k, v[0], end=', ')
        print('\n')
        print('affiliation (academia) ranking by scholar number:')
        i = 1
        for k, v in affi_dict.items():
            if self.affi_list[k][2] != 'a':
                continue
            print(i, k, v[0], end=', ')
            i += 1
        print('\n')
        print('affiliation (industry) ranking by scholar number:')
        i = 1
        for k, v in affi_dict.items():
            if self.affi_list[k][2] != 'i':
                continue
            print(i, k, v[0], end=', ')
            i += 1
        print('\n')
        print('affiliation ranking by citation:')
        affi_dict = {k: v for k, v in sorted(affi_dict.items(), key=lambda item: item[1][2], reverse=True)}
        for i, (k, v) in enumerate(affi_dict.items()):
            print(i + 1, k, v[2], end=', ')
        print('\n')
        print('affiliation (academia) ranking by citation:')
        i = 1
        for k, v in affi_dict.items():
            if self.affi_list[k][2] != 'a':
                continue
            print(i, k, v[2], end=', ')
            i += 1
        print('\n')
        print('affiliation (industry) ranking by citation:')
        i = 1
        for k, v in affi_dict.items():
            if self.affi_list[k][2] != 'i':
                continue
            print(i, k, v[2], end=', ')
            i += 1
        print('\n')
        print('affiliation ranking by citation/scholar number:')
        affi_dict = {k: v for k, v in sorted(affi_dict.items(), key=lambda item: item[1][2]/item[1][0], reverse=True)}
        for i, (k, v) in enumerate(affi_dict.items()):
            print(i + 1, k, int(v[2]/v[0]), end=', ')
        print('\n')
        print('country ranking by scholar number:')
        country_dict = {k: v for k, v in sorted(country_dict.items(), key=lambda item: item[1], reverse=True)}
        for i, (k, v) in enumerate(country_dict.items()):
            print(i + 1, k, v[0], end=', ')
        print('\n')
        print('country ranking by citation:')
        country_dict = {k: v for k, v in sorted(country_dict.items(), key=lambda item: item[1][1], reverse=True)}
        for i, (k, v) in enumerate(country_dict.items()):
            print(i + 1, k, v[1], end=', ')
        print('\n')
        print('country ranking by citation/scholar number:')
        country_dict = {k: v for k, v in sorted(country_dict.items(), key=lambda item: item[1][1]/item[1][0], reverse=True)}
        for i, (k, v) in enumerate(country_dict.items()):
            print(i + 1, k, int(v[1]/v[0]), end=', ')
        print('\n')
        print('region ranking by scholar number:')
        region_dict = {k: v for k, v in sorted(region_dict.items(), key=lambda item: item[1], reverse=True)}
        for i, (k, v) in enumerate(region_dict.items()):
            print(i + 1, k, v[0], end=', ')
        print('\n')
        print('region ranking by citation:')
        region_dict = {k: v for k, v in sorted(region_dict.items(), key=lambda item: item[1][1], reverse=True)}
        for i, (k, v) in enumerate(region_dict.items()):
            print(i + 1, k, v[1], end=', ')
        print('\n')
        print('region ranking by citation/scholar number:')
        region_dict = {k: v for k, v in sorted(region_dict.items(), key=lambda item: item[1][1]/item[1][0], reverse=True)}
        for i, (k, v) in enumerate(region_dict.items()):
            print(i + 1, k, int(v[1]/v[0]), end=', ')
        print('\n')

affistat = AffiStat()
affistat.get_item()
