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
    result = []
    puuid = getPuuidByGameNameTagLine(gameName, tagLine) #puuid 추출
    match_response = getMatchListByPuuid(puuid) #matchList추출
    if not match_response:
        print("최근 게임이 없습니다.")
        return False
    recent_1_matches = match_response[0] #가장 최근 matchId 추출
    info = getMatchDetailsByMatchId(recent_1_matches) #info 추출
    
    participants = info['participants']
    KDA = info['participants']
    TotalDamageDealtToChampions = info['participants']
    TotalDamageTaken = info['participants']
    TotalTime = info['gameDuration']
    print("총 게임 시간:", TotalTime//60, "분", TotalTime%60, "초")
    visionScore=info['participants']
    WardPlaced = info['participants']
    WardDestroyed = info['participants']
    for i in range(10):
        item = {}
        item['championName'] = participants[i]['championName']
        item['kills'] = KDA[i]['kills']
        item['deaths'] = KDA[i]['deaths']
        item['assists'] = KDA[i]['assists']
        item['totalDamageDealtToChampions'] = TotalDamageDealtToChampions[i]['totalDamageDealtToChampions']
        item['totalDamageTaken'] = TotalDamageTaken[i]['totalDamageTaken']
        item['visionScore'] = visionScore[i]['visionScore']
        item['wardsPlaced'] = WardPlaced[i]['wardsPlaced']
        item['wardsDestroyed'] = WardDestroyed[i]['wardsKilled']
        result.append(item)
    return result, puuid
    
"""
    for p in participants:
        if p['puuid'] == puuid:
            if p['win']:
                print(f"\n✅ {gameName}님은 해당 경기에서 승리했습니다.")
            else:
                print(f"\n❌ {gameName}님은 해당 경기에서 패배했습니다.")
            break


    ChampionId = info['participants']
    for i in range(10):
        championId = ChampionId[i]['championId']
        champion_image_url = f"http://ddragon.leagueoflegends.com/cdn/13.6.1/img/champion/{ChampionId[i]['championName']}.png"
        image_response = requests.get(champion_image_url)
        if image_response.status_code == 200:
            with open(f"{ChampionId[i]['championName']}.png", "wb") as f:
                f.write(image_response.content)
            img = Image.open(f"{ChampionId[i]['championName']}.png")
            img.show()
        else:
            print(f"이미지 로딩 실패")




            pDRI_rmEXKfJpSagCPi_nawWiv3CwSjDmNtu6WJ6ISzvmdJeXiDtWoYUvOltYf_TMPDnwJD7sGI55A
"""



