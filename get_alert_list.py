# -*- coding: utf-8 -*-
import torch
import pandas as pd
import numpy as np
import random
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--ml_num', type=int, required=True, help='ml number')
parser.add_argument('--nlp_num', type=int, required=True, help='nlp number')
parser.add_argument('--dmir_num', type=int, required=True, help='dmir number')

args = parser.parse_args()
ml_num = args.ml_num
nlp_num = args.nlp_num
dmir_num = args.dmir_num
file_name = 'ranking_stat/all.txt'

# Check whether previous list exists
is_previous = os.path.exists(file_name)
if is_previous:
    previous_list = [line.strip() for line in open(file_name, 'r').readlines()]
else:
    previous_list = []

fw = open('ranking_stat/all.txt', 'w')
new_list = []
# ML
fr = open('ranking_stat/machine_learning_ranking.txt', 'r')
new_list.extend([line.strip().split('\t')[0] for line in fr.readlines()[:ml_num]])
# NLP
fr = open('ranking_stat/natural_language_processing_ranking.txt', 'r')
new_list.extend([line.strip().split('\t')[0] for line in fr.readlines()[:nlp_num]])
# DMIR
fr = open('ranking_stat/data_mining_and_information_retrieval_ranking.txt', 'r')
new_list.extend([line.strip().split('\t')[0] for line in fr.readlines()[:dmir_num]])

new_list = list(set(new_list))

print('List num: %s' % len(new_list))
print('Removing scholars:')
for scholar in previous_list:
    if scholar not in new_list:
        print(scholar, end=', ')
print()
print('Adding scholars:')
for scholar in new_list:
    if scholar not in previous_list:
        print(scholar, end=',')
    fw.write('%s\n' % scholar)

