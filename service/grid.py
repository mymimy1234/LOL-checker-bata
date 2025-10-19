import requests
import time
import pandas as pd

API_KEY = "RGAPI-c9e81776-87c5-4c55-8077-bf6274769316"
ASIA_DOMAIN = "https://asia.api.riotgames.com"
KR_DOMAIN = "https://kr.api.riotgames.com"
PATH = "/lol/league/v4/entries/"

TIER = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"]
DIVISION = ["I", "II", "III", "IV"]
QUEUE = "RANKED_SOLO_5x5"

def get_puuids_by_tier_and_division(tier, division, count=10):
    puuids = []
    page = 1

    while len(puuids) < count:
        url = f"{KR_DOMAIN}{PATH}{QUEUE}/{tier}/{division}?page={page}&api_key={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if not data:
                break  # 더 이상 데이터 없으면 중단

            for entry in data:
                puuids.append(entry['puuid'])
                if len(puuids) >= count:
                    break
            page += 1
            time.sleep(1)  # API 호출 제한 대비 딜레이
        except Exception as e:
            print(f"Error fetching puuids for {tier} {division} page {page}: {e}")
            break

    return puuids[:count]

def get_puuids_by_tier(tier, count=10):
    puuids = []
    if tier in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
        if tier == "MASTER":
            url = f"{KR_DOMAIN}/lol/league/v4/masterleagues/by-queue/{QUEUE}?api_key={API_KEY}"
        elif tier == "GRANDMASTER":
            url = f"{KR_DOMAIN}/lol/league/v4/grandmasterleagues/by-queue/{QUEUE}?api_key={API_KEY}"
        else:  # CHALLENGER
            url = f"{KR_DOMAIN}/lol/league/v4/challengerleagues/by-queue/{QUEUE}?api_key={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for entry in data.get('entries', []):
                puuids.append(entry['puuid'])
                if len(puuids) >= count:
                    break
            time.sleep(1)
        except Exception as e:
            print(f"리그에서 PUUID데이터를 가져오는데 실패했습니다. {tier}: {e}")
        print(f"PUUIDS {tier}: {puuids}")
    return puuids[:count]

def get_gold_info_by_puuids(puuids):
    golds = []
    cnt = 0

    for puuid in puuids:
        time.sleep(1)

        # 매치 아이디 가져오기
        url = f"{ASIA_DOMAIN}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1&type=ranked&api_key={API_KEY}"
        try:
            response = requests.get(url)
            print(f"MATCH RESPONSE STATUS CODE: {response.status_code}")
            response.raise_for_status()
            match_ids = response.json()
        except Exception as e:
            print(f"매치아이디를 가져오는 중 오류가 발생했습니다. {puuid}: {e}")
            continue

        if not match_ids:
            continue

        match_id = match_ids[0]

        # 매치 상세 데이터 가져오기
        url = f"{ASIA_DOMAIN}/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
        time.sleep(1)
        try:
            print(f"탐색할 매치 아이디: {match_id}")
            response = requests.get(url)
            print(f"매치 아이디 status code: {response.status_code}")
            response.raise_for_status()
            match_data = response.json()

            participants = match_data['info']['participants']

            for participant in participants:
                if participant.get('teamPosition') == 'UTILITY' or participant.get('lane') == 'SUPPORT':
                    golds.append({
                        'puuid': puuid,
                        'kills': participant.get('kills', 0), 
                        'deaths': participant.get('deaths', 0),
                        'assists': participant.get('assists', 0),
                        'goldEarned': participant.get('goldEarned', 0),
                        'visionScore': participant.get('visionScore', 0),
                        'detectorWardsPlaced': participant.get('detectorWardsPlaced', 0)
                    })
                    break

            cnt += 1
            if cnt >= 10:
                break
        except Exception as e:
            print(f"Error fetching match data for match {match_id}: {e}")
            continue

    return golds
"""
# 마스터 이상 티어 처리
for tier in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
    print(f"Processing tier: {tier}")
    puuids = get_puuids_by_tier(tier, count=10)
    golds = get_gold_info_by_puuids(puuids)
    if golds:
        tier_df = pd.DataFrame(golds)
        tier_df['tier'] = tier
        tier_df.to_excel(f'{tier}_golds.xlsx', index=False)
        print(f"Saved {tier}_golds.xlsx")
"""

# 일반 티어 및 디비전별 처리
for tier in TIER:
    for division in DIVISION:
        print(f"Processing tier: {tier}, division: {division}")
        puuids = get_puuids_by_tier_and_division(tier, division, count=100)
        golds = get_gold_info_by_puuids(puuids)
        if golds:
            tier_div_df = pd.DataFrame(golds)
            tier_div_df['tier'] = tier
            tier_div_df['division'] = division
            filename = f'{tier}_{division}golds.xlsx'
            tier_div_df.to_excel(filename, index=False)
            print(f"Saved {filename}")
