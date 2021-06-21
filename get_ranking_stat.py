# -*- coding: utf-8 -*-
import torch
import pandas as pd
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--label', type=str, required=True, help='label')
parser.add_argument('--batch_size', type=int, required=True, help='batch size')
parser.add_argument('--topn', type=int, required=True, help='topn')

args = parser.parse_args()
label = args.label
batch_size = args.batch_size
topn = args.topn

# Prepare data
df = pd.read_excel('scholar_stat/' + label + '.xlsx')
scholar_list = list(df.itertuples(index=False))
name2feature = {}
for scholar in scholar_list:
    name2feature[scholar[1]] = np.array(scholar[3:])

f = open('ranking_dataset/' + label + '_data.txt', 'r')
scholar_tiers = []
scholar_pairs = []
for line in f.readlines():
    scholar_tiers.append(line.strip().split('\t'))
for i in range(len(scholar_tiers)):
    current_tier_scholars = scholar_tiers[i]
    for scholar in current_tier_scholars:
        for j in range(i + 1, len(scholar_tiers)):
            lower_tier_scholars = scholar_tiers[j]
            for lower_scholar in lower_tier_scholars:
                if scholar == lower_scholar:
                    print('Same name error: {}'.format(lower_scholar))
                scholar_pairs.append((scholar, lower_scholar))

dtype = torch.float
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Training
hidden_size = 300
learning_rate = 5e-4
l2_weight = 1e-5
model = torch.nn.Sequential(
    torch.nn.Linear(20, hidden_size),
    torch.nn.ReLU(),
    torch.nn.Linear(hidden_size, 1),
)
model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=l2_weight)
print('batch size: %s, total_num' % batch_size, len(scholar_pairs))
for i in range(5000):
    scholar1_list, scholar2_list = [], []
    cnt = 0
    random.shuffle(scholar_pairs)
    # print(scholar_pairs)
    for scholar_pair in scholar_pairs:
        scholar1, scholar2 = scholar_pair
        scholar1_list.append(name2feature[scholar1])
        scholar2_list.append(name2feature[scholar2])
        cnt += 1
        if cnt >= batch_size:
            break

    score1 = model(torch.tensor(np.array(scholar1_list), dtype=torch.float32).to(device))
    score2 = model(torch.tensor(np.array(scholar2_list), dtype=torch.float32).to(device))
    max_margin_loss, _ = torch.max(torch.cat([score2 - score1 + 0.01, torch.zeros([batch_size, 1]).to(device)], -1), -1)
    loss = torch.sum(max_margin_loss)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if i >= 0:
        # Testing
        scholar1_list, scholar2_list = [], []
        for scholar_pair in scholar_pairs:
            scholar1, scholar2 = scholar_pair
            scholar1_list.append(name2feature[scholar1])
            scholar2_list.append(name2feature[scholar2])
        score1 = model(torch.tensor(np.array(scholar1_list), dtype=torch.float32).to(device))
        score2 = model(torch.tensor(np.array(scholar2_list), dtype=torch.float32).to(device))
        max_margin_loss, _ = torch.max(torch.cat([score2 - score1 + 0.01, torch.zeros([len(scholar_pairs), 1]).to(device)], -1), -1)
        loss = torch.sum(max_margin_loss)
        cost = loss.item()
        if cost / len(scholar_pairs) <= 0.00:
            outliers = {}
            for scholar_pair in scholar_pairs:
                scholar1_list, scholar2_list = [], []
                scholar1, scholar2 = scholar_pair
                scholar1_list.append(name2feature[scholar1])
                scholar2_list.append(name2feature[scholar2])
                score1 = model(torch.tensor(np.array(scholar1_list), dtype=torch.float32).to(device))
                score2 = model(torch.tensor(np.array(scholar2_list), dtype=torch.float32).to(device))
                max_margin_loss, _ = torch.max(torch.cat([score2 - score1 + 0.01, torch.zeros([1, 1]).to(device)], -1), -1)
                if max_margin_loss.item() > 0.0:
                    # print(scholar1_list, scholar2_list)
                    if scholar1_list[0][0] in outliers:
                        outliers[scholar1_list[0][0]] += 1
                    else:
                        outliers[scholar1_list[0][0]] = 1
                    if scholar2_list[0][0] in outliers:
                        outliers[scholar2_list[0][0]] += 1
                    else:
                        outliers[scholar2_list[0][0]] = 1 
            if len(outliers) != 0:
                print(outliers)
            break
    if i % 500 == 0 and i >= 0:
        print(cost / len(scholar_pairs))

# Predict
name2score = {}
for name, feature in name2feature.items():
    score = model(torch.tensor(feature, dtype=torch.float32).to(device))
    name2score[name] = score.item()
name2score = dict(sorted(name2score.items(), key=lambda item: item[1], reverse=True))
max_score, min_score = -10000000, 10000000
for name, score in name2score.items():
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score

fw = open('ranking_stat/' + label + '_ranking.txt', 'w')
cnt = 0
for name, score in name2score.items():
    fw.write('%s\t%s\n' % (name, (score - min_score) / (max_score - min_score)))
    cnt += 1
    if cnt <= topn:
        print(name, (score - min_score) / (max_score - min_score))

