import requests
import pickle
# regions = ["br1","eun1","euw1","jp1","kr","la1","la2","na1","oc1","ru","tr1"]
# key = "RGAPI-876e9821-c0c3-482e-a43e-d18909e0f9fe"
# req = "https://{region}.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/I?page={page}"
# args = {"api_key" : key}
# def tier(tier,results):
#     for i in range(len(regions)):
#         for j in range(1,3):
#             try:
#                 res = requests.get(req.format(region = regions[i], tier = tier, page =j ), params=args)
#                 for entry in res.json():
#                     results.append([entry['summonerName'],regions[i]])
#             except:
#                 pass
#
# masters = []
# tier("GRANDMASTER",masters)
# with open('summoners_grandmaster2.pkl', 'wb') as f:
#     pickle.dump(masters, f)
#
# bronze = []
# tier("BRONZE",bronze)
# with open('summoners_bronze2.pkl', 'wb') as f:
#     pickle.dump(bronze, f)


time = "https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_5602047433/timeline"
key = "RGAPI-876e9821-c0c3-482e-a43e-d18909e0f9fe"
args = {"api_key" : key}
res = requests.get(time, params=args)
dict = res.json()
