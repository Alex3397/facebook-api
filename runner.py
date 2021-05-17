import os
import json
import requests
import time
import api
import random
from decouple import config

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
Token = config('LONGTERM_TOKEN')

# api.getActiveCampaings(adAccountId)
campaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_data.json')
campaings = json.load(campaings)

# api.getActiveAdsets(adAccountId)
allAdsets = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_all_adset_data.json')
allAdsets = json.load(allAdsets)

# api.getActiveCampaingAdsets(adAccountId)
CampaingAdsets = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaing_adset_data.json')
CampaingAdsets = json.load(CampaingAdsets)

api.getInsights(adAccountId)
insights = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_insights_data.json')
insights = json.load(insights)

     



""" GARBAGE CODE that may be useful at some point

campaingFields = config('CAMPAING_FIELDS')
campaing_id = config('CAMPAING_ID')
campaings = "https://graph.facebook.com/v10.0/"+ campaing_id\
    + "/?date_preset=this_year&fields=" + campaingFields + "&access_token=" + token


leads = "https://graph.facebook.com/v10.0/"+ adGroupId +"/leads?access_token=" + token
"""