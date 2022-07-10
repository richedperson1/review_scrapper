from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs

import oops_file as OF
# app = Flask(__name__)
app = Flask(__name__, template_folder='templets', static_folder='static')


@app.route("/", methods=['POST', 'GET'])
def home_page():
    return render_template("home.html")


@app.route("/jaiswal", methods=['POST', 'GET'])
def result_page():
    if request.method == 'POST':
        try:
            form_data = request.form['search_items'].lower().replace(" ", "")
            object_ = OF.fetching_info(form_data, "_1AtVbE col-12-12")
            title = object_.getting_info_of_one()
            All_info = object_.getting_info_of_all()
            # print(All_info)
            number = min(len(All_info[0]), len(
                All_info[1]), len(All_info[2]), len(All_info[3]))
            return render_template("result2.html", outputs={"title_of_page": title, "All_info": All_info, "total": number})
        except Exception as rpe:
            return(f"Error found at result page function 😩😩😩<br>{rpe}")

    return "Welcome to some update site"


def main():
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
