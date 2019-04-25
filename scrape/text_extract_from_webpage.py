from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request,re

#
def tag_visible(element):
#    print(element.parent.parent.name)
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]','footer']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')    
    [s.extract() for s in soup('style')]
    # print (soup)
    texts = soup.findAll('div',attrs={'id':'primary'})
    main_content = texts[0].text
#    print('main content = '+str(main_content))
    main_content = re.sub(r"<!(.|\s|\n)*?>", "", main_content)
#    print(main_content)
    
    
    t= [s.extract() for s in soup(['h1','h2','h3','h4','h5','h6','strong','h7','h8'])]
    headlist = [a.text for a in t]
#    print(headlist)
    
    return main_content,headlist

#html = urllib.request.urlopen('http://iiitd.ac.in/admission/mtech/2017/cse-ece-details').read()
#link_text = text_from_html(html)
#print(link_text)
#
#soup = BeautifulSoup(html,'html.parser')
#x = soup.find_all('div',{'class':'content'})
##visible_text = x.text
#print('x = '+str(x[0].text))
##print('visible text = '+str(visible_text))