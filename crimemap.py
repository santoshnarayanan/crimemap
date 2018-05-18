from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import dbconfig
import datetime
import dateparser
import string

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging','break-in']


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)



@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home1.html", crimes=crimes,categories=categories,error_message=error_message)
# The below lines of code is commented from chapter 6 implementation
# def home():
#     try:
#         data = DB.get_all_inputs()
#     except Exception as e:
#         print(e)
#         data = None
#     return render_template("home1.html", data=data)

# commented as below functions are not required at end of chapter 08
# @app.route("/add", methods=["POST"])
# def add():
#     try:
#         data = request.form.get("userinput")
#         DB.add_input(data)
#     except Exception as e:
#         print(e)
#     return home()
#
#
# @app.route("/clear")
# def clear():
#     try:
#         DB.clear_all()
#     except Exception as e:
#         print(e)
#     return home()


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()

    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")

    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except:
        error_message = "Latitude and Longitude have incorrect format"
        return home(error_message)

    description = sanitize_string(request.form.get("description"))
    DB.add_crime(category, date, latitude, longitude, description)
    return home()





# def format_date(userdate):
# date = dateparser.parse(userdate)
# try:
# return datetime.datetime.strftime(date, "%Y-%m-%d")
# except TypeError:
# return None


if __name__ == '__main__':
    app.run(port=5000, debug=True)