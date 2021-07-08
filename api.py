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

def storeData(adAccountId,data,file_name,base_dir='/stored_data/'):
    print("Storing Data\n")
    path = str(os.getcwd()) + str(base_dir) + str(adAccountId) + str(file_name) + '.json'

    with open(str(os.getcwd()) + str(base_dir) + str(adAccountId) + str(file_name) + '.json', 'w') as outfile:
        json.dump(data, outfile)

    print("Data Stored in path:\n" + path)
    print(data)
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

def Crawl(storeFrame,adAccountId,Data,request_count=1):
    print("\nStarting Crawl\n")
    request_count = request_count
    storeFrame.append(Data)

    while 'next' in Data['paging']:
        print("\nRequesting Crawler GET\n")

        start = time.time();Crawler = requests.get(url=Data['paging']['next']);end = time.time()
        elapsed = end - start
        Headers = Crawler.headers
        Data = Crawler.json()
        storeFrame.append(Data)
        parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access'] if "error" not in Data else 0

        print("Request done in: " + str(elapsed) + " seconds\n")
        print("Status: [200] OK\n") if str(Crawler) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
        print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
        print(Data) if "error" not in Data else 0

        request_count += 1
        time.sleep(20 - elapsed) if elapsed > 0 else 0
        pass
    
    print("\nTotal Crawl Request Count: " + str(request_count) +"\n")
    pass

def getAllCampaings(adAccountId,token=config('LONGTERM_TOKEN'),request_count=0):
    request_count = request_count
    accountCampaingsFields = str(config('ACCOUNT_CAMPAING_FIELDS'))
    accountCampaings = "https://graph.facebook.com/v10.0/act_" + adAccountId\
        + "/campaigns?date_preset=this_year"\
        + "&fields=" + accountCampaingsFields\
        + "&access_token=" + token

    accountCampaingRequest = requests.get(url=accountCampaings)
    accountCampaingHeaders = accountCampaingRequest.headers
    Data = accountCampaingRequest.json()
    request_count += 1

    print("Request Status: " + str(accountCampaingRequest))
    print("\nRequest Headers:\n" + str(accountCampaingHeaders))
    print("\nRequest Data:\n" + str(Data)) if str(accountCampaingRequest) == '<Response [200]>' else print("\nError message:\n" + Data['error']['message'])

    storeFrame = []
    Crawl(storeFrame,adAccountId,Data)
    storeData(adAccountId,storeFrame,'_all_campaings_data')
    pass

def getActiveCampaings(adAccountId,token=config('LONGTERM_TOKEN'),request_count=0):
    request_count = request_count
    accountCampaingsFields = str(config('ACCOUNT_CAMPAING_FIELDS'))
    accountCampaings = "https://graph.facebook.com/v10.0/act_" + adAccountId\
        + "/campaigns?effective_status=['ACTIVE']&date_preset=this_year"\
        + "&fields=" + accountCampaingsFields\
        + "&limit=5000"\
        + "&access_token=" + token

    accountCampaingRequest = requests.get(url=accountCampaings)
    accountCampaingHeaders = accountCampaingRequest.headers
    accountCampaingData = accountCampaingRequest.json()
    request_count += 1

    print("Request Status: " + str(accountCampaingRequest))
    print("\nRequest Headers:\n" + str(accountCampaingHeaders))
    print("\nRequest Data:\n" + str(accountCampaingData)) if str(accountCampaingRequest) == '<Response [200]>' else print("\nError message:\n" + accountCampaingData['error']['message'])

    storeData(adAccountId,accountCampaingData,'_campaings_data')
    pass

def getActiveAdsets(adAccountId,Token=config('LONGTERM_TOKEN'),limit=25,request_count=0):
    # contextual_bundling_spec (configuracoes de anuncio) nao funciona se usuario nao estiver na lista branca
    request_count = request_count
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
    request_count += 1

    print("Request done in: " + str(elapsed) + " seconds\n")
    print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
    print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
    print(Data) if "error" not in Data else 0
    time.sleep(20 - elapsed) if elapsed > 0 else 0
    
    storeFrame = []
    Crawl(storeFrame,adAccountId,Data)
    storeData(adAccountId,storeFrame,'_all_adset_data')
    pass

def getInsights(adAccountId, token=config('LONGTERM_TOKEN'),data_from_campaing=True,base_dir='/stored_data/',file_name='_adset_data.json',request_count=0):
    # Usuario precisa estar na lista branca para acessar impressions_dummy
    parent = "_campaing" if data_from_campaing else "_all"
    request_count = request_count
    insightsFields = config('INSIGHTS_FIELDS')
    adset = open(os.getcwd() + base_dir + str(adAccountId) + parent + file_name)
    data = json.load(adset)

    storeInsightsData = []

    for x in range(len(data[0]['data'])):
        adsetID = data[0]['data'][x]['id']
        insights = "https://graph.facebook.com/v10.0/" + adsetID\
            + "/insights?data_preset=this_year&fields=" + insightsFields\
            + "&access_token=" + token

        insightsRequest = requests.get(url=insights)
        insightsHeaders = insightsRequest.headers
        insightsData = insightsRequest.json()
        storeInsightsData.append(insightsData)
        request_count += 1

        print("Request Status: " + str(insightsRequest))
        print("\nRequest Headers:\n" + str(insightsHeaders))
        print("\nRequest Data:\n" + str(insightsData)) if str(insightsRequest) == '<Response [200]>' else print("\nError message:\n" + insightsData['error']['message'])
        
    storeData(adAccountId,storeInsightsData,'_adset_insights_data')
    print("\nTotal requests by getInsights(): " + str(request_count) + "\n")
    pass

def getActiveCampaingAdsets(adAccountId,token=config('LONGTERM_TOKEN'),isCampaingUpToDate=False,request_count=0):
    campaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_data.json')
    adSetFields = config('ADSET_FIELDS')
    campaings = json.load(campaings)
    isCampaingUpToDate = isCampaingUpToDate
    request_count = request_count
    x = 0

    while x in range(0,len(campaings['data'])) or x < 0:
        print("\nCampaing id: " + str(campaings['data'][x]['id']))
        CampaingId = campaings['data'][x]['id']
        CampaingAdSets = "https://graph.facebook.com/v10.0/" + CampaingId + "/adsets"\
                + "?access_token=" + token\
                + '&effective_status=["ACTIVE"]'\
                + "&date_preset=this_year"\
                + "&limit=5000"\
                + "&fields=" + adSetFields

        print("\nRequesting GET\n")
        Request = requests.get(url=CampaingAdSets)
        Headers = Request.headers
        Data = Request.json()
        parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access'] if "error" in Data else 0
        request_count += 1

        print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
        print(Headers)
        print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
        print(Data) if "error" not in Data else 0

        CampaingAdSetsData = []

        if len(Data['data']) == 0:
            print("\nNon existing data. Checking if campaing data is up to date.\n")

            if isCampaingUpToDate == False:
                print("\nCampaing is not up to date.\n")
                print("\nFetching campaing data:\n")
                getActiveCampaings(adAccountId,request_count=request_count)
                print("\nCampaing data updated.\nRestarting Adset Request.\n")
                isCampaingUpToDate = True
                x = 0
                print(x)
                time.sleep(20)
            
            else:
                print("\nCampaing is up to date.\n")
                print("\nThere is no active adset.\nMoving on.")
                x += 1

        else:
            CampaingAdSetsData.append(Data)
            time.sleep(20)
            x += 1
            print(x)

    storeData(adAccountId,CampaingAdSetsData,'_campaing_adset_data')
    pass

def getCustomAudiences(adAccountId,token=config('LONGTERM_TOKEN')):
    CustomAudiences = "https://graph.facebook.com/v10.0/act_" + str(adAccountId) + "/customaudiences"\
        + "?access_token=" + token\
        + "&fields=name,approximate_count"\
        + "&limit=5000"

    Request = requests.get(url=CustomAudiences)
    Headers = Request.headers
    Data = Request.json()

    print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
    print(Headers)
    print(Data) if "error" not in Data else 0
    
    storeData(adAccountId,Data,'_custom_audiences')
    pass

def getActiveCampaingsNames(adAccountId,token=config('LONGTERM_TOKEN'),request_count=0):
    request_count = request_count
    accountCampaings = "https://graph.facebook.com/v10.0/act_" + adAccountId\
        + "/campaigns?effective_status=['ACTIVE']&date_preset=this_year"\
        + "&fields=name"\
        + "&limit=5000"\
        + "&access_token=" + token

    accountCampaingRequest = requests.get(url=accountCampaings)
    accountCampaingHeaders = accountCampaingRequest.headers
    accountCampaingData = accountCampaingRequest.json()
    request_count += 1

    print("Request Status: " + str(accountCampaingRequest))
    print("\nRequest Headers:\n" + str(accountCampaingHeaders))
    print("\nRequest Data:\n" + str(accountCampaingData)) if str(accountCampaingRequest) == '<Response [200]>' else print("\nError message:\n" + accountCampaingData['error']['message'])

    storeData(adAccountId,accountCampaingData,'_campaings_names_data')
    return accountCampaingData['data']