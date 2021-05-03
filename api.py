import os
import requests
from decouple import config

def changeEnv(Env,Token):
    os.system("sed -i '/" + config(Env) + "/d' .env")
    os.system("sed -i -e '$a" + Env +"=" + Token + "' .env")
    pass

def setNewEnv():
    shortToken = config('SHORT_TOKEN')
    longTermURL = config('LONGTERM_URL')
    appId = config('TESTAPP_ID') + "&"
    appSecret = config('TESTAPP_SECRET') + "&"
    
    getLongTermToken = longTermURL + "client_id=" + appId\
    + "client_secret=" + appSecret + "fb_exchange_token=" + shortToken
    longTokenRequest = requests.get(url=getLongTermToken)

    longTokenData = longTokenRequest.json()
    longTermToken = longTokenData['access_token']

    print("Status: [200] OK") if str(longTokenRequest) == '<Response [200]>' else print(longTokenData['error']['message'])

    changeEnv('SHORT_TOKEN',longTermToken)
    changeEnv('LONGTERM_TOKEN',longTermToken)
    pass

# setNewEnv()

adaccountid = config('ADACCOUNT_ID')
adgroupid = config('ADGROUP_ID')
token = config('LONGTERM_TOKEN')

leads = "https://graph.facebook.com/v10.0/"+ adgroupid +"/leads?access_token=" + token
ads_volume = "https://graph.facebook.com/v10.0/act_" + adaccountid + "/ads_volume?access_token=" + token
ad_sets = "https://graph.facebook.com/v10.0/act_" + adaccountid + "/adsets?access_token=" + token + "&fields=id,name,configured_status,effective_status"

# # stored = []

# CrawlerUrl = requests.get(url=ad_sets)
# print(CrawlerUrl)
# data = CrawlerUrl.json()
# print(data)

# while 'next' in list(data['paging'].keys()):
#     stored.append(data)
#     CrawlerUrl = requests.get(url=data['paging']['next'])
#     data = CrawlerUrl.json()
#     print(CrawlerUrl)
#     print(data)

# print("")
# print("Stored data:")
# print("")
# print(stored)
# for i in data:
#     print(i)
#     for a in data[i]:
#         print(a)
#         if i == "data":
#             print(a['id'])