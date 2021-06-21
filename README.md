# FollowScholar

A tool for obtaining the list of top scholars on a specific research topic as well as their scholar statistics.

## Table of Contents

- [Features](#features)
  - [Get scholar list](#get-scholar-list)
  - [Get citation statistics of scholars](#get_citation_statistics_of_scholars)
  - [Get conference statistics of scholars](#get_conference_statistics_of_scholars)
  - [Get affiliation statistics of scholars](#get_affiliation_statistics_of_scholars)
  - [Get statistics of scholars](#get_statistics_of_scholars)
  - [Get ranking results of scholars](get_ranking_results_of_scholars)
- [To-do List](#to-do_list)

### Features

#### Get scholar list

Get scholar list with label "Natural Language Processing".

```bash
python get_scholar_list.py --label natural_language_processing
```

While getting scholar list, we only consider:

- Scholars whose first two labels contain the specific label.
- Scholars whose citation larger than 3000.
- Top500 scholars in the specific area.

In this project, we have obtained the scholar lists with the following labels:

- Deep Learning
- Artificial Intelligence
- Machine Learning
- Robotics
- Computer Vision
- Data Mining
- Information Retrieval
- Natural Language Processing
- Computational Linguistics
- NLP

The obtained scholar lists are saved at the folder `scholar_list`, and we are not planning to update it. Some excellent scholars (high citations and publish some papers on top-tier conferences) will manually added in the file `scholar_list/manual.txt`. In addition, we manually delete or modify some information due to the wrong information.

#### Get citation statistics of scholars

After obtaining the scholar list with the specified label, we then can get the citation statistics. For example, the label "Natural Language Processing"

```bash
python get_citation_stat.py --label natural_language_processing
```

The obtained citation statistics are saved at the folder `citation_stat`.

#### Get conference statistics of scholars

In addition to some citation information on the "Google Scholar", the publication information on top-tier conferences is also good information to identify whether a scholar is excellent or not. Therefore, the publication infromation could be obtained.

```bash
python get_conf_stat.py
```

We consider the following top-tier conference for different areas:

- ML (Machine Learning): ICML, ICLR, NeuIPS
- CV (Computer Vision): CVPR, ICCV, ECCV
- NLP (Natural Language Processing): ACL, EMNLP, NAACL, COLING
- DM_IR (Data Mining and Information Retrieval): SIGKDD, ICDE, WSDM, CIKM, ICDM, SDM, WWW, SIGIR
- Robotics: RSS, ICRA, IROS

The obtained conference statistics are saved at the folder `conf_stat`.

#### Get affiliation statistics of scholars

Affiliation statistics are also interesting, and could be obtained.

```bash
pythono get_affi_stat.py
```

#### Get statistics of scholars

To get further detailed information of scholar, we can:

```bash
python get_scholar_stat.py --label natural_language_processing
```

The obtained scholar statistics are saved at the folder `scholar_stat`. The detailed information is as follows:

- name
- affiliation
- total citation
- total citation of each year
- five years citation
- five years citation of each year
- last year citation
- last year citation of each year
- total h_index
- total h_index of each year
- five years h_index
- five years h_index of each year
- total i10_index
- total i10_index of each year
- five years i10_index
- five years i10_index of each year
- paper number in machine learning top-tier conferences
- paper number in computer vision top-tier conferences
- paper number in natural language processing top-tier conferences
- paper number in data mining and information retrieval top-tier conferences
- paper number in robotics top-tier conferences
- the year of the first citation

#### Get ranking results of scholars

##### Data Preparation

Different people have different criterias on ranking scholars. Besides, publications and citations are not the only criterias for ranking scholars. Therefore, we don't provide the data for training the ranking model. You could prepare the dataset in the folder `ranking_dataset` with the form as follows:

```
Scholar_A
Scholar_B\tScholar_C
Scholar_D
```

It means Scholar_A > Scholar_B and Scholar_C, Scholar_B > Scholar_D and Scholar_C > Scholar_D.

##### Training

The model could be trained and be stopped training when it fits all the training data.

```bash
python get_ranking_stat.py --label natural_language_processing --batch_size 32 --topn 200
```

The obtained ranking results are save in the folder `ranking_stat`.

### To-do List

- Teacher-Student; Coauther
- Considering author order

