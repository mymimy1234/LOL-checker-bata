import requests

API_KEY = "RGAPI-56810c26-b2ee-4374-b120-47a89ea6c671"
ASIA_DOMAIN = "https://asia.api.riotgames.com"
KOREA_DOMAIN = "https://kr.api.riotgames.com"
QUERY = "?api_key=" + API_KEY

def getAccountInfo(gameName, tagLine):
    path = f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    url = ASIA_DOMAIN + path + QUERY
    response = requests.get(url=url)
    if response.status_code != 200:
        print("사용자 정보를 불러오지 못했습니다.")
        return None
    data = response.json()
    # data에는 puuid, id(encrypted summonerId), gameName, tagLine 등 포함됨
    return data

def getTier(encryptedSummonerId):
    path = f"/lol/league/v4/entries/by-puuid/{encryptedSummonerId}"
    url = KOREA_DOMAIN + path + QUERY
    response = requests.get(url)
    print(response.text)
    if response.status_code != 200:
        print("티어 정보를 불러오지 못했습니다.")
        return None
    data = response.json()
    # 솔로 랭크 정보 찾기 (예: queueType == "RANKED_SOLO_5x5")
    for entry in data:
        if entry['queueType'] == "RANKED_SOLO_5x5":
            print("RANKED_SOLO_5x5")
            print(entry['tier'])
            return entry['tier']
    return "UNRANKED"

# 사용 예시
info = getAccountInfo("someGameName", "someTagLine")
if info:
    tier = getTier(info['id'])
    print(f"티어: {tier}")
