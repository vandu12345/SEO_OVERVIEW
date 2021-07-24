from django.shortcuts import render
import numpy as np
from scipy import stats
from scipy.stats import norm
import re,urllib,requests,math
from bs4 import BeautifulSoup
import math,statistics
import matplotlib.pyplot as plt
from urllib. parse import urlparse
from .utils import get_plot
from .utils1 import get_plot1
from .utils2 import get_plot2
from collections import Counter
import io
def home(request):
     return render(request,"index.html")
# Metric_1
def test(img_url,domain,protocol,url):
    try:
        if img_url.startswith("http"):
            site = img_url
        elif img_url.startswith("//"):
            site = protocol+":"+img_url
        elif img_url.startswith("/"):
            site = protocol+"://"+domain+img_url
        elif img_url.startswith("#"):
            site = url+img_url    
        return site
    except:
        return ""
def images_computation(request):
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"image_metric1.html",{'url':None})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        t = 0    
        count = 0
        Max = 0
        Min = float("inf")
        list1 = list()
        Sum = 0
        domain = urlparse(url). netloc 
        protocol = url.split(":")[0]
        x1 = list()
        y1 = list()
        img_list = list()

        for img in soup.find_all("img"):
            try:
                img_url = img.attrs.get("src")
                sit = test(img_url,domain,protocol,url)
                if len(sit)!=0:
                    img_list.append(sit)
                    file = urllib.request.urlopen(sit)
                    size = file.headers.get("content-length")
                    length = int(size)/1000
                    Max = max(Max,length)
                    Min = min(Min,length)
                    Sum+=length
                    count+=1
                    list1.append(length)     
            except KeyError:
                pass
            except:
                t+=1

        for img in soup.find_all("img"):
            try:
                img_url = img.attrs.get("data-a-hires")
                sit = test(img_url,domain,protocol,url)
                
                if len(sit)!=0:
                    img_list.append(sit)  
                    file = urllib.request.urlopen(sit)
                    size = file.headers.get("content-length")
                    length = int(size)/1000
                    Max = max(Max,length)
                    Min = min(Min,length)
                    Sum+=length
                    count+=1
                    list1.append(length)
            except KeyError:
                pass
            except:
                t+=1
     
        for img1 in soup.find_all("img"):
            try:
                srcset_list = img1['srcset'].strip().split(",")
                for i in range(0,len(srcset_list)):
                    img = srcset_list[i].strip().split(" ")[0]
                    img_url = img
                    sit = test(img_url,domain,protocol,url)
                    if len(sit)!=0:
                        img_list.append(sit)
                        file = urllib.request.urlopen(sit)
                        size = file.headers.get("content-length")
                        length = int(size)/1000
                        Max = max(Max,length)
                        Min = min(Min,length)
                        Sum+=length
                        count+=1
                        list1.append(length)
            except KeyError:
                    pass
            except:
                    t+=1
        if count>0:
            mean = round(Sum/(count-t),2)
            c1 =min(100,mean)
            c = 0
            sd = 0
            y = 0
            for i in list1:
                sd = sd+(i-mean)**2
                if(i>c1):
                    x = (Max-i)/(Max-c1)
                    y+=x
                elif(i<c1):
                    x = (i-Min)/(c1-Min)
                    y+=x
                else:
                    x = 1
                    y+=x
                c+=1
                x1.append(i)
                y1.append(x)
            sd1 = round(math.sqrt(sd/(count-t)))
            chart = get_plot(x1,y1)
            overrall_performance  = y/c
            # list3 = [i+1 for i in range(len(img_list)) ]
            # zip1 = zip(list3,img_list)
            return render(request,'image_metric1.html',{'url':url,'count':count,'sum':round(Sum,2),
                            'max':round(Max,2),'min':round(Min,2),'average':round(mean,2),'sd':round(sd1,2),'overall':round(y/c,2),'t':t,'img_list':img_list,'chart':chart})
        else:
            # print("No Image Found")
            return render(request,'image_metric1.html',{'url':url,'img_list':img_list})
            # 

# Metric 2
def paragraph_computation_metric2(request):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"paragraph_metric2.html",{'url':None})
    else:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        count = 0
        Max = 0
        Min = float("inf")
        Sum = 0
        list1 = list()
        x1 = list()
        y1 = list()
        for par in soup.find_all('p'):
            k = len(par.text.split(" "))
            Max = max(Max,k)
            Min = min(Min,k)
            Sum+=k
            count+=1
            list1.append(k)
        if count>0:
            mean = round(Sum/count)
            sd = 0
            c1 = min(mean,100)
            c = 0
            y = 0
            for i in list1:
                sd = sd+(i-mean)**2
                if(i>c1):
                    x = (Max-i)/(Max-c1)
                    y+=x
                elif(i<c1):
                    x = (i-Min)/(c1-Min)
                    y+=x
                else:
                    x = 1
                    y+=x
                c+=1
                x1.append(i)
                y1.append(x)
            chart1 = get_plot1(x1,y1)
            sd1 = 0.0
            sd1 = round(math.sqrt(sd/(count)))
            return render(request,'paragraph_metric2.html',{'url':url,'count':count,'sum':round(Sum,2),
                            'max':round(Max,2),'min':round(Min,2),'average':round(mean,2),'sd':round(sd1,2),'overall':round(y/c,2),'chart1':chart1})
        else:
            return render(request,'paragraph_metric2.html',{'url':url,'count':count})
        
# Metric 3
def link_calculator_metric3(request):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    count = 0
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"link_metric3.html",{'url':None,'count':0})
    else:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        domain = urlparse(url). netloc 
        protocol = url.split(":")[0]
        internal_link = list()
        external_link = list()
        count = 0
        for link in soup.find_all('a',href=True):

            count+=1
            try:
                if link['href'].startswith("http"):
                    ur = link['href']
                    if re.search(domain,link['href']):
                        internal_link.append(ur)
                    else:
                        external_link.append(ur)
                elif link['href'].startswith("//"):
                    ur = protocol+":"+link['href']
                    if re.search(domain,ur):
                        internal_link.append(ur)
                    else:
                        external_link.append(ur)
                elif link['href'].startswith("/"):
                    ur = protocol+"://"+domain+link["href"]
                    internal_link.append(ur)
                elif link['href'].startswith("#"):
                    ur = url+"/"+link['href']
                    internal_link.append(ur)
                else:
                    ur = protocol+"://"+domain+"/"+url
                    internal_link.append(ur)
            except:
                pass
        # print(len(internal_link))
        # print(len(external_link))
        # print(count)
        len1 = len(internal_link)
        len2 = len(external_link)


        if count>0:
            data = [len(internal_link),len(external_link),count]
            entry = ['Internal Links', 'External Links','Total Links']
            chart2 = get_plot2(data,entry,'Links')
            return render(request,'link_metric3.html',{'url':url,'count':count,'internal':len1,'external':len2,'chart2':chart2})

                

        else:
            return render(request,"link_metric3.html",{'url':url,"count":0})


# Metric 4

def donofollow_calculator_metric4(request):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    count = 0
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"donofollow_metric4.html",{'url':None,'count':0})
    else:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        domain = urlparse(url). netloc 
        protocol = url.split(":")[0]
        dofollow_link = list()
        nofollow_link = list()
        count = 0
        for link in soup.find_all('a',href=True):
            count+=1
            try:

                if link['rel'][0]=="nofollow":
                    nofollow_link.append(link['href'])
                else:
                    dofollow_link.append(link['href'])
            except:
                dofollow_link.append(link['href'])

                

        # print(len(internal_link))
        # print(len(external_link))
        len1 = len(nofollow_link)
        len2 = len(dofollow_link)


        if count>0:
            data = [len(nofollow_link),len(dofollow_link),count]
            entry = ['NoFollow Links', 'DoFollow Links','Total Links']
            chart = get_plot2(data,entry,"Do-No-Follow")
            return render(request,'donofollow_metric4.html',{'url':url,'count':count,'nofollow':len1,'dofollow':len2,'chart':chart})

                

        else:
            return render(request,"donofollow_metric4.html",{'url':url,"count":0})

# Matric 5
def url_checker(url_c,protocol,domain,url):
    if url_c.startswith("http"):
        ur = url_c
    elif url_c.startswith("//"):
        ur = protocol+":"+url_c
    elif url_c.startswith("/"):
        ur = protocol+"://"+domain+url_c
    elif url.startswith("#"):
        ur = url+"/"+url_c
    else:
        ur = protocol+"://"+domain+"/"+url_c
    return ur
def brokenlink_metric5(request):
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"brokrnlink_metric5.html",{'url':None,'count':0})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        domain = urlparse(url). netloc 
        protocol = url.split(":")[0]
        list1 = list()
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        for link in soup.find_all('a',href=True):
            try:
                result = url_checker(link['href'],protocol,domain,url)
                response = requests.get(result,headers=headers)
                status= response.status_code
                if status==404:
                    list1.append(result)
            except:
                pass                          
        # for link in soup.find_all('link',href=True):
        #     try:
        #         result = url_checker(link['href'],protocol,domain,url)
        #         response= requests.get(result,headers=headers)
        #         status= response.status_code
        #         if status==404:
        #             list1.append(result)
        #     except:
        #         pass
     
        return render(request,'brokrnlink_metric5.html',{'url':url,'list1':list1})

# Metric 6
def word_density_checker_metric6(request):
    dict1 = dict()
    url = request.POST.get('name')
    if url==None or url=='':
        return render(request,"word_density_metric6.html",{'url':None,'dict1':dict1})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        x = re.findall('[A-Za-z0-9]+', text)
        list1 = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves","what",
    "which","who","whom","this","that","these","those","am","is","are","was","were","be",
    "been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or",
    "because","as","until","while","of","at","by","for","with","about","against","between","into","through",
    "during","before","after","above","below","to","from","up","down","in","out","on","off","over","under",
    "again","further","then","once","here","there","when","where","why","how","all","any","both","each","few",
    "more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t"
    ,"can","will","just","don","should","now",'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
    'q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R'
    ,'S','T','U','V','W','X','Y','Z']

        word_list = dict()
        dict1 = dict()
        if len(x):
            for word in x:
                if word in word_list:
                    if word.lower() in list1:
                        pass
                    else:
                        word_list[word] += 1
                else:
                    if word.lower() in list1:
                        pass
                    else:
                        word_list.update({word: 1})
            length = len(word_list)
            dict1 = dict(Counter(word_list).most_common(10))
            dict2 = dict1.items()
            return render(request,"word_density_metric6.html",{'url':url,'dict1':dict1,'dict2':dict2,'length':length})
        else:
            return render(request,"word_density_metric6.html",{'url':'url','dict1':dict1})


# Metric 7
def meta_description_metric7(request):
    url = request.POST.get('name')
    list1 = list()
    if url==None or url=='':
        return render(request,"meta_description_metric7.html",{'url':None})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        header = req.headers
        header1 = header.items()

        
        metas = soup.find_all('meta')
        for meta in metas:
            try:
                if 'name' in meta.attrs and meta.attrs['name'] == 'description':
                    list1.append(meta.attrs['content'])
            except:
                pass
        # print(list1)
        # print(len(list1))
        if len(list1):
            return render(request,'meta_description_metric7.html',{'url':url,'list1':list1})
        else:
            return render(request,'meta_description_metric7.html',{'url':url,'list1':list1})

# Metric 8
def HTTP_HEADER_description_metric8(request):
    url = request.POST.get('name')
    list1 = list()
    if url==None or url=='':
        return render(request,"header_description_metric8.html",{'url':None})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        header = req.headers
        header1 = header.items()
        return render(request,"header_description_metric8.html",{'url':url,'header':header,'header1':header1})

# Metric 9

def canonical_tag_metric9(request):
    url = request.POST.get('name')
    list1 = list()
    if url==None or url=='':
        return render(request,"canonical_tag_metric9.html",{'url':None})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        for link in soup.find_all('link',href=True):
            try:
                if link['rel'][0] == 'canonical':
                    # print(link['href'])
                    list1.append(link['href'])
                # print(link['rel'][0])
            except:
                pass
        # print(list1)
        return render(request,"canonical_tag_metric9.html",{'url':url,'list1':list1})

# Metric 10
def robotstext_metric10(request):
    url = request.POST.get('name')
    list1 = list()
    if url==None or url=='':
        return render(request,"robots_text_metric10.html",{'url':None})
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        if url.endswith("/"):
            path = url
        else:
            path = url+"/"
        path = path + "robots.txt"
        req = requests.get(path, headers=headers)
        soup = BeautifulSoup(req.text,'html.parser')
        status= int(req.status_code/100)
        return render(request,'robots_text_metric10.html',{'url':url,'path':path,'status':status})



# SUKANTA METRIC
# Metric_1
# def status_code_metric1(request):
#     url = request.POST.get('name')
#     string = str()
#     # respose = ""
#     status = ""
#     try:
#         response= requests.get(url)
#         status = response.status_code
#         status1 = int(status/100)
#         if status1==1:
#             string = f"{status}:This lets us know that the request was recieved"
#         elif status1==2:
#             string = f"{status}:This shows that the request was successful"
#         elif status1==3:
#             string = f"{status}:This is for redirects (temporary and permanent)"
#         elif status1==4:
#             string = f"{status}:Client errors"
#         elif status1==5:
#             string = f"{status}:Client errors"
#         else:
#             string = "Any other Problem Occured"
#     except:
#             if url==None:
#                 string = "Enter A URL"
#             else:
#                 string = "Enter Valid URL"

    
#     return render(request,'status_code_metric1.html',{'string':string})

# # Metric 2
# def social_link(request):
#     string = str()
#     try:
#         url = request.POST.get('name')
#         list1 = list()
#         list2 = list()
#         zip1 = zip(list1,list2)
#         if url ==None:
#             return render(request,"social_link_metric2.html",{'zip':zip1,'url':url})
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # print(soup)
#         flag1 = 0
#         flag2 = 0
#         flag3 = 0
#         flag4 = 0
#         flag5 = 0
#         list1 = list()
#         list2 = list()
        
#         str1 = ""
#         for social in soup.find_all('a',href=True):
#             if re.search("youtube",social['href']) and flag1==0:
#                 flag1 = 1
#                 list2.append("YouTube Present")
#                 list1.append(social['href'])
#             elif re.search("facebook",social['href']) and flag2==0:
#                 flag2 = 1
#                 list2.append("FaceBook Present")
#                 list1.append(social['href'])
#             elif re.search("instagram",social['href']) and flag3==0:
#                 flag3 = 1
#                 list2.append("Instagram Present")
#                 list1.append(social['href'])
#             elif re.search("twitter",social['href']) and flag4==0:
#                 flag4 = 1
#                 list2.append("Twitter Present")
#                 list1.append(social['href'])
#             elif  re.search("linkedin",social['href']) and flag5==0:
#                 flag5 = 1
#                 list2.append("LinkedIn Present")
#                 list1.append(social['href'])
#             zip1 = zip(list1,list2)
#     except:
#         pass
#     return render(request,"social_link_metric2.html",{'zip':zip1,'url':url})



