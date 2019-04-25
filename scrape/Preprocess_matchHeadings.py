
# coding: utf-8

# In[3]:


import pickle

with open('all_file_headings_mapping.pickle', 'rb') as f:
    x = pickle.load(f)


# In[52]:


x['76.txt']


# In[36]:


fdatapath= "C:\\Users\\hpunetha\\PycharmProjects\\Chatbot\\Solr\\preprocess\\website_scraped_text_new_lxml"
foutputpath = "C:\\Users\\hpunetha\\PycharmProjects\\Chatbot\\Solr\\preprocess\\out"


# In[51]:


import os
pathListing = os.walk(fdatapath)


newdict ={}


for root,dirlist,filelist in pathListing:
        for filename in filelist:
            headdict ={}
            pathvar = os.path.join(root,filename)
#             print(pathvar)
            fname= os.path.basename(pathvar)
#             print(fname)
            text=""
            
            
            
#             ########Test Input
            fname="76.txt"
            pathvar="C:\\Users\\hpunetha\\PycharmProjects\\Chatbot\\Solr\\preprocess\\website_scraped_text_new_lxml\\76.txt"
#             #####input end
            
            totlen = len(x[fname])
            for headindex in range(totlen):
                heading = x[fname][headindex]
                last=False
                found=False
                if(headindex==totlen-1):
                    last=True
                
                
                
                with open(pathvar, encoding='utf8') as f:
    #                 text = f.read()
    #             print(text)
                    filltext = ""
                    for line in f:
                        if heading.strip(' \n') == line.strip(' \n'):
                            found= True
                            continue
                        if found:                           
                            if last==False:
                                nexthead = x[fname][headindex+1]
                                if nexthead.strip(' \n') != line.strip(' \n'):
                                    filltext += line
                                else:
                                    found=False
                                    break
                            else:
                                filltext += line
                    
                    print("=======================================")
                    print("heading=> ",heading)
                    print("text=> ",filltext)
                    print("=======================================")
                    headdict[heading]=filltext
                    
            import json
            outpath = foutputpath + "\\" +fname
            with open(outpath + ".json", 'w') as outfile:
                json.dump(headdict, outfile)
            print("*********done for ",fname)
            break
        break
            


# In[60]:


link = "http://iiitd.ac.in/research/publications-to"


def flattenlist(nonfllist):
    import collections
    for val in nonfllist:
        if not isinstance(val, (str,bytes)) and isinstance(val , collections.Iterable):
            yield from flattenlist(val)
        else:
            yield val



val = link.split('/')
t = 'iiitd.ac.in'
ind = val.index(t)
tags = [val[i] for i in range(ind+1,len(val))]
tags = [c.split('-') for c in tags]

tags = list(flattenlist(tags))
tags

