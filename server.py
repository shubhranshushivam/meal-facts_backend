from fileinput import filename
from urllib import response
from flask import Flask, jsonify, request, session
import requests
import math
from flask_cors import CORS
import sys
import json

temp = {}
# Initializing flask app
app = Flask(__name__)
CORS(app)


# Route for seeing a data

class DataStore():
    a = None


classData = DataStore()


@app.route('/getData', methods=['GET'])
def test1():
    x = classData.a

    print(x, file=sys.stderr)

    img = 'C:\\Users\\shubh\\Desktop\\Gitam_notes_sem7\\CSD-Coding\\project\\frontend\\meal\\public\\images\\'+x

    api_user_token = 'c0360369626d67778d5783ed5f31ac068e3eafa9'
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
        "X-RapidAPI-Key": "942e64e2a3msh1c36f02eb391e7dp16ffb9jsnad49626b1671",
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
    # session['fileName']=x
    print(data, file=sys.stderr)
    print(x, file=sys.stderr)
    test1()
    return {
        "data": x
    }
    # print(request.json['fileName'], file=sys.stderr)
    # fileName= request.json['fileName']
    # return {
    #     "fileName": filename
    # }
    # return jsonify({"Result"
    #                                +request.json['fileName']})


# def get_food():

    # image_file = request.args.get('fileName')
    # print(image_file)
    # return {
    #     'ok':'ok',
    #     'image':image_file
    # }

    # image_file = request.args.get('fileName')
    # print(request, file=sys.stderr)
    # print(image_file, file=sys.stderr)
    # return {
    #     "image_file":image_file
    # }

    # img = 'C:\\Users\\shubh\\Desktop\\Gitam_notes_sem7\\CSD-Coding\\project\\frontend\\backend\\burger.jpg'

    # api_user_token = 'c0360369626d67778d5783ed5f31ac068e3eafa9'
    # headers = {'Authorization': 'Bearer ' + api_user_token}

    # # Single/Several Dishes Detection
    # url = 'https://api.logmeal.es/v2/image/segmentation/complete'
    # resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)

    # # Nutritional information
    # url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
    # resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)

    # result = resp.json();
    # foodName="".join(result['foodName'][-1]).title()
    # calories=(math.ceil(result['nutritional_info']['calories']))

    # # Returning an api for showing in  reactjs
    # return {
    #     'Name':foodName,
    #     "Calories": calories,
    #     'fileName':image_file,
    #     }


# Running app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
