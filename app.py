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
                return 'Please make sure the link is correct ????????'

    else:
        return 'Please make sure the link is correct ????????'

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
                    send_message('?????? ???????? ??????????',chat_id)
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
                                send_message('???? ???????????? ???????? \npoints expired\n\nMore points contact ',chat_id,message_id)
                            else:
                                resl =send_req(qu_url)
                                se = str(resl)
                                if se.startswith('here is your answer'):
                                    su=sub_point(user_id)
                                    i = open('./Answer.html', 'rb')
                                    url876 = ("https://api.telegram.org/bot"+TOKEN+"/sendDocument?chat_id="+str(chat_id)+'&caption='+str('This is your answer ????'+str()+'\n??? Remaining points:'+str(su)+""+'&reply_to_message_id='+str(message_id))+'&parse_mode=Markdown')
                                    url_txt = requests.post(url876, files={'document': i})
                                else:
                                    send_message(resl, chat_id, message_id)
                        else:
                            print("now l can get answer")
                            pi=get_point(user_id)
                            print(pi)
                            ress=int(pi)
                            if ress==0 or ress<0:
                                send_message('???? ???????????? ???????? \npoints expired\n\nMore points contact ',chat_id,message_id)
                            else:
                                print("l am sore but not answer")
                                resl = ans_book(qu_url)
                                se = str(resl)
                                if se.startswith('here is your answer'):
                                    su=sub_point(user_id)
                                    i = open('./Answer.html', 'rb')
                                    url876 = ("https://api.telegram.org/bot"+TOKEN+"/sendDocument?chat_id="+str(chat_id)+'&caption='+str('This is your answer ????'+str()+'\n??? Remaining points:'+str(su)+""+'&reply_to_message_id='+str(message_id))+'&parse_mode=Markdown')
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
                    'Cookie': "C=0; O=0; V=e0f96a13ff179f8a15c57ed7cbd8eae76092e252aa7330.20619403; optimizelyEndUserId=oeu1620238947057r0.4739424413092004; _pxvid=e756da38-adce-11eb-a65e-0242ac12000e; usprivacy=1YNY; _omappvp=d4LHLApu8WYRvXT7K4X7t3buIOz748uIGefedImlcTCB8dQMLm7HyU3fa78stjOBNJathpREhAXg0FBPvTy06vmXcsniNhks; _ga=GA1.2.1710289273.1620239010; _ym_d=1620239019; _ym_uid=1620239019425285515; _rdt_uuid=1620239029113.3bde86d0-1a8b-464e-86bb-00368726626b; _fbp=fb.1.1620239030002.1358400468; _gcl_au=1.1.1080882895.1620239032; s_ecid=MCMID%7C21757172410124956326528104647333967652; _scid=fa3dd047-7fdb-4b1a-b28f-105cc20a14b8; __gads=ID=bf7f7adb7dbf9dfa:T=1620412564:S=ALNI_MYaQB0ypzDhDdnDn8tpskkNrYQhTw; _cs_c=1; sbm_mcid=21757172410124956326528104647333967652; sbm_sbm_id=0100007F694F9860440071970272AA20; sbm_country=IQ; sbm_dma=0; __ssid=85819ca27ddb9b7289cf02d3be49adc; _vid=BK790Wv976EZR0EoZf8r; DFID=web|BK790Wv976EZR0EoZf8r; chgcsdetaintoken=1; adobeujs-optin=%7B%22aam%22%3Atrue%2C%22adcloud%22%3Atrue%2C%22aa%22%3Atrue%2C%22campaign%22%3Atrue%2C%22ecid%22%3Atrue%2C%22livefyre%22%3Atrue%2C%22target%22%3Atrue%2C%22mediaaa%22%3Atrue%7D; omSeen-tgjg3ieouzbhy6fc0ctw=1623271980532; sourceTracking=adobe; gidr=MA; chgcsastoken=CQleSNb9N9gIRehpWX6wF12a5nvsnujDlqz5P7DbWi5X3Z_lV_FYL7Z0FOcXmAB6RMqjl_o5e7SqECCN6ESx0KLpCnlKsZ6UBVHdA0XiIiB7N7ZyiQ81tD5gS5wirDWQ; _sctr=1|1624654800000; _cs_id=d5498b0f-d242-a0af-edbd-deaaf993a45a.1620412942.29.1624807199.1624807199.1.1654576942499.Lax.0; __CT_Data=gpv=78&ckp=tld&dm=chegg.com&apv_79_www33=78&cpv_79_www33=78; _sp_id.ad8a=79b408a5-a90f-4faf-8bae-b389c289b872.1623075166.15.1624868606.1624807683.4a9d8644-3469-4ebc-ad2e-23ed6084c566; gid=1566655; _gid=GA1.2.1353768807.1625046981; intlPaQExitIntentModal=hide; user_geo_location=%7B%22country_iso_code%22%3A%22IQ%22%2C%22country_name%22%3A%22Iraq%22%2C%22region%22%3A%22BG%22%2C%22region_full%22%3A%22Baghdad%22%2C%22city_name%22%3A%22Baghdad%22%2C%22locale%22%3A%7B%22localeCode%22%3A%5B%22ar-IQ%22%5D%7D%7D; AMCVS_3FE7CBC1556605A77F000101%40AdobeOrg=1; al_cell=2021-7-2-wt-main-1-control; BIBSESSID=0392366a-dce6-4d05-bf25-afa6312f0985; CSID=1625292988618; mcid=21757172410124956326528104647333967652; schoolapi=null; PHPSESSID=jrudtso6ifes19kqvrsotgcdeq; CSessionID=0aa5999f-abf8-418c-9267-ac87cebab3ef; forterToken=5d627c8ac7184415a386d8768fd2da60_1625293027644__UDF43_13ck; _px3=3f50285b8317e40b0c555ed421cf7c60785531e2ac7112395cffc2834f90c114:Jn8HWI3G3Vdf4NC4k8YlLvvT1b3YPq4CfQvDNPDOEyltR/DKQX0VObybB/nF826hnI0lLQCSIr027rQ5lLWVtw==:1000:UrO6q1YOsxRuEQWX9RoXCosMvl3mwNZm6vzF4/SW/0JAWXNUHjK0oN4FhahbGR1lZQc6tDQcAhyzmLu3pXtHOZJhwEXFwEwO6sRvb41hePTHWMGnE0IYmxdULazKJLxqUFxXrFSoG4gTUVvX6Qe1ZTxCP/unIkqhn42iAeNoeX7mILoL4Qw+vLiTYm4yrTC9mIWawUG0+ozWzWO6ejt0JQ==; chgmfatoken=%5B%20%22account_sharing_mfa%22%20%3D%3E%201%2C%20%22user_uuid%22%20%3D%3E%209de64bf2-3a90-41e3-b4d3-7d9bc61f0287%2C%20%22created_date%22%20%3D%3E%202021-07-03T06%3A17%3A57.018Z%20%5D; id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI5ZGU2NGJmMi0zYTkwLTQxZTMtYjRkMy03ZDliYzYxZjAyODciLCJhdWQiOiJDSEdHIiwiaXNzIjoiaHViLmNoZWdnLmNvbSIsImV4cCI6MTY0MTA2MzE5MiwiaWF0IjoxNjI1MjkzMTkyLCJlbWFpbCI6Im1vZ2FoYWRtYWhtb2RAZ21haWwuY29tIn0.csztT4MSeUrlE1508XldaGevpqzfXyVsAt6iumXow3LxzVqPuhVjx6_aIvo0npVa6BG4GWYEx0GbOzO1nvIVwgeW4hzCW3bjYXciN0vJ2k9gPogaw5HRK_GEnmYMD8pAoQ8eq4YQUZn0m8w0QtCJSlV1GE-YbgD0dR5HfK-Dpgq9NqhmlxKD-nc-5W90ZGCd2sBwKyvMz_XPnOtVcgL5-f75bF52InP1irQdkTZ5QKmNa4JMLWp5I6Y2uUP1d64odjVDT9N7b0DjeC8yRauZIPuY1WqbCwS920tC6BmGXXgga4tb-1JUkvEVYxmE_WUKArcUegWN4j6yqI4MdlmDBQ; access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhUTkU0cWwxNTRxekZieTBBakxDdSJ9.eyJodHRwczovL3Byb3h5LmNoZWdnLmNvbS9jbGFpbXMvYXBwSWQiOiJOc1lLd0kwbEx1WEFBZDB6cVMwcWVqTlRVcDBvWXVYNiIsImlzcyI6Imh0dHBzOi8vY2hlZ2ctcHJvZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8OWRlNjRiZjItM2E5MC00MWUzLWI0ZDMtN2Q5YmM2MWYwMjg3IiwiYXVkIjpbImNoZWdnLW9pZGMiLCJodHRwczovL2NoZWdnLXByb2QudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYyNTI5MzE5MiwiZXhwIjoxNjI1Mjk0NjMyLCJhenAiOiIzVFpiaGZzWndkZUhiaG9WTXhPdlpHYjM3TWN2YzBvOCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgYWRkcmVzcyBwaG9uZSBvZmZsaW5lX2FjY2VzcyIsImd0eSI6InBhc3N3b3JkIn0.Kv2-t7rwwp5XOL-opD72hXCz7r_iQKPypVfWbLf9bceHzE5LxccozbJENCozHCHbZ5azNH8G4AtJgEfS3PAT6aWlznfUksQSR0j4hJh1DApse9qhp7A9-Jaju_3S7fNKvkPJA3ls21TGaqPLDwgnHOBNw56MfopE3i9ETz1hK-ecynfuS2Zyi3n3AS7n7AIO5F2p-ssYoAME9N9UuD2OQw7kSiA-WdTTM1NeAC5H6Qomnrd32XzYThXYaf_U_Hoo9pd4Mm4Q3uiUmj5heKoPlBkVZ3BRJVPPcIBqBlYGFxjDhL4Rho5Wx3EZn9giKKiqaK-cuZZEwjCKziyi0iXEzw; access_token_expires_at=1625294633; refresh_token=ext.a0.t00.v1.MQFhKQ4AkzqJTZkOlI0sRz-wjnI-JCwKv6-qK89PXLLP6daTrKRDJ6L61xiVWgKxjlCLuwjW1D42kvOhiqX0EQg; SU=QWpjRHXDd0qkrWTh6RUSsVC56jd1qADCwTmJqfbb2pCoZNjoNECfJMr1_Q_NaL5ZkrGcC9uiFNKxFbiIE-jCSnVdgylIPJkAplilVF1UFT3bkXIZBz5URQTmvmjtUkQE; U=7874bfef6dbe1be98c99fd13ded1b4a0; exp=A311C%7CA803B%7CC024A%7CA560B%7CA207B%7CA239A%7CA209A%7CA212A%7CA735A%7CA259B%7CA110B%7CA966G%7CA270C%7CA278C%7CA935B%7CA448A%7CA360A%7CA890H; expkey=A7E03C9C8FD021D4FAB156C1CF235EE7; CVID=04307780-f55d-40ea-96f1-2ea1593febe6; _sdsat_cheggUserUUID=9de64bf2-3a90-41e3-b4d3-7d9bc61f0287; _sdsat_authState=Hard%20Logged%20In; sbm_a_b_test=3-control; userRole=mybib; _ym_isad=2; AMCV_3FE7CBC1556605A77F000101%40AdobeOrg=-408604571%7CMCIDTS%7C18811%7CMCMID%7C21757172410124956326528104647333967652%7CMCAID%7CNONE%7CMCOPTOUT-1625300462s%7CNONE%7CMCAAMLH-1625898062%7C6%7CMCAAMB-1625898062%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CMCSYNCSOP%7C411-18814%7CvVersion%7C4.6.0%7CMCCIDH%7C2124296753; chgcsdmtoken=%7B%22user_uuid%22%3A%229de64bf2-3a90-41e3-b4d3-7d9bc61f0287%22%2C%22created_date%22%3A%222021-07-03T06%3A21%3A18.740Z%22%2C%22account_sharing_device_management%22%3A1%7D; _gat=1; chgcsdmtoken=9de64bf2-3a90-41e3-b4d3-7d9bc61f0287++web|BK790Wv976EZR0EoZf8r++1625293308463; _gali=redirect-on-remove-device-dialog; s_pers=%20buFirstVisit%3Dcs%252Ccore%252Cothers%252Ctb%252Chelp%252Cme%7C1781038477724%3B%20gpv_v6%3Dchegg%257Cweb%257Ccs%257Cqa%257Cquestion%2520page%7C1625295113077%3B; _px3=dc179461da8ca43fa8377c0304282e9f9e37252401d044f2f30b9e0618c0059a:A5wxn/2dcmSXWGKwPUSucx0DPYKIH/woTcQHmePdMrnkLQiS/qc8MfbupOrwYJ2GtZQTRTlP2Ub1N4W3xsuu8Q==:1000:Rl6F8PglzOAtR6Nz81LDuhtzCiBBoeGTXZYutMinSRDx94v7BLDGYAPRRUmlQ4PDpGgmlxpifMJTs2bK1tx/mxQqFB4Bv99U4QS/ddSGFivvifpkdCUU/M2nPoy7ClEJacut4W/jIQrEsXtxeCm0Wcb4dTsSMbafgYbWopblgVBYV2I/tg0fvx+tKqwgCzLphwe8xd5LsiRvqV7bi/xfDw==; _px=A5wxn/2dcmSXWGKwPUSucx0DPYKIH/woTcQHmePdMrnkLQiS/qc8MfbupOrwYJ2GtZQTRTlP2Ub1N4W3xsuu8Q==:1000:nOpJSASX8/Udc1GfNm7HeA3A+ZV6UeW3DHxCtjDrFfA4IwIl40KoEi29cTDBsA/nHRE6jarU8tC/LiShvbme1F8q1QBm/o6nWhSJm0X0XEYnKLugQ4+15qEhwReekU7teDUXp8FhKrtGz+t6yHiRG+QZ+01Ptt1BoU6uPnGSaC739+dshyYjaq+9DmqEXg3mal520OIebzwagOAjqn+R8/EhdxdqWPyS/Rn4sLXNOERN9fizgXAduEa/3VHRAvzNd9tQHDf4i6P84ChOmxDcHQ==; OptanonConsent=isIABGlobal=false&datestamp=Sat+Jul+03+2021+09%3A21%3A54+GMT%2B0300+(%D8%A7%D9%84%D8%AA%D9%88%D9%82%D9%8A%D8%AA+%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A+%D8%A7%D9%84%D8%B1%D8%B3%D9%85%D9%8A)&version=6.10.0&hosts=&consentId=4f5b347a-89d2-4ac7-ab12-bbc8d4849fe7&interactionCount=1&landingPath=NotLandingPage&groups=snc%3A1%2Cfnc%3A1%2Cprf%3A1%2CSPD_BG%3A1%2Ctrg%3A1&AwaitingReconsent=false; s_sess=%20buVisited%3Dcore%252Ccs%3B%20s_sq%3Dcheggincriovalidation%253D%252526pid%25253Dchegg%2525257Cweb%2525257Ccore%2525257Cmyaccount%2525257Cdevices%252526pidt%25253D1%252526oid%25253Dfunctionln%25252528%25252529%2525257B%2525257D%252526oidt%25253D2%252526ot%25253DSUBMIT%3B%20cheggCTALink%3Dfalse%3B%20SDID%3D54D9127FE2A0DDA9-1E9011022CC52FB5%3B%20s_ptc%3D0.01%255E%255E0.02%255E%255E0.00%255E%255E0.17%255E%255E0.94%255E%255E0.18%255E%255E3.84%255E%255E0.28%255E%255E5.35%3B; _sdsat_highestContentConfidence={%22course_uuid%22:%2225666383-b7ce-4ff6-a7db-d5f73e55ef50%22%2C%22course_name%22:%22introduction-to-statistics%22%2C%22confidence%22:0.767%2C%22year_in_school%22:%22college-year-1%22%2C%22subject%22:[{%22uuid%22:%226dbb976f-d4ab-4bfc-84bf-cbfa5363b814%22%2C%22name%22:%22statistics%22}]}; _uetsid=6df6ecc0d98911eba5c69b883321329e; _uetvid=06caf680adcf11eb84310579a277abdb; wcs_bt=s_4544d378d9e5:1625293315; 9de64bf2-3a90-41e3-b4d3-7d9bc61f0287_TMXCookie=true",
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
                    #markdown = """??? This is your answer ????\n??? Join channel : @Chegg6\n??? Remaining : ????""" + r + """???? """ + "\n??? Time ??? : """ + str( mma) + "\n??? Solution link: " + str(linkup) + """"""

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
            return '?????? ???? ?????? ?????????????? ?????? ?????? ????????????'+"\n?????? This question hasn't been answered"
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
                                            <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">??</span></button>
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
