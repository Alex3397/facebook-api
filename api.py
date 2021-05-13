import os
import json
import requests
import time
from decouple import config

def changeEnv(Env,Token):
    os.system("sed -i '/" + config(Env) + "/d' .env")
    os.system("sed -i -e '$a" + Env +"=" + Token + "' .env")
    print("Changed " + Env)
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

    print("\nNew token succesfully requested\n") if str(longTokenRequest) == '<Response [200]>' else print("\nCould not request new token\nError:\n"+str(longTokenData['error']['message']))
    print("Changing Enviroment variables") if str(longTokenRequest) == '<Response [200]>' else 0

    changeEnv('SHORT_TOKEN',longTermToken) if str(longTokenRequest) == '<Response [200]>' else 0
    changeEnv('LONGTERM_TOKEN',longTermToken) if str(longTokenRequest) == '<Response [200]>' else 0
    pass

def getActiveCampaings(adAccountId,token=config('LONGTERM_TOKEN')):
    accountCampaingsFields = str(config('ACCOUNT_CAMPAING_FIELDS'))
    accountCampaings = "https://graph.facebook.com/v10.0/act_" + adAccountId\
        + "/campaigns?effective_status=['ACTIVE']&date_preset=this_year"\
        + "&fields=" + accountCampaingsFields\
        + "&limit=5000"\
        + "&access_token=" + token

    accountCampaingRequest = requests.get(url=accountCampaings)
    accountCampaingHeaders = accountCampaingRequest.headers
    accountCampaingData = accountCampaingRequest.json()

    print("Request Status: " + str(accountCampaingRequest))
    print("\nRequest Headers:\n" + str(accountCampaingHeaders))
    print("\nRequest Data:\n" + str(accountCampaingData)) if str(accountCampaingRequest) == '<Response [200]>' else print("\nError message:\n" + accountCampaingData['error']['message'])

    print("Storing Campaings Data\n")
    with open(str(os.getcwd()) + '/stored_data/' + str(adAccountId) + '_campaings_data.json', 'w') as outfile:
        json.dump(accountCampaingData, outfile)
    print("Campaings Data Stored")
    pass

def getActiveAdsets(adAccountId,Token=config('LONGTERM_TOKEN'),limit=25,page_limit=3):
    # contextual_bundling_spec (configuracoes de anuncio) nao funciona se usuario nao estiver na lista branca
    adSetFields = config('ADSET_FIELDS')
    adSets = "https://graph.facebook.com/v10.0/act_" + adAccountId + "/adsets"\
        + "?access_token=" + Token\
        + "&date_preset=this_year"\
        + '&effective_status=["ACTIVE"]'\
        + "&limit=" + str(limit)\
        + "&fields=" + adSetFields
    
    print("Requesting GET\n")
    start = time.time()
    Request = requests.get(url=adSets)
    end = time.time()
    elapsed = end - start
    Headers = Request.headers
    Data = Request.json()
    parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access'] if "error" in Data else 0

    print("Request done in: " + str(elapsed) + " seconds\n")
    print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
    print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
    print(Data) if "error" not in Data else 0
    time.sleep(20 - elapsed) if elapsed > 0 else 0
    
    stored = []
    print("\nStart Crawling\n")

    while 'next' in Data['paging']:
        stored.append(Data)
        print("\nCrawler Requesting GET\n")

        start = time.time();Crawler = requests.get(url=Data['paging']['next']);end = time.time()
        Headers = Crawler.headers
        Data = Crawler.json()
        parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access'] if "error" not in Data else 0

        print("Request done in: " + str(elapsed) + " seconds\n")
        print("Status: [200] OK\n") if str(Crawler) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
        print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
        print(Data) if "error" not in Data else 0

        elapsed = end - start
        time.sleep(20 - elapsed) if elapsed > 0 else 0
        pass

    print("Storing Adsets\n")
    with open(str(os.getcwd()) + '/stored_data/' + str(adAccountId) + '_adset_data.json', 'w') as outfile:
        json.dump(stored, outfile)
    print("Adsets Stored")
    pass

def getInsights(adAccountId, token=config('LONGTERM_TOKEN')):
    # Usuario precisa estar na lista branca para acessar impressions_dummy
    insightsFields = config('INSIGHTS_FIELDS')
    adset = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_data.json')
    data = json.load(adset)
    adset_id = data[0]['data'][0]['id']
    insights = "https://graph.facebook.com/v10.0/" + adset_id\
        + "/insights?data_preset=this_year&fields=" + insightsFields\
        + "&access_token=" + token

    insightsRequest = requests.get(url=insights)
    insightsHeaders = insightsRequest.headers
    insightsData = insightsRequest.json()

    print("Request Status: " + str(insightsRequest))
    print("\nRequest Headers:\n" + str(insightsHeaders))
    print("\nRequest Data:\n" + str(insightsData)) if str(insightsRequest) == '<Response [200]>' else print("\nError message:\n" + insightsData['error']['message'])
    
    print("Storing Insights\n")
    with open(str(os.getcwd()) + '/stored_data/' + str(adAccountId) + '_adset_insights_data.json', 'w') as outfile:
        json.dump(insightsData, outfile)
    print("Insights Stored")
    pass