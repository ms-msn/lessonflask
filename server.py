from datetime import datetime

from reg import get_weather

from flask import Flask, abort, request

city_id = 524901
apikey = '2e445bb44e9ad4dac0edbaf9ed9559b2'

app = Flask(__name__)


@app.route("/")
def index():
    url = "http://api.data.mos.ru/v1/datasets/2009/rows?api_key=%s" % apikey
    weather = get_weather(url)
    cur_date = datetime.now().strftime('%d.%m.%Y')

    # result = "<p><b>Температура:</b>%s</p>" % weather['main']['temp']
    # result += "<p><b>Город:</b></p>" % weather['name']
    result = "<p><b>Дата:</b>%s</p>" % cur_date
    result += "<table><tr><th>Имя</th><th>Кол-во</th><th>В каком году</th><tr>"
    for baby in weather:
        result += "<tr><th>%s</th><th>%s</th><th>%s</th><tr>" % ( baby['Cells']['Name'], baby['Cells']['NumberOfPersons'], baby['Cells']['Year'])
    result += "</table>"
    return result

@app.route("/news")
def all_the_news():
    limit = request.args.get('limit', 'all')
    limit = request.args.get('color', 'black')
    return '<h1 style="color: %s">News:  <small>%s</small></h1>' % (color, limit)

@app.route("/news/<int:news_id>")
def news_by_id(news_id):
    news_to_show = [news for news in all_news if news['id'] == news_id]
    if len(news_to_show) == 1:
        result = "<h1>%(title)s</h1><p><i>%(date)s</i><p>%(text)s</p>"
        return 'Новость: %s' % news_id
    else:
        abort(404)

@app.route("/names")
def names_by_year():
    url = "http://api.data.mos.ru/v1/datasets/2009/rows?api_key=%s" % apikey
    weather = get_weather(url)
    years = [2015, 2016, 2017]
    year = int(request.args.get('year')) if int(request.args.get('year')) in years else 2017
    print(year)
    result = "<table><tr><th>Имя</th><th>Кол-во</th><th>Месяц</th><th>В каком году</th><tr>"
    for baby in weather:
        if year == baby['Cells']['Year']:
            result += "<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><tr>" % ( baby['Cells']['Name'], baby['Cells']['NumberOfPersons'],baby['Cells']['Month'], baby['Cells']['Year'])
    result += "</table>"
    return result    


if __name__ == "__main__":

    app.run(debug=True)
