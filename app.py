import json
import requests
import time
import hashlib
import urllib.parse
import os
import urllib3
import linecache
import sys
import shutil
import base64
from bs4 import BeautifulSoup as s
import string
import os
import pymongo
import re
import random
import timeit
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import timedelta
import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random,string

#point users
client2user = pymongo.MongoClient("mongodb+srv://aa:bb@cluster0.kq7ic.mongodb.net/a?retryWrites=true&w=majority")
mydb= client2user["a"]

mycol = mydb["users"]
allgive="0"
list = ["655049808","1150981021","1137847054"]
listgrop = ["655049808","1150981021","-1001465035595","-542619016"]
payload={}

TOKEN = "1831155904:AAHdieMeenLc3Ls6QcfR1xLlvczaXybCNT0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
hh1 = ''' <html>
                                                                                                             <head> 
                                                                                                            <meta charset="utf-8"/>        
                                                                                                             <meta name="viewport" content="width=device-width, initial-scale=1.0" /> 
                                                                                                                    </head>



                                                                                                                            <body    '''

hh2 = '''</body>
                                                                                                         </html>   '''

class ParseMode(object):
    MARKDOWN = 'Markdown'
    MARKDOWN_V2 = 'MarkdownV2'
    HTML = 'HTML'

def get_url(url):
    try:
        response = requests.get(url)
        content = response.content.decode("utf-8")
        return (content)
    except:
        pass

def post_url(urll , data, file=None):
    try:
        if file is not None:
            response = requests.post(urll, files=file , data=data)
            return json.loads(response.content.decode())
        else:
            response = requests.post(urll , data=data)
            return json.loads(response.content.decode())
    except:
        pass

def get_updates(offset=None):
    try:
        url = URL + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        content = get_url(url)
        js = json.loads(content)
        return js
    except:
        pass

def get_last_update_id(updates):
    try:
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)
    except:
        pass



#check is url is chegg or not


def get_id(qu_url):
    qu_url = qu_url.split('?')[0]
    qu_url = qu_url.split('&')[0]
    qu_url = qu_url.split('#')[0]
    qu_url = qu_url.split('%')[0]
    qid = ''
    ty = ''
    if ('solution' in qu_url) and ('chapter' in qu_url):  # and ('problem' in qu_url):
        if '-exc' in qu_url:
            exc = qu_url.rindex('-exc')
            if exc > 100:
                qu_url = qu_url[:exc]
            else:
                pass
        qid = qu_url[qu_url.rindex('help/') + 5:]
        ty = 't'
    elif '-q' in qu_url:
        try:
            qid = qu_url[qu_url.rindex('-q'):]
            ty = 'q'
        except Exception as e:
            if 'not found' in str(e):
                return 'Please make sure the link is correct 🤔😕'

    else:
        return 'Please make sure the link is correct 🤔😕'

    return [qid, ty]

#

def zro(repy_id):
    try:
        mydoc2 = mycol.find_one({ str(repy_id):str(repy_id)})
        print(mydoc2)
        print("is sub grube")
        g=[mydoc2]
        oldadd=int(g[0]['point'])
        newadd=int(g[0]['point'])
        clc=oldadd-newadd
        print("is clc sub  :"+str(clc))
        mydict77 = {  str(repy_id):str(repy_id), "point": str(clc) }
        mydict4 = { "$set":mydict77}
        mycol.update_one(mydoc2, mydict4)
        return str(clc)
    except:
        pass

#sub grupe
def sub_point(user_id):
    try:
        mydoc2 = mycol.find_one({ str(user_id):str(user_id)})
        print(mydoc2)
        print("is sub ")
        g=[mydoc2]
        oldadd=int(g[0]['point'])
        newadd=int("1")
        clc=oldadd-newadd
        print("is clc sub  :"+str(clc))
        mydict77 = {  str(user_id):str(user_id), "point": str(clc) }
        mydict4 = { "$set":mydict77}
        mycol.update_one(mydoc2, mydict4)
        return str(clc)
    except:
        pass



#add points
def add_point(repy_id ,add):
    try:
        #print("id group points :"+str(chat_id)+"and add point :"+str(add_point))
        mydoc2 = mycol.find_one({ str(repy_id):str(repy_id)})
        print(mydoc2)
        if  str(repy_id)  not in str(mydoc2):
            mydict = {  str(repy_id):str(repy_id), "point": str(add) }
            x = mycol.insert_one(mydict)
            return str(add)
        else:
            print("is old grupe")
            g=[mydoc2]
            oldadd=int(g[0]['point'])
            newadd=int(add)
            clc=oldadd+newadd
            print("is clc :"+str(clc))
            mydict77 = {  str(repy_id):str(repy_id), "point": str(clc) }
            mydict4 = { "$set":mydict77}
            mycol.update_one(mydoc2, mydict4)
            return str(clc)
    except:
        pass



#chuck point
def get_point(user_id):
    try:
        print("id  points :"+str(user_id))
        mydoc2 = mycol.find_one({ str(user_id):str(user_id)})
        print(mydoc2)
        if  str(user_id)  not in str(mydoc2):
            mydict = {  str(user_id):str(user_id), "point": allgive }
            x = mycol.insert_one(mydict)
            return allgive
        else:
            g=[mydoc2]
            print("user is old in file time :"+str(g[0]['point']))
            return str(g[0]['point'])
    except:
        pass



def Check(update):
    try:
        if not 'callback_query' in str(update) and not 'channel_post' in str(update):
            
            user_id = update["message"]["from"]["id"]
            chat_id = update["message"]["chat"]["id"]
            chat_type= update["message"]["chat"]["type"]
            message_text = update['message']['text']
            try:
                first_name = update["message"]["from"]["first_name"]
            except:
                first_name = ''
            try:
                last_name = update["message"]["from"]["last_name"]
            except:
                last_name = ''
            try:
                username = update["message"]["from"]["username"]
            except:
                username = ''
            
            message_id = update["message"]["message_id"]
            if message_text=='/get':
                pi=get_point(user_id)
                send_message('Remaining  chances:'+str(pi),chat_id,message_id)
            elif message_text.startswith('/add-') and update["message"]['reply_to_message'] and str(user_id) in list:
                repy_id = update["message"]['reply_to_message']['from']['id']
                repy_msg_id= update["message"]['reply_to_message']['message_id']
                string = str(message_text)
                pattern = '\d+'
                result = re.findall(pattern, string)
                print(result)
                add=str(result[0])
                asd=add_point(repy_id ,add)
                send_message('chances increased:'+str(asd),chat_id,repy_msg_id)
            elif message_text=="/zero"  and update["message"]['reply_to_message'] and str(user_id) in list:
                repy_id = update["message"]['reply_to_message']['from']['id']
                zz=zro(repy_id)
                print(str(zz))
                send_message("Total points have been deleted",chat_id,message_id)
            elif message_text=="/id" :
                send_message("id :"+str(user_id)+"\n"+str(chat_id),chat_id,message_id)
            elif message_text=="/info"  :
                send_message( 'The number of database  :'+str(mycol.count()) , chat_id, message_id)

              

            elif 'text' in update['message'].keys():
                if message_text=='/start':
                    send_message('بوت يعمل بنجاح',chat_id)
                    return True


                if 'entities' in update['message'].keys():
                    qu_url = ''
                    for entiti in update['message']['entities']:
                        if (entiti['type']=='url' or entiti['type']=='text_link'):
                            offset = entiti['offset']
                            length = entiti['length']
                            qu_url = message_text[offset: offset + length]
                    
                    if  qu_url and str(chat_id) in listgrop:
                        print("Question : ",qu_url)
                        cc=get_id(qu_url)
                        print(cc)
                        time.sleep(10)
                        if "Please make sure the link is correct" in  cc:
                            print("url is not chegg")
                        elif cc[0].startswith('-q'):
                            print("url is from Q and A")
                            pi=get_point(user_id)
                            print(pi)
                            ress=int(pi)
                            if ress==0 or ress<0:
                                send_message('تم انتهاء نقاط \npoints expired\n\nMore points contact ',chat_id,message_id)
                            else:
                                resl =send_req(qu_url)
                                se = str(resl)
                                if se.startswith('here is your answer'):
                                    su=sub_point(user_id)
                                    i = open('./Answer.html', 'rb')
                                    url876 = ("https://api.telegram.org/bot"+TOKEN+"/sendDocument?chat_id="+str(chat_id)+'&caption='+str('This is your answer 🌚'+str()+'\n✅ Remaining points:'+str(su)+""+'&reply_to_message_id='+str(message_id))+'&parse_mode=Markdown')
                                    url_txt = requests.post(url876, files={'document': i})
                                else:
                                    send_message(resl, chat_id, message_id)
                        else:
                            print("now l can get answer")
                            pi=get_point(user_id)
                            print(pi)
                            ress=int(pi)
                            if ress==0 or ress<0:
                                send_message('تم انتهاء نقاط \npoints expired\n\nMore points contact ',chat_id,message_id)
                            else:
                                print("l am sore but not answer")
                                resl = ans_book(qu_url)
                                se = str(resl)
                                if se.startswith('here is your answer'):
                                    su=sub_point(user_id)
                                    i = open('./Answer.html', 'rb')
                                    url876 = ("https://api.telegram.org/bot"+TOKEN+"/sendDocument?chat_id="+str(chat_id)+'&caption='+str('This is your answer 🌚'+str()+'\n✅ Remaining points:'+str(su)+""+'&reply_to_message_id='+str(message_id))+'&parse_mode=Markdown')
                                    url_txt = requests.post(url876, files={'document': i})
                                else:
                                    send_message(resl, chat_id, message_id)

    except:
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print('Error EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    return True





chuk = {
         "User-Agent":"PostmanRuntime/7.28.0",
        "Accept": "*/*",
 "Cache-Control":"no-cache",
 "Postman-Token": "04d2a2c9-63ab-43bf-bfcb-e7f38a92beb4",
 "Host":"www.chegg.com",
 "Accept-Encoding":"gzip, deflate, br",
 "Connection": "keep-alive",
 "Cookie": "C=0;CSessionID=6f7a55cd-cf95-485c-ba1c-e3b122cd1d7b;O=0; PHPSESSID=837161d45166559ee95dfa1bdde1e371; U=0; V=ba35049ebce8516446423128043519ce6074891676d8c5.51631027; exp=A184A%7CA311C%7CA803B%7CC024A%7CA560B; expkey=BEE682351558F2E82EA91564D646A8A1; user_geo_location=%7B%22country_iso_code%22%3A%22US%22%2C%22country_name%22%3A%22United+States%22%2C%22region%22%3A%22VA%22%2C%22region_full%22%3A%22Virginia%22%2C%22city_name%22%3A%22Ashburn%22%2C%22postal_code%22%3A%2220149%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22en-US%22%5D%7D%7D"

}
# ans urls chegg book
def ans_book(qu_url):
    try:
        urk = str(qu_url)
        while True:

            ############
            r = requests.get(str(urk), headers=chuk)
            print(r)
            soup = s(r.content, 'html.parser')
            images4 = soup.find_all("script")
            cc = str(images4)
            zx = cc.find("isbn13")
            print(zx)
            print((cc[zx:(zx + 34)]))
            text = str(soup)
            start = text.find('''chapterData''') + 1
            end = text.find('''chapterMap''')
            cut_text = text[start:end].strip()
            print(cut_text)
            ###############################
            text = str(cut_text)
            start = text.find("problemId") + 1
            end = text.find('''''')
            cut_text3 = text[start:].strip()
            print(cut_text3)
            ####################
            text = str(cut_text)
            start = text.find('''chapterId''') + 1
            end = text.find('''problemData''')
            cut_text2 = text[start:end].strip()
            print(cut_text2)
            if zx == -1:
                continue
            else:
                # import requests
                import json
                import re
                # print((take[x:(x+20)]))
                # print((take[x2:(x2+26)]))
                # print((take[x3:(x3+22)]))
                string = str(cut_text2)
                pattern = '\d+'
                result = re.findall(pattern, string)
                print(result[0])
                z1 = result[0]
                ######
                string = (cc[zx:(zx + 34)])
                pattern = '\d+'
                result = re.findall(pattern, string)
                print(result[1])
                z2 = result[1]
                ##########
                string = str(cut_text3)
                pattern = '\d+'
                result = re.findall(pattern, string)
                print(result[0])
                z3 = result[0]
                ##################
                url = "https://www.chegg.com/study/_ajax/persistquerygraphql"

                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
                    'Accept': 'application/json',
                    'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                    'Referer': urk,
                    'Content-Type': 'application/json',
                    # 'Origin': 'https://www.chegg.com',
                    # 'Connection': 'keep-alive',
                    'Cookie': "C=0; O=0; U=3f6a6afbcb1fa0721634142329e2a47b; V=53ea3d09ffac4987552099cbc650c3f1600572af6bd005.67201889; exp=A184B%7CA311C%7CA803B%7CC024A%7CA560B%7CA259B%7CA294C%7CA207A%7CA735A%7CA209A%7CA212A%7CA239A%7CA110B%7CA270C%7CA448A%7CA360B%7CA935B%7CA890H%7CA278C%7CA966F; expkey=D13857522271B0BE27ADD3A2D010E0C4; usprivacy=1YNY; OptanonConsent=isIABGlobal=false&datestamp=Sat+Jun+12+2021+17%3A09%3A36+GMT%2B0300+(%D8%A7%D9%84%D8%AA%D9%88%D9%82%D9%8A%D8%AA+%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A+%D8%A7%D9%84%D8%B1%D8%B3%D9%85%D9%8A)&version=6.10.0&hosts=&consentId=42e3d1d6-5eb1-4651-a397-7228e2e5bcee&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; _scid=51cbd642-6298-4f9a-8e63-5340c7f5b568; s_ecid=MCMID%7C29037934875219248102115392500229927675; _ga=GA1.2.969290114.1610969786; _sctr=1|1613336400000; LPVID=ZlNmM0ZDg4NTU4YWJjOGMw; _omappvp=YtbBWN9Rej9YSk5amzwlEYQyTNkY6oTNrZIYwl4RF5JVI56dJGs6uCNmIpSG0gvbkyDtbbJAgVYtagiZq0SJiYCFZvZfsBCm; OneTrustWPCCPAGoogleOptOut=false; sbm_mcid=29037934875219248102115392500229927675; _pxvid=d3c11c77-5981-11eb-bafc-0242ac12000d; sbm_sbm_id=0100007F73730560340052BB0268C817; sbm_country=IQ; sbm_dma=0; __gads=ID=c3186b246bf23f05-22271f3b95b90052:T=1610969972:S=ALNI_MapCo18UIZ8skSlOzbQtftyHuJz0Q; sbm_gaid=969290114.1610969786; csrftoken=HHEsWsklgxBaSlQB2Ol8gmn1n47E3Fdi0hbDHEu2x1g79xX8UoaQpBFE9Iip5rh0; al_cell=main-1-control; optimizelyEndUserId=oeu1612370560880r0.845804414318425; _cs_c=1; __CT_Data=gpv=405&ckp=tld&dm=chegg.com&apv_79_www33=405&cpv_79_www33=405&rpv_79_www33=35; _cs_id=80a89d96-4877-abd3-99ac-9b25fd169509.1612370628.121.1622554936.1622554936.1.1646534628095.Lax.0; WRUID=3150646956556611; bc.visitor_token=6762772580509515776; _vid=O5syefnm0OgfgfmYsRF6; DFID=web|O5syefnm0OgfgfmYsRF6; _ym_uid=1612534492191791627; _ym_d=1612534492; chgcsdmtoken=%7B%22user_uuid%22%3A%22e9fe463f-802a-4c69-b181-f5c5ad4305c5%22%2C%22created_date%22%3A%222021-06-12T14%3A04%3A08.522Z%22%2C%22account_sharing_device_management%22%3A1%7D; al_cell=main-1-control; chgcsdetaintoken=1; chgcsastoken=nZ6bB9cr0hHlUqFGqCVcnqbEoLL7iMETmoU19VJp3vxZBhCTAPRjdbGWQc0PiVlCBV0WMY3WfyoAhI1X4SkI5_hZIw0ugq77pMXKCoc1aj-ORRZ5-GUzoyh-WTgcEACv; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%20e9fe463f-802a-4c69-b181-f5c5ad4305c5%2C%20%22created_date%22%20%3D%3E%202021-06-12T14%3A02%3A32.812Z%20%5D; _CT_RS_=Recording; gid=1562908; gidr=MA; forterToken=0f35933ac63146f883ddfdab379135da_1623506529085_5251_dUAL9_13ck; AMCV_3FE7CBC1556605A77F000101%40AdobeOrg=-408604571%7CMCMID%7C29037934875219248102115392500229927675%7CMCIDTS%7C18790%7CMCAID%7CNONE%7CMCOPTOUT-1623514176s%7CNONE%7CvVersion%7C4.6.0; s_pers=%20buFirstVisit%3Dcore%252Ccs%252Cothers%7C1781189904023%3B%20gpv_v6%3Dno%2520value%7C1623508776582%3B; intlPaQExitIntentModal=hide; user_geo_location=%7B%22country_iso_code%22%3A%22IQ%22%2C%22country_name%22%3A%22Iraq%22%2C%22region%22%3A%22DQ%22%2C%22region_full%22%3A%22Dhi+Qar%22%2C%22city_name%22%3A%22Nasiriyah%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ar-IQ%22%5D%7D%7D; AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg=1; _sdsat_cheggUserUUID=e9fe463f-802a-4c69-b181-f5c5ad4305c5; _sdsat_authState=Hard%20Logged%20In; CVID=016059f3-1d47-45e5-ad17-aef3f86d921f; s_sess=%20buVisited%3Dcore%252Ccs%3B%20s_sq%3Dcheggincriovalidation%253D%252526pid%25253Dchegg%2525257Cweb%2525257Ccs%2525257Cqa%2525257Cquestion%25252520page%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.chegg.com%2525252Fstudy%252526ot%25253DA%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D5828ACB275C66C8D-14FB8EC9C943097E%3B%20s_ptc%3D0.00%255E%255E0.00%255E%255E0.00%255E%255E0.00%255E%255E0.79%255E%255E0.00%255E%255E25.91%255E%255E0.37%255E%255E27.08%3B; BIBSESSID=9f041898-ff22-4a0e-a855-8743c276f88c; userRole=mybib; mcid=29037934875219248102115392500229927675; CSID=1623506514181; schoolapi=39d1a707-b142-40d6-b4ba-3f5833b3e904|0.9; PHPSESSID=mjq97vf3bve3dj7ps2dk1r60ve; CSessionID=63c3eb72-5247-4ba1-b9fb-13a29b45d033; id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlOWZlNDYzZi04MDJhLTRjNjktYjE4MS1mNWM1YWQ0MzA1YzUiLCJhdWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImV4cCI6MTYzOTI3NjU5NCwiaWF0IjoxNjIzNTA2NTk0LCJlbWFpbCI6Im5hc2ExODM3NkBnbWFpbC5jb20ifQ.mA2Dy5pFAQWPtUifI4ltkooel7VMmYLab9WQ3UQAHkrIOPBgS4KsIdatVwRZZ2A0RDCx7oynJ1VL5IjkGf2GuCF_7PrfwwTPTno_ULNay8ZCEK67nPj9SHvt36qfgTkihWEnx_GsiVUjiNpmaoriL8HmGzyE8sTlDRO8UcpjlfMt4hsL30m9CYNZYo7KAKV_-Xmm_JiGy-2RrPcX1XBA7tY0pWb4cu_jruD78YasycjwCfShtBNBCKP5M-uto06jBrT2fLrRM7EvwTbeQdcAmjZaspxgFJzwR-FjUx9z4FuU2vScIBT_j3N8WZewNCAmhiKRIp-I-0hesD8F-87PHw; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhUTkU0cWwxNTRxekZieTBBakxDdSJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJOc1lLd0kwbEx1WEFBZDB6cVMwcWVqTlRVcDBvWXVYNiIsImlzcyI6Imh0dHBzOi8vY2hlZ2ctcHJvZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8ZTlmZTQ2M2YtODAyYS00YzY5LWIxODEtZjVjNWFkNDMwNWM1IiwiYXVkIjpbImNoZWdnLW9pZGMiLCJodHRwczovL2NoZWdnLXByb2QudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyMzUwNjU5NCwiZXhwIjoxNjIzNTA4MDM0LCJhenAiOiIzVFpiaGZzWndkZUhiaG9WTXhPdlpHYjM3TWN2YzBvOCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSBvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIn0.Eqk75URWf3SAYme7OXGpNEY7TycnDtqQctfhJ2ZwMqN7T4K3AILsfExSxGEI9cNT8O-IAVzfRHMCKpc4GcknRsTO_WF58Vtme4-4By3hXznpV03v966qnmahZQ0SOQsUNgfBMTrC6lNAzuaSF8cEe7wxAPV36hWuK2PBubcXBEtTGIyfeRqEnv2XHjoGCmTk9DBnJrMiOHkEHat3CSUnbGrUb5iQfETGqXIXBSms6L342P8Fvq6STmDUh16BJNjXeL-CSMs8uveL3LvQd2He7_lkG5Hhsfzn6cwfs0aY9WSTsgknxw-uZeFkwzR7G8O9jaOMmbG46ADR50Nxo8hvBQ; access_token_expires_at=1623508034; refresh_token=ext.a0.t00.v1.MWMKw10fQn4ux_WKexfMW8v9yqEXcrcQiI9V-zQyE12BkGVpAzhh8JM7H-KhMwp1e-BYzTKGFPqtNRLx63kdyko; SU=oIGyKNc1JsJdZaHiCvza7aWSnblCf3yBUuhzEei-UO-9TESKo3uc2I5VWHghRcMJCFU6UNJVlFEuFKvt8_g5BEW3eAz2nd_TJBBJZj4XSjFIfr1oKUuMj3wBDy2A2Mcw; o_id=Rr-VI1F0dZ7jmREAo0RddO_l_OrrVbA51TQ0uzZQJlRzcDpEyjU5BckhDzvp6B_4l7U5Sqrhwcgck5h0MRZbu1POeBmKixnjB0_nXDh8x6lrnGbmBbjEWiipxCsgM5l4; o_key=d21cb48151de933e8e6396f57da4b015; opt-user-profile=53ea3d09ffac4987552099cbc650c3f1600572af6bd005.67201889%252C19944471923%253A19963683656; _gd1623506618645=1; sbm_a_b_test=1-control; sbm_sbm_session_id_2=720da875-d54d-491d-8fe0-e0ae617684aa; _gd1623506621142=1; e9fe463f-802a-4c69-b181-f5c5ad4305c5_TMXCookie=true; _sdsat_highestContentConfidence={%22course_uuid%22:%224b278621-1ff4-4f47-afcf-c613047a1553%22%2C%22course_name%22:%22intermediate-algebra%22%2C%22confidence%22:0.1501%2C%22year_in_school%22:%22college-year-1%22%2C%22subject%22:[{%22uuid%22:%220cf46127-71ed-41c6-bea0-67b85e0d3bc6%22%2C%22name%22:%22algebra%22}]}; chgcsdmtoken=e9fe463f-802a-4c69-b181-f5c5ad4305c5++web|O5syefnm0OgfgfmYsRF6++1623506684068; _uetsid=14bd7b70ca0e11ebbed60def281bf8bf; _uetvid=6439cf50598111eb8b57b3883813738a; exp=A184B%7CA311C%7CA803B%7CC024A; expkey=E6003A675A636A34AE07AF56A498B086",
                    # 'Sec-GPC': '1',
                    # 'TE': 'Trailers'
                }

                r = requests.get(str("https://www.chegg.com/homework-help/follow-prob-7-39-students-measure-aerodynamic-drag-model-sub-chapter-7-problem-41p-solution-9780077295462-exc"),headers=headers, data=payload)
                soup = s(r.content, 'html.parser')

                f = open("nn2.txt", "w")
                f.write(str(soup))
                f.close
                f2 = open("./nn2.txt", "r")
                # f2.read()
                # print(f2.read())

                #############
                text = str(f2.read())
                start = text.find('''prod","token"''') + 1
                end = text.find('''userUuid''')
                cut_text2 = text[start:end].strip()
                print(cut_text2)
                vv = cut_text2.replace('''rod","token":"''', "")
                vv2 = vv.replace('''","''', "")
                print(str(vv2))
                ##################

                payload2 = json.dumps({
                    "query": {
                        "operationName": "getSolutionDetails",
                        "variables": {
                            "isbn13": z2,
                            "chapterId": z1,
                            "problemId": z3
                        }
                    },
                    "token": str(vv2)
                })
                response = requests.request("POST", url, headers=headers, data=payload2)
                print(response)
                if "problemHtml" not in str(response.text):
                    print("is can not get ans book")
                    return 'Something is wrong with the book getting resolved'
                else:
                    print("now l can get ans book")
                    # print(response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]["problemHtml"])
                    xx = response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]['solutionV2'][0]["totalSteps"]
                    xx2 = response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]["problemHtml"]
                    for i in range(xx):
                        # print(response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]['solutionV2'][0]['steps'][i]["html"])
                        # v="\n"+response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]['solutionV2'][0]['steps'][i]["html"]
                        # print(str(v))
                        f = open('DD.html', 'a')
                        f.write("""<H3> <p style="color:RED;">""" + "Step " + str(i + 1) + " of " + str(
                            xx) + ":) </H3> </p>" + "\n" + str(
                            response.json()['data']['textbook_solution']['chapter'][0]['problems'][0]['solutionV2'][0][
                                'steps'][i]["html"]))
                        f.close()
                    # os.remove("DD.html")
                    f2 = open('DD.html', 'r')
                    f = open('Answer.html', 'w')
                    f.write(str(hh1) + """<H1> <p style="color:#2E97A6;">""" + " All Step " + str(
                        xx) + ":) </H1> </p> " + "\n" + str(xx2) + "\n" + f2.read() + str(hh2))
                    f.close()
                    os.remove("DD.html")
                    i = open('./Answer.html', 'rb')
                    # imgkit.from_file('Answer.html', 'Answer.jpg')
                    # i2 = open('./Answer.jpg', 'rb')
                    #########up file
                    url = "https://siasky.net/skynet/skyfile"

                    files = [
                        ('', ('Answer.html', open('./Answer.html', 'rb'), 'text/html'))
                    ]
                    headers7 = {
                        'referrer': 'https://siasky.net/'
                    }
                    #response = requests.request("POST", url, headers=headers7, data=payload, files=files)
                    #print(response.text)
                    if 'skylink' not in str("oooooo"):
                        return 'here is your answer :\n'
                    else:
                        #print(response.json()["skylink"])
                        #linkup = "https://siasky.net/" + response.json()["skylink"]
                        return 'here is your answer :\n' 
                    #i2 = open('./clients.json', 'rb')
                    #markdown = """✅ This is your answer 🌚\n✅ Join channel : @Chegg6\n✅ Remaining : 🔓""" + r + """🔓 """ + "\n✅ Time ⏱ : """ + str( mma) + "\n✅ Solution link: " + str(linkup) + """"""

                break




    except:
        pass

#ans url chegg H.w
linkapi="https://api-bot.alinasim.repl.co/p?tagId="
def send_req(qu_url):
    try:
        print(qu_url)
        r = requests.get(linkapi + qu_url,data=payload)
        print(r)
        soup = s(r.content, 'html.parser')
        print(r)

        if "An expert answer will be posted here" in str(soup):
            return '⚠️ لم تتم الإجابة على هذا السؤال'+"\n⚠️ This question hasn't been answered"
        else:
            x0 = soup.find('div', '</div>', class_="ugc-base question-body-text")
            x1 = soup.find('div', '</div>', class_="answer-given-body ugc-base")
            if 'None' in str(x1):
                return "Something went wrong, send it at another time"
            else:
                for a in x0.findAll('img'):
                    if "https:" not in a['src']:
                        print("reo https")
                        a['src'] = "https:" + a['src']
                    else:
                        print("noo")
                s1 = str(x0)
                ###################
                for a in x1.findAll('img'):
                    if "https:" not in a['src']:
                        print("reo https")
                        a['src'] = "https:" + a['src']
                    else:
                        print("noo")
                s2 = str(x1)
                ############
                f = open('Answer.html', 'w')
                messagee = str("""

                <html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8">
                                        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
                                            <link rel="preconnect" href="https://fonts.gstatic.com">
                                            <link href="https://fonts.googleapis.com/css2?family=Questrial&amp;display=swap" rel="stylesheet">
                                        <link rel="stylesheet" href="style.css">
                                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">



                                        <style>
                                        h1 {
                                            font-family: 'Questrial', sans-serif;
                                                }

                                        p {
                                    font-family: 'Questrial', sans-serif;
                                            }

                                        td {
                                    font-family: 'Questrial', sans-serif;
                                            }  


                                        .content {
                                            width: 100%;
                                        margin: auto;
                                        background: white;
                                        padding: 10px;
                                            }


                                        img{
                                        max-width: 100%;
                                            }
                                            body {background-color: LightGray;
                                                overflow: scroll;}
                                        h1   {color: red;}

                                            </style>

                                            </head><body><div class="container"><div class="alert alert-danger alert-dismissible" role="alert">
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>
                                            <center><strong> <p><a href="https://t.me/AliAuzi1">For All Answers Join channel : @AliAuzi1</a></p></strong> 
                                            </center></div><div class="content" "=""><h1></h1><h1><font size="6"><strong>Q:</strong></font></h1><p></p><div id="mobile-question-style" style="font-family: Roboto; color:#333333; "><p dir="ltr"> """ + str(
                    s1) + """</p>
                </div><p dir="ltr">&nbsp; </p>
                <p></p><hr><h1><font size="6"><strong>A:</strong></font></h1><p></p><p> """ + str(s2) + """ </p><p></p> </div> </div></body></html>










                """)
                f.write(messagee)
                f.close()
                url = "https://siasky.net/skynet/skyfile"
                files = [
                    ('', ('Answer.html', open('./Answer.html', 'rb'), 'text/html'))
                ]
                headers7 = {
                    'referrer': 'https://siasky.net/'
                }
                #response = requests.request("POST", url, headers=headers7, data=payload, files=files)
                #print(response.text)
                if 'skylink' not in str(messagee):
                    return 'here is your answer :\n'
                else:
                    #print(response.json()["skylink"])
                    #linkup = "https://siasky.net/" + response.json()["skylink"]
                    return 'here is your answer :\n'
    except:
        pass


def editMessage(text, chat_id, text_id , inline_keyboard):
    try:
        url = URL + "editMessageText?chat_id={}&message_id={}&parse_mode=&text={} &reply_markup=".format(chat_id,text_id, text) + inline_keyboard
        r = get_url(url)
        return r
    except:
        pass

def deleteMessage(chat_id, message_id):
    try:
        url = URL + "deleteMessage?chat_id={}&message_id={}".format(chat_id, message_id)
        get_url(url)
    except:
        pass

def send_message(text, chat_id, text_id = None,inline_keyboard=None,parse_mode=None):
    try:
        data = {
            'text':text,
            'chat_id':chat_id,
            'reply_to_message_id':text_id,
            'reply_markup':inline_keyboard,
            'disable_web_page_preview':True,
            'parse_mode': parse_mode
        }
        r = post_url(URL + "sendMessage",data)
        return r
    except Exception as e:
        print(e)

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        # print(updates)
        try:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                for i in updates['result']:
                    Check(i)
        except:
            try:
                print(updates['description'])
            except:
                pass




if __name__ == '__main__':
    main()
