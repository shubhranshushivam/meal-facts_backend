from flask import Flask, request
import requests
import math
from flask_cors import CORS
import sys
import json
from flask_mysqldb import MySQL

temp = {}
# Initializing flask app
app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meal_fact'
mysql = MySQL(app)



# Route for seeing a data

class DataStore():
    a = None


class UserData():
    userName= None
    userEmail= None
    userImage = None
    loginDate = None


classData = DataStore()


@app.route('/getData', methods=['GET'])
def test1():
    x = classData.a

    print(x, file=sys.stderr)

    img = 'C:\\Users\\shubh\\Desktop\\Gitam_notes_sem7\\CSD-Coding\\project\\frontend\\meal\\public\\images\\'+x

    api_user_token = 'API_TOKEN'
    headers = {'Authorization': 'Bearer ' + api_user_token}

    # Single/Several Dishes Detection
    url = 'https://api.logmeal.es/v2/image/segmentation/complete'
    resp = requests.post(
        url, files={'image': open(img, 'rb')}, headers=headers)

    print(resp.json()['imageId'], file=sys.stderr)

    # Nutritional information
    url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
    resp = requests.post(url, json={'imageId': resp.json()['imageId']}, headers=headers)

    result = resp.json()
    foodName = "".join(result['foodName'][-1]).title()
    calories = (math.ceil(result['nutritional_info']['calories']))


    # recipe
    url = "https://tasty.p.rapidapi.com/recipes/list"

    query=foodName

    querystring = {"from":"0","size":"1","q":query}

    headers = {
        "X-RapidAPI-Key": "API_TOKEN",
        "X-RapidAPI-Host": "tasty.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    val=""
    try:
        xVal= len(response.json()['results'][0]['recipes'][0]['instructions'])
        for i in range(xVal):
            val+=' '+response.json()['results'][0]['recipes'][0]['instructions'][i]['display_text']

    except:
        xVal= len(response.json()['results'][0]['instructions'])
        for i in range(xVal):
            val+=' '+response.json()['results'][0]['instructions'][i]['display_text']


    # Returning an api for showing in  reactjs
    return {
        'name': foodName,
        "calories": calories,
        "image": x,
        "recipe":val,
    }




@app.route('/data', methods=['GET', 'POST'])
def test():
    data = request.get_json()
    x = (data['fileName'])
    classData.a = x
    print(data, file=sys.stderr)
    print(x, file=sys.stderr)
    test1()
    return {
        "data": x
    }
   

loginData = UserData()

@app.route('/login', methods=['POST'])
def test2():
    data=request.get_json()
    print(data, file=sys.stderr)
    loginData.userName = data['userName']
    loginData.userEmail = data['userEmail']
    if(loginData.userEmail=='undefined'):
        return
    loginData.userImage = data['userImage']
    loginData.loginDate = data['date']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO login_log VALUES(%s,%s, %s, %s)''',(loginData.userName,loginData.userEmail, loginData.userImage, loginData.loginDate))
    mysql.connection.commit()
    cursor.close()


# Running app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
