import os
import json
import requests
import time
import api
from decouple import config

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
token = config('LONGTERM_TOKEN')

campaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_data.json')
campaings = json.load(campaings)

adset = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_data.json')
adset = json.load(adset)

# for x in campaings['data']:
#     print(x)

# api.getActiveAdsets(adAccountId)




















# GARBAGE CODE that may be useful at some point


# campaingFields = config('CAMPAING_FIELDS')
# campaing_id = config('CAMPAING_ID')
# campaings = "https://graph.facebook.com/v10.0/"+ campaing_id\
#     + "/?date_preset=this_year&fields=" + campaingFields + "&access_token=" + token


# leads = "https://graph.facebook.com/v10.0/"+ adGroupId +"/leads?access_token=" + token