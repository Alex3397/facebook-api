import os
import json
import requests
import time
import api
from decouple import config

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
Token = config('LONGTERM_TOKEN')

# api.getActiveCampaings(adAccountId)
campaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_data.json')
campaings = json.load(campaings)

# api.getActiveAdsets(adAccountId)
adset = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_data.json')
adset = json.load(adset)

# api.getInsights(adAccountId)
insights = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_insights_data.json')
insights = json.load(insights)

# for x in range(0,len(adset)):
#         for c in range(0,len(adset[x]['data'])):
#             print("Adset Number: " + str(c))
#             # print("Adset    Id: " + str(adset[x]['data'][c]['id']))
#             print("Campaing Id: " + str(adset[x]['data'][c]['campaign_id']))
#             # print("Adset Data: \n\n" + str(adset[x]['data'][c]) + "\n")

# print("")
# # print(adset[0])        

adSetFields = config('ADSET_FIELDS')
limit = 5000

for x in range(0,len(campaings['data'])):
    print("\nCampaing id: " + str(campaings['data'][x]['id']))
    CampaingId = campaings['data'][x]['id']
    CampaingAdSets = "https://graph.facebook.com/v10.0/" + CampaingId + "/adsets"\
            + "?access_token=" + Token\
            + '&effective_status=["ACTIVE"]'\
            + "&date_preset=this_year"\
            + "&limit=" + str(limit)\
            + "&fields=" + adSetFields

    print("\nRequesting GET\n")
    Request = requests.get(url=CampaingAdSets)
    Headers = Request.headers
    Data = Request.json()
    parse = json.loads(Headers['x-business-use-case-usage'])[adAccountId][0]['estimated_time_to_regain_access'] if "error" in Data else 0

    print("Status: [200] OK\n") if str(Request) == '<Response [200]>' else print("Error:\n" + str(Data['error']['message']) + "\n")
    time.sleep(3)
    print(Headers)
    time.sleep(3)
    print("Estimated time to regain acess: " + str(parse) + " minutes") if "error" in Data and 'too many calls' in Data['error']['message'] else 0
    print(Data) if "error" not in Data else 0
    time.sleep(20)
    print(x+1)

















# GARBAGE CODE that may be useful at some point

# for x in range(0,len(campaings)):
#         print("")
#         print(campaings[x]['data'])
#         print("")
#         for c in campaings[x]['data']:
#             print("")
#             print(c)
#             print("")
# print(insights)

# campaingFields = config('CAMPAING_FIELDS')
# campaing_id = config('CAMPAING_ID')
# campaings = "https://graph.facebook.com/v10.0/"+ campaing_id\
#     + "/?date_preset=this_year&fields=" + campaingFields + "&access_token=" + token


# leads = "https://graph.facebook.com/v10.0/"+ adGroupId +"/leads?access_token=" + token