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

    print("New token succesfully requested") if str(longTokenRequest) == '<Response [200]>' else print(longTokenData['error']['message'])
    print("Changing Enviroment variables\n")

    changeEnv('SHORT_TOKEN',longTermToken)
    changeEnv('LONGTERM_TOKEN',longTermToken)
    pass

def getAdsets(adAccountId,Token,limit=20,page_limit=3):
    # contextual_bundling_spec (configuracoes de anuncio) nao funciona se usuario nao estiver na lista branca
    ad_sets = "https://graph.facebook.com/v10.0/act_" + adAccountId + "/adsets?access_token=" + Token\
        + "&date_preset=this_year" + "&fields=" + config('ADSET_FIELDS') + "&limit=" + str(limit)
    
    print("Requesting GET\n")
    Request = requests.get(url=ad_sets)
    Headers = Request.headers
    Data = Request.json()
    print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
    parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access']
    print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
    print(Data) if "error" not in Data else 0
    
    print("\nStart Crawling\n")
    stored = []
    i=0
    while i != page_limit:
        start = time.time()
        stored.append(Data)
        print("Crawler Requesting GET\n")
        Crawler = requests.get(url=Data['paging']['next'])
        Data = Crawler.json()
        print("Status: [200] OK\n") if str(Crawler) == '<Response [200]>' else print(Data['error']['message'])
        print(json.dumps(Data, indent=4))
        end = time.time()
        elapsed = end - start
        print("\nseconds elapsed: " + str(elapsed) + "\n")
        time.sleep(20 - elapsed) if elapsed > 0 else 0
        i += 1
        pass

    print("Storing Adsets\n")
    with open(str(os.getcwd()) + '/stored_data/' + str(adAccountId) + '_adset_data.json', 'w') as outfile:
        json.dump(stored, outfile)
    print("Adsets Stored")
    pass

def getInsights(adAccountId):
    # Usuario precisa estar na lista branca para acessar impressions_dummy
    insightsFields = config('INSIGHTS_FIELDS')
    adset = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_data.json')
    data = json.load(adset)
    adset_id = data[0]['data'][0]['id']
    insights = "https://graph.facebook.com/v10.0/" + adset_id + "/insights?data_preset=this_year&fields="\
        + insightsFields + "&access_token=" + token +"&limit=1"

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

# setNewEnv()

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
token = config('LONGTERM_TOKEN')

account = "https://graph.facebook.com/v10.0/act_" + adAccountId\
    + "/campaigns?effective_status=['ACTIVE']&date_preset=this_year"\
    + "&fields=id,name,objective,insights,total_count,adlabels,bid_strategy,buying_type,daily_budget,is_skadnetwork_attribution,iterative_split_test_configs,lifetime_budget,promoted_object,source_campaign_id,special_ad_categories,special_ad_category_country,spend_cap,start_time,status,stop_time,topline_id,upstream_events"\
    + "&access_token=" + token

accountRequest = requests.get(url=account)
print(accountRequest)
acdata = accountRequest.json()
print(acdata)

campaingFields = config('CAMPAING_FIELDS')
campaing_id = config('CAMPAING_ID')
campaings = "https://graph.facebook.com/v10.0/"+ campaing_id\
    + "/?date_preset=this_year&fields=" + campaingFields + "&access_token=" + token

# getrequest = requests.get(url=campaings)
# print(getrequest)
# data = getrequest.json()
# print(data)

# getAdsets(config('ADACCOUNT_ID2'),config('LONGTERM_TOKEN'),1,3)
# getInsights(adAccountId)

# leads = "https://graph.facebook.com/v10.0/"+ adGroupId +"/leads?access_token=" + token
