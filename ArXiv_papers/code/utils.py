import os
from glob import glob
import re

class Paper:
    """ 각 Paper의 tex file과 bbl file
    """
    def __init__(self, path):
        self.path = path
        self.tex = []
        self.bbl = []
        for file in glob(path + '/*'):
            if file[-4:] == '.tex':
                self.tex.append(file)
            elif file[-4:] == '.bbl':
                self.bbl.append(file)
        
        self.ref_id2title = []
        self.pairs = []
        self.paper_ref_ids = []
        
        self.get_ref_id2title()
        
        self.paper_ref_ids = [list(id_info.keys())[0] for id_info in self.ref_id2title]
        
        self.get_pairs()
        
        self.convert_all_references_to_title()
        
    def get_pairs(self):
        """ Reference가 포함된 문장과 Reference의 쌍을 얻는 함수.
        """
        # tex 파일 한 개인 경우에만 처리
        if len(self.tex) == 1:
            texfile = self.tex[0]
            
            pattern = re.compile('\\\\cite\[?[-\s.,:0-9a-zA-Z]*\]?\{[-\s,:0-9a-zA-Z]*\}')
            
            try:
                with open(texfile, 'r') as f:
                    all_lines = f.readlines()
                    for line in all_lines:
                        if line.count('\cite') == 1:
                            citation = re.findall(pattern, line)    # ['\\cite{Kai, Lichtenbaum, Skorobogatov}']
                                                                  # ['\\cite[Remark 21.3.2]{Patnaik}']
                            if citation:  # regex expression으로 찾아진 부분이 존재하면
                                info = {}
                                try:
                                    end = citation[0].index(']')
                                    ref = citation[0][end+2:-1]
                                except:
                                    ref = citation[0][6:-1]        # ref: 'Kai, Lichtenbaum, Skorobogatov'
                                
                                ref_list = ref.split(',')
                                ref_list = [x.strip() for x in ref_list]
                                
                                if len(ref_list) >= 1:
                                    line = line.strip()
                                    
                                    info["sentence"] = line
                                    info["reference"] = ref_list
                                
                                self.pairs.append(info)
            except:
                print('file을 열 수 없습니다(Encoding error)')
        return self.pairs

    def get_ref_id2title(self):
        """ tex file 안의 ref id와 실제 paper title을 대응시켜주는 함수
        """
        # bbl 파일 한 개인 경우에만 처리
        if len(self.bbl) == 1:
            bblfile = self.bbl[0]
            
            with open(bblfile, 'r') as f:
                all_lines = f.read()
                
                bib_items = all_lines.split('\\bibitem')[1:-1]
                
                for item in bib_items:
                    h, t = item.index('{'), item.index('}')
                    
                    ref_dict = dict()
                    
                    key = item[h+1:t]
                    value = item[t+1:].strip()
                    
                    ref_dict[key] = value
                    
                    self.ref_id2title.append(ref_dict)
                    
        return self.ref_id2title
    
    def convert_all_references_to_title(self):
        """ 각 tex file 안의 ref id를 실제 paper title로 변환하여 self.pairs에 저장하는 함수
        """
        for i, items in enumerate(self.pairs):
            if 'reference' in items.keys():
                ref_id_list = items['reference']

                title_reference = []
    
                for ref_id in ref_id_list:
                    for id_info in self.ref_id2title:
                        if ref_id == list(id_info.keys())[0]:    
                            title_reference.append(list(id_info.values())[0])
                
                self.pairs[i]['reference'] = title_reference
            
        return self.pairs 