import requests
import json
page = requests.get('https://api.hellopeter.com/consumer/business/telkom/reviews/appalling-service-cdc4559e8084e0db01dd6d7e807875460607ac77-2851593')
jsondata=json.loads(page.text)
print(jsondata['review_content'])