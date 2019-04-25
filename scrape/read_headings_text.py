# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 17:35:33 2019

@author: hp
"""

import os,json,pickle
from ast import literal_eval
fdatapath = 'headings_text_out\\out'
pathListing = os.walk(fdatapath)
#s = '[Overall Average salary: 11.41\xa0 lacs  placement past-stats]'

print(x)        
newdict ={}

def flattenlist(nonfllist):
    import collections
    for val in nonfllist:
        if not isinstance(val, (str,bytes)) and isinstance(val , collections.Iterable):
            yield from flattenlist(val)
        else:
            yield val


def clean_text(text):
    
    st = ' '.join(text.split())
    s = st.replace("'","")
    s = s.replace("\xa0","")
    x = literal_eval("'%s'" %s)
    return x


all_documents_final = []

all_webpage_text_path = 'website_scraped_text_new_lxml'

for root,dirlist,filelist in pathListing:
    for filename in filelist:
        
        pathvar = os.path.join(root,filename)
#        print(pathvar)
        fname= os.path.basename(pathvar)
#        print(fname)
        
        f1 = open(all_webpage_text_path+'\\'+str(fname[:-5]),encoding = 'utf-8')
        all_file_text = f1.readlines()
        url = all_file_text[0].strip('\n')
        f1.close()
        
        
        f = open(pathvar,encoding = 'utf-8')
        heading_text = json.load(f)
#        print(heading_text)
        
        for heading,corresponding_text in heading_text.items():
            if len(clean_text(corresponding_text))>5:
                
                title_orig = clean_text(heading)
                branch = ''
                doc_text = clean_text(corresponding_text)
                
                url1 = url
                
                
                val = url1.split('/')
                t = 'iiitd.ac.in'
                ind = val.index(t)
                tags = [val[i] for i in range(ind+1,len(val))]
                tags = [c.split('-') for c in tags]
                
                tags = list(flattenlist(tags))
                search_tags = tags
                
                
                if 'btech' in tags:
                    degree = 'btech'
                elif 'mtech' in tags:
                    degree = 'mtech'
                elif 'phd' in tags:
                    degree = 'phd'
                else:
                    degree = 'all'
                
                title_with_tags = clean_text(title_orig + ' '+' '.join(tags))
                
                if 'cse' in url1:
                    branch = branch +' cse '
                if 'ece' in url1:
                    branch = branch +' ece '
                if 'cb' in url1:
                    branch = branch +' cb '
                if 'csam' in url1:
                    branch = branch +' csam '
                if 'csd' in url1:
                    branch = branch +' csd '
                if 'csss' in url1:
                    branch = branch +' csss '
                if 'csb' in url1:
                    branch = branch +' csb '
                
                branch = clean_text(branch.strip())
                if branch == '':
                    branch = 'all'
                
                all_documents_final.append({'url':url1,'title_orig':title_orig,'doc_text':doc_text,
                                            'search_tags':tags,'degree':degree,'title':title_with_tags,
                                            'branch':branch})


with open('all_final_documents.pickle','wb') as f:
    pickle.dump(all_documents_final,f)
    f.close()
        
        

           