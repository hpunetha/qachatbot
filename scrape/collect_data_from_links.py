# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 14:57:41 2019

@author: hp
"""

import pickle,urllib,text_extract_from_webpage as text


def read_pickle(filename):
    
    with open(filename,'rb') as f:
        arr = pickle.load(f)
    
    return arr

def clean_links(all_links):
    
    all_filtered_links = []
    for i in all_links:
    
        if not (i.lower().endswith('.png') or i.lower().endswith('.pdf')\
        or i.lower().endswith('.jpg') or 'tenders/Tender' in i.lower() or i.lower().endswith('.xlsx')\
        or i.lower().endswith('.jpeg') or i.lower().endswith('.zip')): 
            all_filtered_links.append(i)
            
    return all_filtered_links

    
def driver():
    
    all_links = list(read_pickle('all_iiitd_links.pickle'))[0]
    #print(all_links)
    #print(len(all_links))
    
    
    all_filtered_links = clean_links(all_links)
    
    with open('all_filtered_links.pickle','wb') as f:
        pickle.dump(all_filtered_links,f)
    f.close()
    
    
    path = 'website_scraped_text_new_lxml\\'
    count = 0
    mapping = {}
    
    all_links = list(set(all_filtered_links))
    print(len(all_links))
    content_seen = []
    headings_list = []
    
    file_headings_dict = {}
    
    for i in range(len(all_links)):
        count = count+1
        try:
            html = urllib.request.urlopen(all_links[i]).read()
        except Exception:
            print('links error = '+str(all_links[i]))
        link_text = ''
        try:
            link_text,headings_list = text.text_from_html(html)
        except:
            continue
        
        if len(link_text)>50 and link_text not in content_seen:
            
            mapping[count] = all_links[i]
            
            f = open(path+str(count)+'.txt','w',encoding='utf-8')
            f.write(all_links[i]+'\n')
            file_headings_dict[str(count)+'.txt'] = headings_list
            try:
                f.write(link_text)
            except:
                print('ERROR! link text = '+str(link_text))
            f.close()
            
            content_seen.append(link_text)
            
    with open('all_file_headings_mapping.pickle','wb') as f:
        pickle.dump(file_headings_dict,f)
    f.close()
    
    return file_headings_dict,path


links = read_pickle('all_filtered_links.pickle')
print(len(links))