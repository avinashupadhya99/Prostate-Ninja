from app import app
from flask import Flask, flash, request, redirect, url_for, render_template

@app.route('/')
def index():
    return render_template('index.html')
