import getAdGroups
from decouple import config
from google.oauth2 import service_account
from google.ads.googleads.client import GoogleAdsClient

SCOPES = ['https://www.googleapis.com/auth/adwords']
SERVICE_ACCOUNT_FILE = config('PATH_TO_ADS_SERVICE_JSON')
customer_id = config('CUSTOMER_ID')

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

client = GoogleAdsClient(credentials=credentials,developer_token=config('DEVELOPER_TOKEN'))
service = client.get_service("CustomAudienceService")
audience = client.get_type("GetCustomAudienceRequest")
print(service)
print(audience)

campaign_id=12777026566
ga_service = client.get_service("GoogleAdsService")

query = """
    SELECT
        campaign.id,
        ad_group.id,
        ad_group.name
    FROM ad_group"""

if campaign_id:
    query += f" WHERE campaign.id = {campaign_id}"

search_request = client.get_type("SearchGoogleAdsRequest")
search_request.customer_id = customer_id
search_request.query = query

results = ga_service.search(request=search_request)

print(results)