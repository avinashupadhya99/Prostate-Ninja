from app import app
from flask import Flask, flash, jsonify, request, redirect, url_for, render_template
from app.apiClient import *

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def get_results():
    age = int(request.form['age'])
    sex = request.form['sex']
    health = request.form['health']
    gender = GenderEnum.male if sex=='Male' else GenderEnum.female
    isHealthy = HealthyVolunteersEnum.healthy if health=='healthy' else HealthyVolunteersEnum.notHealthy
    apiClient = ApiClient()
    studies = apiClient.getTrialsFor(age = age, sex = gender, isHealthy = isHealthy, location = "")
    for study in studies:
        print(f"Minimum Age: {study.minimumAge} --- Maximum Age: {study.maximumAge}")
    return render_template('result.html', studies=studies)

