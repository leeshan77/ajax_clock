from flask import Flask, request, render_template, redirect

from flask_ckeditor import CKEditor

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 200

ckeditor = CKEditor(app)

@app.route('/')
def index():
    # return render_template("index.html")

    company_codes = ["005930", "000660", "005380"]
    # company_codes = ["005930"]

    # while True:
    prices = []
    for item in company_codes:
        now_price = get_price(item)
        prices.append(now_price)
        print(now_price)
    print("----------------------")

    # time.sleep(5)

    return render_template("index.html", content=prices)


def get_bsoup(company_code):
    url = "https://finance.naver.com/item/main.nhn?code=" + company_code

    result = requests.get(url)
    if result.status_code == 200:
        bs_obj = BeautifulSoup(result.content, "html.parser")
        return bs_obj
    else:
        print(result.status_code)


def get_price(company_code):
    bs_obj = get_bsoup(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})

    now_price = blind.text
    return now_price

@app.route('/hello')
def hellohtml():
    return render_template("hello.html", cke_type='standard')

@app.route('/method123', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        num = request.args["num"]
        name = request.args.get("name")
        return "GET으로 전달된 데이터({}, {})".format(num, name)
    else:
        num = request.form["num"]
        # num = request.form.get("num")
        text = request.form.get('ckeditor')
        return render_template('display.html', id=num, content=text)

@app.route('/clock')
def clock():
    return render_template("clock.html")

@app.route('/get_php')
def get_php():
    return render_template("get_php.html")

@app.route('/get_clock')
def get_clock():
    return render_template("get_clock.html")

@app.route('/naver')
def naver():
    return render_template("naver.html")

@app.route('/daum')
def daum():
    return redirect("https://www.daum.net/")

if __name__ == '__main__':
    app.run(debug=True)

