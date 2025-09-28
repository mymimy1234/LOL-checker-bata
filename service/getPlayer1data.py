import requests

API_KEY = "RGAPI-56810c26-b2ee-4374-b120-47a89ea6c671"
ASIA_DOMAIN = "https://asia.api.riotgames.com"
KOREA_DOMAIN="https://kr.api.riotgames.com"
QUERY = "?api_key="+API_KEY
def getPuuidByGameNameTagLine(gameName, tagLine):
    path = "/riot/account/v1/accounts/by-riot-id/"+gameName + "/" + tagLine
    url = ASIA_DOMAIN + path + QUERY
    response = requests.get(url=url)
    if response.status_code != 200:
        print("사용자 정보를 불러오지 못했습니다.")
        exit()
    response = response.json()
    puuid = response['puuid']
    print(puuid)
    return puuid



def getMatchListByPuuid(puuid):
    match_path ="/lol/match/v5/matches/by-puuid/"+puuid +"/ids"
    match_query = "?api_key="+API_KEY
    match_url = ASIA_DOMAIN + match_path + match_query
    match_response = requests.get(url=match_url)
    return match_response.json()

def getMatchDetailsByMatchId(matchId):
    match_details_domain = "https://asia.api.riotgames.com"
    match_details_path = "/lol/match/v5/matches/" + matchId
    match_details_query = QUERY
    match_details_url = match_details_domain + match_details_path + match_details_query
    match_details_response = requests.get(url=match_details_url)
    match_details_response = match_details_response.json()
    info = match_details_response['info']
    return info

def getMatchData(gameName, tagLine):
    result2 = []
    puuid = getPuuidByGameNameTagLine(gameName, tagLine) #puuid 추출
    match_response = getMatchListByPuuid(puuid) #matchList추출
    if not match_response:
        print("최근 게임이 없습니다.")
        return False
    recent_1_matches = match_response[0] #가장 최근 matchId 추출
    info = getMatchDetailsByMatchId(recent_1_matches) #info 추출
    player1Gold = info['participants']
    player1CS = info['participants']
    player1EXP = info['participants']
    Playerinfo={}
    Playerinfo['goldEarned'] = player1Gold[i]['goldEarned']
    player1CS['totalMinionsKilled'] = player1CS[i]['totalMinionsKilled']
    player1EXP['champExperience'] = player1EXP[i]['champExperience']

    