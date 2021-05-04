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

    print("Status: [200] OK") if str(longTokenRequest) == '<Response [200]>' else print(longTokenData['error']['message'])

    changeEnv('SHORT_TOKEN',longTermToken)
    changeEnv('LONGTERM_TOKEN',longTermToken)
    pass

def getAdsets(adAccountId,Token):
    limit = 150
    ad_sets = "https://graph.facebook.com/v10.0/act_" + adAccountId + "/adsets?access_token=" + Token\
        + "&date_preset=last_year"\
        + "&fields=id,name,optimization_goal,multi_optimization_goal_weight,configured_status,effective_status,"\
        + "billing_event,bid_amount,daily_budget,campaign_id,targeting,status,start_time,end_time,asset_feed_id,"\
        + "adlabels,attribution_spec,bid_adjustments,bid_constraints,bid_info,bid_strategy,budget_remaining,"\
        + "created_time,creative_sequence,daily_min_spend_target,ads,activities,ad_studies,copies,"\
        + "daily_spend_cap,destination_type,frequency_control_specs,instagram_actor_id,is_dynamic_creative,"\
        + "issues_info,learning_stage_info,lifetime_budget,lifetime_imps,lifetime_min_spend_target,"\
        + "lifetime_spend_cap,optimization_sub_event,pacing_type,promoted_object,recommendations,"\
        + "recurring_budget_semantics,review_feedback,rf_prediction_id,source_adset,source_adset_id,"\
        + "time_based_ad_rotation_id_blocks,time_based_ad_rotation_intervals,updated_time,use_new_app_click,"\
        + "delivery_estimate,adcreatives,adrules_governed,asyncadrequests,targetingsentencelines"\
        + "&limit=" + str(limit)
    
    print("Requesting GET")
    Request = requests.get(url=ad_sets)
    Data = Request.json()
    print("Status: [200] OK") if str(Request) == '<Response [200]>' else print(Data['error']['message'])
    print(Data) if "error" not in Data else 0
    
    
    
    pass

# setNewEnv()

adaccountid = config('ADACCOUNT_ID')
adgroupid = config('ADGROUP_ID')
token = config('LONGTERM_TOKEN')

getAdsets(adaccountid,token)

# contextual_bundling_spec nao funciona se usuario nao estiver na lista branca
# CAMPOS ADSET:
# id,name,optimization_goal,multi_optimization_goal_weight,configured_status,effective_status
# billing_event,bid_amount,daily_budget,campaign,targeting,status,start_time,end_time,asset_feed_id,
# adlabels,attribution_spec,bid_adjustments,bid_constraints,bid_info,bid_strategy,budget_remaining,
# created_time,creative_sequence,daily_min_spend_target,ads,activities,ad_studies,copies,
# daily_spend_cap,destination_type,frequency_control_specs,instagram_actor_id,is_dynamic_creative,
# issues_info,learning_stage_info,lifetime_budget,lifetime_imps,lifetime_min_spend_target,
# lifetime_spend_cap,optimization_sub_event,pacing_type,promoted_object,recommendations,
# recurring_budget_semantics,review_feedback,rf_prediction_id,source_adset,source_adset_id,
# time_based_ad_rotation_id_blocks,time_based_ad_rotation_intervals,updated_time,use_new_app_click,
# delivery_estimate,adcreatives,adrules_governed,asyncadrequests,targetingsentencelines

leads = "https://graph.facebook.com/v10.0/"+ adgroupid +"/leads?access_token=" + token
ads_volume = "https://graph.facebook.com/v10.0/act_" + adaccountid + "/ads_volume?access_token=" + token
insights = "https://graph.facebook.com/v10.0/" + "/insights"
insightsFields = "account_currency,account_id,account_name,action_values,actions,activity_recency"\
    +",ad_click_actions,ad_format_asset,ad_id,ad_impression_actions,ad_name,adset_id,adset_name,age_targeting"\
    +",attribution_setting,auction_bid,auction_competitiveness,auction_max_competitor_bid,body_asset,buying_type"\
    +",campaign_id,campaign_name,canvas_avg_view_percent,canvas_avg_view_time,catalog_segment_actions"\
    +",catalog_segment_value,catalog_segment_value_mobile_purchase_roas,catalog_segment_value_omni_purchase_roas"\
    +",catalog_segment_value_website_purchase_roas,clicks,comparison_node,conversion_values,conversions"\
    +",converted_product_quantity,converted_product_value,cost_per_15_sec_video_view"\
    +",cost_per_2_sec_continuous_video_view,cost_per_action_type,cost_per_ad_click,cost_per_conversion"\
    +",cost_per_dda_countby_convs,cost_per_inline_link_click,cost_per_inline_post_engagement"\
    +",cost_per_one_thousand_ad_impression,cost_per_outbound_click,cost_per_store_visit_action,cost_per_thruplay"\
    +",cost_per_unique_action_type,cost_per_unique_click,cost_per_unique_conversion,cost_per_unique_inline_link_click"\
    +",cost_per_unique_outbound_click,country,cpc,cpm,cpp,created_time,ctr,date_start,date_stop,dda_countby_convs,"\
    +"dda_results,description_asset,device_platform,dma,estimated_ad_recall_rate_lower_bound,"\
    +"estimated_ad_recall_rate_upper_bound,estimated_ad_recallers_lower_bound,estimated_ad_recallers_upper_bound,"\
    +"frequency,frequency_value,full_view_impressions,full_view_reach,gender_targeting,"\
    +"hourly_stats_aggregated_by_advertiser_time_zone,hourly_stats_aggregated_by_audience_time_zone,image_asset,"\
    +"impression_device,impressions,impressions_dummy,inline_link_click_ctr,inline_link_clicks,inline_post_engagement,"\
    +"instant_experience_clicks_to_open,instant_experience_clicks_to_start,instant_experience_outbound_clicks,"\
    +"interactive_component_tap,labels,location,media_asset,mobile_app_purchase_roas,objective,optimization_goal,"\
    +"outbound_clicks,outbound_clicks_ctr,place_page_id,place_page_name,platform_position,product_id,"\
    +"publisher_platform,purchase_roas,qualifying_question_qualify_answer_rate,reach,rule_asset,social_spend,"\
    +"spend,store_visit_actions,title_asset,unique_actions,unique_clicks,unique_conversions,unique_ctr,"\
    +"unique_inline_link_click_ctr,unique_inline_link_clicks,unique_link_clicks_ctr,unique_outbound_clicks,"\
    +"unique_outbound_clicks_ctr,unique_video_view_15_sec,updated_time,video_15_sec_watched_actions,"\
    +"video_30_sec_watched_actions,video_asset,video_avg_time_watched_actions,video_continuous_2_sec_watched_actions,"\
    +"video_p100_watched_actions,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,"\
    +"video_p95_watched_actions,video_play_actions,video_play_curve_actions,video_play_retention_0_to_15s_actions,"\
    +"video_play_retention_20_to_60s_actions,video_play_retention_graph_actions,video_time_watched_actions,"\
    +"website_ctr,website_purchase_roas,wish_bid"

# stored = []
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