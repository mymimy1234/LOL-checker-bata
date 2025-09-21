import requests

API_KEY = "RGAPI-7e1ccdeb-ca17-4f2e-9104-2011be04e8b9"
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
    return puuid

def GetEncryptedPuuid(puuid):
    path = f"/lol/summoner/v4/summoners/by-puuid/"+puuid

    url = KOREA_DOMAIN + path + QUERY
    
   
    response = requests.get(url)
    if response.status_code != 200:
        print("소환사 정보를 불러오지 못했습니다.")
        exit()
    
    
    summoner_data = response.json()
    encrypted_puuid = summoner_data['puuid']
    return encrypted_puuid
    

def GetTier(encrypted_puuid):
    path=f"/lol/league/v4/entries/by-puuid/" + encrypted_puuid
    url= KOREA_DOMAIN+path+QUERY
    response = requests.get(url)
    print(response.text)
    response = response.json()
    tier = response[0]['tier']
    return tier

