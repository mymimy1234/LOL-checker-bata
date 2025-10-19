import requests
import time
import pandas as pd

API_KEY = "RGAPI-c9e81776-87c5-4c55-8077-bf6274769316"
ASIA_DOMAIN = "https://asia.api.riotgames.com"
KR_DOMAIN = "https://kr.api.riotgames.com"
PATH = "/lol/league/v4/entries/"

TIER = ["IRON","BRONZE","SILVER","GOLD","PLATINUM","EMERALD","DIAMOND","MASTER","GRANDMASTER","CHALLENGER"]  # 테스트용
DIVISION = ["I", "II", "III", "IV"]
QUEUE = "RANKED_SOLO_5x5"

def get_puuids_by_tier(tier):
    path2 = PATH+QUEUE+"/"+tier+"/"+DIVISION[0]  # 예: GOLD I
    url = KR_DOMAIN+path2+"?page=1&api_key="+API_KEY
    puuids = []
    try:
        response = requests.get(url=url)
        response = response.json()
        print(response)
        for data in response:
            puuids.append(data['puuid'])
    except Exception as e:
        print("Error in get_puuids_by_tier:", e)
    return puuids

def get_gold_info_by_puuids(puuids):
    cnt = 0
    golds = []
    for puuid in puuids:
        time.sleep(1)  # API 제한 맞추기

        # 최근 1개 랭크 매치 ID 가져오기
        path = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        query = f"?start=0&count=1&type=ranked&api_key={API_KEY}"
        url = ASIA_DOMAIN + path + query

        try:
            response = requests.get(url=url)
            match_ids = response.json()
        except Exception as e:
            print("Error fetching match IDs:", e)
            continue
        
        if not match_ids:
            continue
        
        try:
            match_id = match_ids[0]
        except KeyError:
            print("match_ids 리스트가 비어 있습니다.")
            match_id = None  # 또는 다른 기본값



        # 매치 상세 정보
        path = f"/lol/match/v5/matches/{match_id}"
        query = f"?api_key={API_KEY}"
        url = ASIA_DOMAIN + path + query

        time.sleep(1)

        try:
            response = requests.get(url=url)
            match_data = response.json()

            participants = match_data['info']['participants']

            for participant in participants:
                
                if participant.get('teamPosition') == 'UTILITY' or participant.get('lane') == 'SUPPORT':
                    kills = participant.get('kills', 0)
                    deaths = participant.get('deaths', 0)
                    assists = participant.get('assists', 0)
                    gold_earned = participant.get('goldEarned', 0)
                    vision_score = participant.get('visionScore', 0)
                    detector_wards_placed = participant.get('detectorWardsPlaced', 0)

                    golds.append({
                        'puuid': puuid,
                        'kills': kills,
                        'deaths': deaths,
                        'assists': assists,
                        'goldEarned': gold_earned,
                        'visionScore': vision_score,
                        'detectorWardsPlaced': detector_wards_placed
                    })
                    break  

            cnt += 1
            if cnt >= 10:  
                break

        except Exception as e:
            print("Error fetching match data:", e)
            continue

    return golds

final_df = pd.DataFrame()

for tier in TIER:
    puuids = get_puuids_by_tier(tier)
    golds = get_gold_info_by_puuids(puuids)
    tier_df = pd.DataFrame(golds)
    tier_df['tier'] = tier
    final_df = pd.concat([final_df, tier_df], ignore_index=True)


final_df.to_excel('golds_by_tier.xlsx', index=False)
