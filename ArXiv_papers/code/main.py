import os
from glob import glob
import re
import json
from collections import defaultdict, OrderedDict
from utils import Paper

def all_paper_dirs():
    """ 모든 paper directory 이름을 가져오는 함수.
    """
    subdirs = []
    for dirs in glob('../data/*'):
        if os.path.isdir(dirs):
            for path in glob(dirs + '/*'):
                if os.path.isdir(path):
                    subdirs.append(path)
    return subdirs

if __name__ == "__main__":
    subdirs = all_paper_dirs()

    data = OrderedDict()
    new_data = OrderedDict()
    final_data = OrderedDict()
    
    for path in subdirs:
        print(path)
        paper = Paper(path)
        data[path] = paper.pairs

    for paper_dir in data.keys():
        pairs = data[paper_dir]
        new_data[paper_dir] = []
        for item in pairs:
            if len(item['reference']) > 0:
                new_data[paper_dir].append(item)
        if len(new_data[paper_dir]) > 0:
            final_data[paper_dir] = new_data[paper_dir]

    with open('../data/sentence_reference_pairs.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent='\t')