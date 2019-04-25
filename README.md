# qachatbot
Question Answering chatbot created for IIITD site. It uses Solr for indexing the data and uses BERT trained model optionally for answering factoid questions. Scraping codes for scraping the data from iiitd website are included in scrape directory . BERT trained model (trained on SQUAD Dataset) is not included in the repository due to its huge size (~ 7 GB)

# Files Description



Scraping:- 

1- website_scraper.py - scrapes links from iiitd website_scraper . Generates a pickle file with name all_iiitd_links.pickle file
2- collect_data_from_links.py - Reads the file all_iiitd_links.pickle and creates a folder for scraped webpages. For each webpage a text file is created inside the scraped folder. Also generates  "all_file_headings_mapping.pickle" which contains mapping between text file and the headings in that text file
3- Preprocess_matchHeadings.py -  Reads "all_file_headings_mapping.pickle" file and scraped folder for all scraped webpages and generates a json file corresponding to each input file in the out folder which contains the heading and text mappings
4- read_headings_text.py - Reads all the json files in the out directory and creates degree tags corresponding to each file based on the webpage urls . Finally generates the file 'all_final_documents.pickle' which will be used for Indexing


Indexing : -
Solr_index_website_data_lxml.py - reads 'all_final_documents.pickle' and indexes them to Solr.
querygen.py -  "Retrives the Solr result for some sample input queries from "qatest_pairs_new_factoids.csv". BERT module is also included in the file to answer factoid questions.

Web Server
web_connect.py - contains the code written using flask to host a webpage and questions and retrieve answers from Solr and BERT. (includes the functions of querygen.py)

File to run - web_connect.py 
