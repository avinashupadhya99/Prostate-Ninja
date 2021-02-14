from app import app
from flask import Flask, flash, jsonify, request, redirect, url_for, render_template
from app.apiClient import *

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        age = int(request.form['age'])
        sex = request.form['sex']
        health = request.form['health']
        gender = GenderEnum.male if sex=='Male' else GenderEnum.female
        isHealthy = HealthyVolunteersEnum.healthy if health=='healthy' else HealthyVolunteersEnum.notHealthy
        apiClient = ApiClient()
        studies = apiClient.getTrialsFor(age = age, location=location, sex = gender, isHealthy = isHealthy)
        for study in studies:
            print(study.organization)
        return render_template('index.html', studies=studies)
    else:
        return render_template('index.html')


# @app.route('/result', methods=['POST'])
# def get_results():
#     age = int(request.form['age'])
#     sex = request.form['sex']
#     health = request.form['health']
#     gender = GenderEnum.male if sex=='Male' else GenderEnum.female
#     isHealthy = HealthyVolunteersEnum.healthy if health=='healthy' else HealthyVolunteersEnum.notHealthy
#     apiClient = ApiClient()
#     studies = apiClient.getTrialsFor(age = age, sex = gender, location = "", isHealthy = isHealthy)
#     for study in studies:
#         print(study.organization)
#     return render_template('result.html', studies=studies)


