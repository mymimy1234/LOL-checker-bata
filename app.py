from flask import Flask, request, render_template

from service.getMatchData import getMatchData
from service.getTierData import GetTier
app = Flask(__name__)

@app.route('/')
def hello_world():  #Route 함수
    return 'Hello, World!'

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        gameName = request.form['gameName']
        tagLine = request.form['tagLine']
        result,puuid = getMatchData(gameName, tagLine)
        tier = GetTier(puuid)
        summoner_name=gameName+"#"+tagLine
        return render_template('search.html',summoner_name=summoner_name,result=result,tier=tier)
    if request.method == 'GET':
        return render_template('search.html')



if __name__ == '__main__':
    app.run(port=8000,host = "0.0.0.0")