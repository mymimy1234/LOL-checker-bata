import requests

API_KEY = "RGAPI-dd3c330f-8904-4b7e-82e9-6b360541b34b"
ASIA_DOMAIN = "https://asia.api.riotgames.com"
QUERY = "?api_key=" + API_KEY

def getPuuidByGameNameTagLine(gameName, tagLine):
    path = f"/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    url = ASIA_DOMAIN + path + QUERY
    response = requests.get(url=url)
    if response.status_code != 200:
        print("사용자 정보를 불러오지 못했습니다.")
        exit()
    response_json = response.json()
    return response_json['puuid']

def getMatchListByPuuid(puuid):
    match_path = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
    match_url = ASIA_DOMAIN + match_path + QUERY
    match_response = requests.get(url=match_url)
    return match_response.json()

def getMatchDetailsByMatchId(matchId):
    match_details_path = f"/lol/match/v5/matches/{matchId}"
    match_details_url = ASIA_DOMAIN + match_details_path + QUERY
    match_details_response = requests.get(url=match_details_url)
    return match_details_response.json()

def player1Data(gameName, tagLine):
    result2 = []
    puuid = getPuuidByGameNameTagLine(gameName, tagLine)
    match_response = getMatchListByPuuid(puuid)
    if not match_response:
        print("최근 게임이 없습니다.")
        return False
    
    recent_1_matches = match_response[0]
    info = getMatchDetailsByMatchId(recent_1_matches)['info']
    
    for participant in info['participants']: #10명 순회
        data = {} #한명의 데이터가 기록될
        data['goldEarned'] = participant['goldEarned']
        data['totalMinionsKilled'] = participant['totalMinionsKilled']
        data['champLevel'] = participant['champLevel']
        items = [] #한명의 아이템 들이 기록될....
        for i in range(7):
            items.append(participant[f'item{i}'])
        data['items'] = items
        result2.append(data)   
    return result2, puuid

result2, puuid = player1Data("Hide On Bush", "KR1")
print(result2)
