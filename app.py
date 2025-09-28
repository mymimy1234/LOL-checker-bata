from flask import Flask, request, render_template

from service.getMatchData import getMatchData
from service.getTierData import getTier

app = Flask(__name__)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        gameName = request.form['gameName']
        tagLine = request.form['tagLine']
        result, puuid = getMatchData(gameName, tagLine)
        tier = getTier(puuid)  # 함수명 소문자 통일
        return render_template(
            'search.html',
            playerName=gameName,
            playerTagLine=tagLine,
            playerTier=tier,
            result=result
        )
    else:
        return render_template('search.html')


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")


