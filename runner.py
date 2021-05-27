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


for page in range(len(allCampaings)):
    for x in range(len(allCampaings[page]['data'])):
        campaing = allCampaings[page]['data'][x]
        for i in campaing:
            if type(campaing[i]) == str or type(campaing[i]) == int or type(campaing[i]) == bool:
                    baseDF[i] = []

            elif type(campaing[i]) == list:
                if len(campaing[i]) == 0:
                    baseDF[i] = ''
                else:
                    for n in range(len(campaing[i])):
                        print(campaing[i])
                        listDF[i] = []
                        
            elif type(campaing[i]) == dict:
                if len(campaing[i]) == 0:
                    baseDF[i] = []
                else:
                    if 'source_campaign' not in i:
                        if len(campaing[i]['data']) == 1:
                            for l in campaing[i]['data'][0]:
                                baseDF[l] = ''
                        else:
                            for k in range(len(campaing[i]['data'])):
                                for d in campaing[i]['data'][k]:
                                    dictDF[d] = []
                    else:
                        pass
                    pass
                pass

for page in range(len(allCampaings)):
    for x in range(len(allCampaings[page]['data'])):
        campaing = allCampaings[page]['data'][x]
        print("Campaing: " + str(x) + "\n")
        a = 0

        for i in campaing:
            print("\nColumn: " + str(i))
            print(str(campaing[i]) + "\n") if type(campaing[i]) != dict and type(campaing[i]) != list else 0
            
            if type(campaing[i]) == bool or type(campaing[i]) == str or type(campaing[i]) == int:
                if i not in baseDF:
                    baseDF[i] = [campaing[i]]
                else:
                    baseDF.loc[x,i] = campaing[i]
                Bool += 1 if type(campaing[i]) == bool else 0
                Str += 1 if type(campaing[i]) == str else 0
                Int += 1 if type(campaing[i]) == int else 0
                pass

            elif type(campaing[i]) == dict:
                if len(campaing[i]) == 0:
                    baseDF.loc[x,i] = campaing[i]
                    Dict_emp += 1
                else:
                    if i != 'source_campaign':
                        if len(campaing[i]['data']) == 1:
                            for l in campaing[i]['data'][0]:
                                baseDF.loc[x,l] = campaing[i]['data'][0][l]
                        else:
                            for k in range(len(campaing[i]['data'])):
                                for d in campaing[i]['data'][k]:
                                    print(campaing[i]['data'][k][d])
                                    dictDF.loc[k,i] = [campaing[i]['data'][k][d]]
                    else:
                        pass
                    pass
                Dict +=1
                pass

            elif type(campaing[i]) == list:
                if len(campaing[i]) == 0:
                    baseDF.loc[x,i] = campaing[i] if campaing[i] != [] else ''
                    List_emp += 1
                else:
                    for n in range(len(campaing[i])):
                        print(campaing[i][n])
                        listDF.loc[x,i] = [campaing[i][n]]
                    pass
                List += 1
                pass

            else:
                unidentifiedClass.append(type(campaing[i]))
                pass

            a += 1
    name = str(config('ADACCOUNT_ID2')) + "_all_campaing_data"
    baseDF.to_sql(name=name,con=engine,schema='public',if_exists='replace',index=False,method='multi') if page == 0 else 0
    baseDF.to_sql(name=name,con=engine,schema='public',if_exists='append',index=False,method='multi') if page != 0 else 0
    print("\nCampaing " + str(x) + " Column count: " + str(a) + "\n")
print("\nCampaings count: " + str(x+1))
print("List Count: " + str(List))
print("Empty List Count: " + str(List_emp))
print("Dict Count: " + str(Dict))
print("Empty Dict Count: " + str(Dict_emp))
print("Str Count: " + str(Str))
print("Int Count: " + str(Int))
print("Bool Count: " + str(Bool))
print("Unidentified Classes: " + str(unidentifiedClass) + "\n")
print("Base DF: ")
print(baseDF)

name = str(config('ADACCOUNT_ID2')) + "_all_campaing_data"
databaseDF = pd.read_sql_table(table_name=name,con=engine,schema='public')
print(databaseDF)
# baseDF.to_sql(name=name,con=engine,schema='public',if_exists='replace',index=False,method='multi')

""" GARBAGE CODE that may be useful at some point

leads = "https://graph.facebook.com/v10.0/"+ adGroupId +"/leads?access_token=" + token
"""