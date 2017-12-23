from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hpdf-secret-app'
from app import views
