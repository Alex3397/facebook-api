import os
import json
import requests
import time
import api
import random
import pandas as pd
import psycopg2
import sqlalchemy
from decouple import config

conn = psycopg2.connect(host=config('DATABASE_HOST'),database=config('DATABASE'), user=config('DATABASE_USER'), password=config('DATABASE_PASSWORD'))
engine = sqlalchemy.create_engine(config('DATABASE_URI_TEST'))

adAccountId = config('ADACCOUNT_ID2')
adGroupId = config('ADGROUP_ID')
Token = config('LONGTERM_TOKEN')

# api.setNewEnv()

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

List = 0
List_emp = 0
Dict = 0
Dict_emp = 0
Str = 0
Int = 0
Bool = 0
unidentifiedClass = []
baseDF = pd.DataFrame()
listDF = pd.DataFrame()
dictDF = pd.DataFrame()


for page in range(len(allAdsets)):
    for x in range(len(allAdsets[page]['data'])):
        print(x)
        sub_dict = allAdsets[page]['data'][x]
        for item in sub_dict:
            print("\n" + str(item) + " " + str(type(sub_dict[item])) + "\n")

            if type(sub_dict[item]) == bool \
                or type(sub_dict[item]) == str \
                or type(sub_dict[item]) == int:
                if item not in baseDF:
                    baseDF[item] = [sub_dict[item]]

            
            elif type(sub_dict[item]) == list and len(sub_dict[item]) == 0:
                baseDF[item] = [sub_dict[item]]
            
            elif type(sub_dict[item]) == list and len(sub_dict[item]) > 0:
                for listInt in range(len(sub_dict[item])):
                    listDF[item] = [sub_dict[item]]

            elif type(sub_dict[item]) == dict and len(sub_dict[item]) == 0:
                baseDF[item] = [sub_dict[item]]
                
            # DELIVERY_ESTIMATE AND ADCREATIVES START
            elif type(sub_dict[item]) == dict and len(sub_dict[item]) > 0:
                if 'data' in sub_dict[item]:
                    for x in range(len(sub_dict[item]['data'])):
                        for sub_item in sub_dict[item]['data'][x]:
                            if type(sub_dict[item]['data'][x][sub_item]) == list:
                                for day in range(len(sub_dict[item]['data'][x][sub_item])):
                                    for key in sub_dict[item]['data'][x][sub_item][day]:
                                        dictDF[key] = [sub_dict[item]['data'][x][sub_item][day][key]]
                            else:
                                dictDF[sub_item] = [sub_dict[item]['data'][x][sub_item]]
            # DELIVERY_ESTIMATE AND ADCREATIVES fINISH
                else:
            # TARGETING AND TARGETINGSETENCELINES START
                    for sub_item in sub_dict[item]:
                        if type(sub_dict[item][sub_item]) == int \
                            or type(sub_dict[item][sub_item]) == str:
                            print(str(sub_item) + ": " + str(sub_dict[item][sub_item]))
                            baseDF[sub_item] = [sub_dict[item][sub_item]]

                        elif type(sub_dict[item][sub_item]) == dict:
                            for key in sub_dict[item][sub_item]:
                                
                                if type(sub_dict[item][sub_item][key]) == list:
                                    for listInt in range(len(sub_dict[item][sub_item][key])):
                                        print(str(key) + ": " + str(sub_dict[item][sub_item][key][listInt]))
                                        listDF[key] = [sub_dict[item][sub_item][key][listInt]]

                        elif type(sub_dict[item][sub_item]) == list:
                            for listInt in range(len(sub_dict[item][sub_item])):

                                if type(sub_dict[item][sub_item][listInt]) == dict:
                                    for listItem in sub_dict[item][sub_item][listInt]:
                                        if type(sub_dict[item][sub_item][listInt][listItem]) == str:
                                            column = str(sub_dict[item][sub_item][listInt][listItem])

                                        elif type(sub_dict[item][sub_item][listInt][listItem]) == list and listItem != 'interests':
                                            for subListInt in range(len(sub_dict[item][sub_item][listInt][listItem])):
                                                print(column + " " + str(sub_dict[item][sub_item][listInt][listItem][subListInt]))
                                                listDF[column.replace(':','')] = [sub_dict[item][sub_item][listInt][listItem][subListInt]]
                                        
                                else:
                                    print(str(sub_item) + ": " + str(sub_dict[item][sub_item][listInt]))
                                    listDF[sub_item] = [sub_dict[item][sub_item][listInt]]
                        

print("\n" + str(baseDF))
print(listDF)
print(dictDF)