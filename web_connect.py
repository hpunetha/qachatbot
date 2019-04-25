from flask import Flask, render_template, request
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#import chat_helper as _helper
import time 
# import spacy
import pysolr

bertpath = "E:\\berttrained\\bert-master"
bot=""
class getResults:
    
    def __init__(self):
        
        self.results = []
        self.solr = pysolr.Solr('http://localhost:8983/solr/all_paragraphs_iiitd', timeout=10)
        
        
    def process_query(self,query):
        
#        start1 = time.time()
#        translations_and_syn = _helper.translations_and_synonyms(query)
#        end1 = time.time()
        
        stop_words_list = set(stopwords.words('english'))
        relevant_terms = []
        query_terms = word_tokenize(query)
        relevant_terms = [x for x in query_terms if not x in stop_words_list]
        
        return relevant_terms

    def create_query_for_solr(self,stop_words_removed,noun_entities=[]):
        
        query_types = []
        
        import re
       
            
        qtype1 = ' '.join(stop_words_removed)
        qtype2 = ' '.join(noun_entities)
        docquery = 'doc_text:('+qtype1 +')'
#         docquery2 = 'doc_text:('+qtype2 +')'


         
        valid1 = re.match('^[\w-]+$',docquery) is not None
#         valid2 =re.match('^[\w-]+$',docquery2) is not None

        if(not valid1):
            query_types.append(docquery)
#         query_types.append(docquery2)
#        print(docquery)
        
        titlequery = 'title:('+qtype1 +')^1.25'
        titlequery2 = 'title:('+qtype2 +')^2.0 '
        fullq = titlequery + docquery
#         fullq2 = titlequery2 + docquery2
#        print(fullq)

        valid3 =re.match('^[\w-]+$',fullq) is not None
#         valid4 =re.match('^[\w-]+$',fullq2) is not None
        if(not valid3):
            query_types.append(fullq)
#         if(valid4):
#         query_types.append(fullq2)
#        
        mainquery = '"%s"' % " ".join([a.strip() for a in qtype1.split("\n") if a])
#         mainquery2 = '"%s"' % " ".join([a.strip() for a in qtype2.split("\n") if a])
        
      
        valid5 =re.match('^[\w-]+$',mainquery) is not None
#         valid6 =re.match('^[\w-]+$',mainquery2) is not None
#        print(mainquery)
  
        
        if(not valid5):
            query_types.append(mainquery)
#         query_types.append(mainquery2)
        
        print('query types = '+str(query_types))
        return query_types
        
    def retrieve_results(self,query,filter_queries=[]):
        
        #noun_entities = _helper.extract_nouns(query)
        noun_entities = []
        relevant_terms = self.process_query(query)
        all_query_types = self.create_query_for_solr(relevant_terms,noun_entities)
        print(all_query_types)
    
        
        f = open('results.txt','w')

        # flag= False
        flagres = {'id':"dajnjknsdk",'branch': 'all','degree': 'btech','doc_text': ['Please type a longer query'],'search_tags': ['academics', 'regulations', 'rules', 'btech'],'title': 'ORDINANCES FOR BTECH PROGRAM academics regulations rules btech','title_orig': 'ORDINANCES FOR BTECH PROGRAM','url': [""]}
        
       
        for q in all_query_types:
            f.write('\n--------\n')
            f.write(q+'\n')
            try:
                result = self.solr.search(q,fq=filter_queries,fl='*,score')
            except:
                result = [flagres]
            for j in result:
                try:
                    f.write(str(j)+'\n')
                except UnicodeEncodeError:
                    print('ERROR')
                    f.write(str(str(j).encode('utf-8'))+'\n')
                f.write('\n')
            self.results.append(result)
        return self.results
        


def getBertResults(question,final_res):
        # E:\berttrained\bert-master
    global bertpath
    import os
    os.chdir(bertpath)
    # !dir

    contextdict ={}


    # strcontex = ''.join(resdict[1]['title_orig']) + " "+ ''.join(resdict[1]['doc_text'])

    strcontex = ''.join(final_res['title_orig']) + " "+ ''.join(final_res['doc_text'])

    ques = question

    print(ques)
    print(strcontex)

    strcontex = strcontex.replace("'","")
    # print(strcontex)

    strtitle="IIITD"




    contextdict["context"] =strcontex
    ansdict ={}
    ansdict["answers"] = [{'answer_start': 1, 'text': ''}, {'answer_start': 1, 'text': ''},{'answer_start': 1, 'text': ''}] 

                           
    ansdict["id"] ='1'
    ansdict["question"]=ques

    ansdict


    newdict={}
    newdict["qas"] =[ansdict]

    contextdict["qas"] = newdict["qas"]
    contextdict

    maindict ={}
    maindict["title"] = strtitle
    maindict["paragraphs"] = [contextdict]

    maindict

    finmaindict={}
    finmaindict["data"]=[maindict]
    finmaindict

    import json
    with open('questest.json','w') as json_data:
        json.dump(finmaindict,json_data)
        
    print("****exported")

    import tensorflow as tf
    # Important - Clear flags before running bert
    def del_all_flags(FLAGS):
        # Function to Clear flags before running bert
        flags_dict = FLAGS._flags()    
        keys_list = [keys for keys in flags_dict]    
        for keys in keys_list:
            FLAGS.__delattr__(keys)

    # Calling the clear Flags to clear tensorflow flags before calling Bert
    del_all_flags(tf.flags.FLAGS)

    # Running Bert for predictions
    import subprocess
    val = "python run_squad.py  --vocab_file=vocab.txt --bert_config_file=bert_config.json --init_checkpoint=out -do_predict=True --predict_file=questest.json --output_dir=outcheck"
    subprocess.call(val, shell=True)



    import json
    import os

    predpath = "outcheck/"+"predictions.json"
    preddict={}
    with open(predpath) as json_data:
        preddict = json.load(json_data)
    print(preddict['1'])


    answer = preddict['1']
    answerurl = final_res['url'][0]

    return answer,answerurl


def getQueryResult(question):
    result="Default result"

    rscount=0
    
    resdict ={}
    result1 = getResults().retrieve_results(question)[0]
    result_from_q1 = []
    for a in result1:
        rscount+=1
        print(" \nResult %s :- \n "%(rscount))
        result_from_q1.append(a)
        resdict[rscount]=a

        print(a)


    print("==============================")

    rscount=0
    result2 = getResults().retrieve_results(question)[1]
    result_from_q2 = []
    for a in result2:
    # for a in getResults().retrieve_results(qarr[itcount])[2]:
        rscount+=1
        result_from_q2.append(a)
        print(" \nResult %s :-\n "%(rscount))
        print(a)


    top_results_1 = result_from_q1[0:5]
    top_results_2 = result_from_q2[0:5]

    final_results = []

    for a in range(len(top_results_1)):
       
       for b in range(len(top_results_2)):
           
           if top_results_1[a]['id'] == top_results_2[b]['id']:
                final_results.append([top_results_1[a],top_results_2[b]])

    #print(len(final_results))
    #print(final_results)
    import numpy as np


    final_res=""

    if len(final_results) == 1:
        final_res=final_results[0][0]
        print(final_results[0][0])

    elif len(final_results)>1:
       
        final_scores = []
        for i in range(len(final_results)):
            final_scores.append(final_results[i][0]['score']+final_results[i][1]['score'])

        index = np.argmax(final_scores)
        final_res=final_results[index][0]
        print(final_results[index][0])

    else:
        final_res=top_results_1[0]
    #     if top_results_1[0]['score']>top_results_2[0]['score']:
    #         final_res=top_results_1[0]
    #         print(top_results_1[0])
    #     else:
    #         final_res=top_results_2[0]
    #         print(top_results_2[0])


    result =  final_res['doc_text'][0] + '    \n    ' + "Source: "+final_res['url'][0]

    # Uncomment below two lines to enable bert
    # answer, ansurl = getBertResults(question,final_res)
    # result =  answer + '    \n    ' + "Source: "+ansurl


    return result



app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def samplefunction():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        
        if 'form1' in request.form:
            global human1            
            human1 = request.form['human']
            # if human1 in greetIn:
            global bot
            bot = getQueryResult(human1)
            return render_template('index.html', bot=bot)

        if 'form2' in request.form:
            value = request.form['tip3']
            rating=False
            if value=='1':
                rating=True

            valcheck = bot

            if bot=="":
                rating="Please ask question first"
            else:
                import pandas
                # 'question':0,'answer':1,'feedback':2
                d = {'0':[human1],'1':[valcheck],'2':[rating]}
                df1 = pandas.DataFrame(d)
                with open('feedback.csv', 'a') as f:
                    (df1).to_csv(f, header=False,index=False)
           
            bot=""            

            return render_template('index.html',rating=rating,bot=valcheck)

            

            # else:
            #     render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)