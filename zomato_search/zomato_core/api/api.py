# import requests
#
# class API:
#     HOST = "https://developers.zomato.com/api/v2.1"
#     KEY = 'dd3fff93902a02d74d92adec2c748f46'
#
#     def __init__(self):
#         self.headers = {
#             "User-agent": "curl/7.43.0",
#             'Accept': 'application/json',
#             'X-Zomato-API-Key': self.KEY
#         }
#
#     def get(self, endpoint, params):
#         url = f'{self.HOST}{endpoint}'
#         response = requests.get(url, headers=self.headers, params=params)
#         return response.json()
from zomathon import ZomatoAPI

class API:

