import os
import json
import requests
import time
import api
import random
import pandas as pd
import psycopg2
import sqlalchemy
import sheets
from decouple import config

# conn = psycopg2.connect(host=config('DATABASE_HOST'),database=config('DATABASE'), user=config('DATABASE_USER'), password=config('DATABASE_PASSWORD'))
# engine = sqlalchemy.create_engine(config('DATABASE_URI_TEST'))

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
Token = config('LONGTERM_TOKEN')

# api.setNewEnv()

# api.getActiveCampaingsNames(adAccountId)
campaingsNames = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_names_data.json')
campaingsNames = json.load(campaingsNames)

# api.getActiveCampaings(adAccountId)
campaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaings_data.json')
campaings = json.load(campaings)

# api.getAllCampaings(adAccountId)
allCampaings = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_all_campaings_data.json')
allCampaings = json.load(allCampaings)

# api.getActiveAdsets(adAccountId)
allAdsets = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_all_adset_data.json')
allAdsets = json.load(allAdsets)

# api.getActiveCampaingAdsets(adAccountId)
CampaingAdsets = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_campaing_adset_data.json')
CampaingAdsets = json.load(CampaingAdsets)

# api.getInsights(adAccountId)
insights = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_adset_insights_data.json')
insights = json.load(insights)

# api.getCustomAudiences(adAccountId)
CustomAudiences = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_custom_audiences.json')
CustomAudiences = json.load(CustomAudiences)

sheets.updateFacebookCustomAudience(SPREADSHEET_ID='1yo-rVFj91FxHk3AZ5quQuPsHITrv0LyLOqL1b4FQBVU',
                                    adAccountId=config('ADACCOUNT_ID2'),spreadsheet=config('SPREADSHEET'))

sheets.updateFacebookCustomAudience(SPREADSHEET_ID='1ZYJ_H2CY5xWOpaWI1gVwpB-zgNqJpYPcWTbrvBXnabk',
                                    adAccountId=config('ADACCOUNT_ID1'),spreadsheet=config('SPREADSHEET'))
