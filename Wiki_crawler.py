import requests
from bs4 import BeautifulSoup
import random
import time 
import csv

GlobalNodeCount = 0
count = 0
queue = []
arr = []
dic1 = dict()


def scrapeWikiArticle(url,count,queue,parent,GlobalNodeCount,arr,dic1,flag):
    dic = dict()
    count += 1
    if(count%20==0):
        time.sleep(1)
    response = requests.get(
        url=url,)
    print(response)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")
    allLinks = soup.find(id="bodyContent").find_all("a")
    linkToScrape = 0
    s = 0
    for link in allLinks:
        if(link.has_key('href')):
            st = str("https://en.wikipedia.org" +link["href"])
            if link['href'].find("/wiki/") == -1: 
                continue
            elif("en.wikipedia.orghttps://" in st):
                st = str(link['href'])
                print("====Continue=====",st)                
                continue
            else:
                st = str(link['href'])
                if "https://en.wikipedia.org" not in st:
                    linkToScrape = link
                    st = str("https://en.wikipedia.org" + linkToScrape['href'])
                else:
                    print("yeahh",GlobalNodeCount,link['href'])
                    continue
                    st = str(linkToScrape['href'])
                    print("st==>",st)    
                if st in dic:
                    continue
                    print("YESS")
                else:
                    if st in dic1:
                        if flag == True:
                            queue.append(st+"\t"+str(parent)+"\t"+str(dic1[st]))
                        print("in dic  1")
                        if st in arr:
                            print("----------present---------")
                        arr.append([st,str(parent),str(dic1[st])])
                        dic[st] = parent
                    
                    else:
                        GlobalNodeCount +=1
                        if flag == True:
                            queue.append(st+"\t"+str(parent)+"\t"+str(GlobalNodeCount))
                        if st in arr:
                            print("----------present---------")
                        arr.append([st,str(parent),str(GlobalNodeCount)])
                        dic[st] = parent
                        dic1[st] = GlobalNodeCount
        s +=1
        if '/wiki/' in link:
            print("---------YES-------")

            if link['href'].find("/wiki/") == -1: 
                continue
    print("size of array",len(arr),len(queue))
    return GlobalNodeCount, int(len(queue))   # After certain iteration enque will be stopped and only deque and capturing the node is performed 
        #break
    #
    
    #scrapeWikiArticle("https://en.wikipedia.org" + linkToScrape['href'],count+s)
def Url_BFS_Collector(url_Site,GlobalNodeCount,queue,arr,count,dic1,depth):
    qsize = 1
    flag = True 
    urls = input("Enter the URL with http\n")
    depth = int(input("Enter the Levels to be traversed\n"))
    #urls = 'https://en.wikipedia.or/www.wikidata.org/wiki/Q286890#identifiers'
    #print(uri_exists(urls))
    urls = url_Site
    queue.append(urls+"\t"+str(0)+"\t"+str(GlobalNodeCount))
    arr.append([urls,'0',str(GlobalNodeCount)])
    dic1[urls] = 0
    file1 = open('WikiNode_Covid-19_10.csv','w+',newline="",encoding='utf-8')
    with file1:
        header = ['Link', 'ParentNode', 'NameNode']
        writer = csv.DictWriter(file1, fieldnames = header)
        writer.writeheader()
        file1.close()
    while qsize > 0: 
        if depth < 0 : 
            flag = False
        depth -= 1
        st = queue[0]
        st,pnode,node = st.split("\t")
        print("After split   ",node,st,pnode)
        print(len(queue),queue[0][2])
        queue.pop(0)    
        #caller
        urls = st
        GlobalNodeCount, arrSize =  scrapeWikiArticle(urls,count,queue,node,GlobalNodeCount,arr,dic1,flag)
        qsize = arrSize  ##main step for depth capturing 
        print("queue-->",qsize) #dynamic iteration count
        #to store in file
        file = open('WikiNode_Covid-19_10.csv', 'a+', newline ='',encoding='utf-8') 
    # writing the data into the file
        data = arr
        with file:    
            write = csv.writer(file)
            write.writerows(data)
        file.close()
        arr = []

#Driver code 
if __name__ == "__main__":
    Url_BFS_Collector('https://en.wikipedia.org/wiki/COVID-19',GlobalNodeCount,queue,arr,count,dic1,4)