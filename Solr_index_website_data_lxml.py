# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:22:26 2019

@author: hp
"""

import pysolr,csv,os, pickle,re
import random,string,json

class Solr_Index:
    
    
    def __init__(self):
        
        self.all_documents = []
        self.solr = pysolr.Solr('http://localhost:8983/solr/all_paragraphs_iiitd', timeout=10)
        
    def read_pickle(self,filename):
    
        with open(filename,'rb') as f:
            arr = pickle.load(f)
        
        return arr
    

    def get_data(self,path='website_scraped_text_new_lxml'):
        
        documents = []
        headings_file_mapping = read_pickle('all_file_headings_mapping.pickle')
#        print(headings_file_mapping['3.txt'])
        
        for filename in os.listdir(path):
            
            f = open(path+'\\'+filename,encoding='utf-8')
            all_file_text = f.readlines()
            url = all_file_text[0].strip('\n')
            doc_text = ' '.join(' '.join(all_file_text[1:]).split())
            
            tags = headings_file_mapping[filename]
            
            documents.append({'url':url,'doc_text':doc_text,'tags':tags})
        
        
        return documents
    
    def add_to_index(self,documents):
        self.solr.add(documents)
        

def remove_unwanted_lxml(links,all_data):
    
    updated_data = []
    for j in all_data:
        if j['url'] in links:
            continue
        else:
            j['doc_text'].replace('\\','')
            j['doc_text'].replace('\"','')
            j['doc_text'] = re.sub(r"You are here", r"", j['doc_text'])
            j['title_orig'].replace('\\','')
            j['title_orig'].replace('\"','')
            
            updated_data.append(j)
    
    print(len(updated_data))
    return updated_data

def old_data_process():
    
    with open("all_data.json", "r") as read_file:
        data = json.load(read_file)

    new_data = []    
    for each_dict in data:
        
        temp = {}
        temp['title_orig'] = each_dict['title']
        temp['doc_text'] = each_dict['doc_text']
        temp['degree'] = each_dict['degree'].lower()
        temp['branch'] = each_dict['branch'].lower()
        temp['url'] = 'http://iiitd.ac.in/academics/resources'
        temp['search_tags'] = ['academics','regulations','rules']
        if temp['branch']!='all':
            temp['search_tags'].append(temp['branch'])
        if temp['degree']!='all':
            temp['search_tags'].append(temp['degree'])
        temp['title'] = str(temp['title_orig']) + ' '+ ' '.join(temp['search_tags'])
        new_data.append(temp)

    return new_data

solr_obj = Solr_Index()

links = ['https://iiitd.ac.in/tenders','http://iiitd.ac.in/phase2-construction',
             'https://iiitd.ac.in/life/hostels/hostel-site','http://iiitd.ac.in/about/act',
             'http://iiitd.ac.in/research/publications','http://iiitd.ac.in/admission/btech/2012/faq',
             'http://iiitd.ac.in/admission/btech/2013/faq','http://iiitd.ac.in/admission/btech/2014/faq',
             'http://iiitd.ac.in/admission/btech/2015/faq','http://iiitd.ac.in/admission/btech/2016/faq',
             'http://iiitd.ac.in/admission/btech/2017/faq']
documents_lxml = solr_obj.read_pickle('all_final_documents.pickle')
updated_lxml_data = remove_unwanted_lxml(links,documents_lxml)

processed_old_data = old_data_process()
solr_obj.add_to_index(updated_lxml_data)
solr_obj.add_to_index(processed_old_data)

