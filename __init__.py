from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '524fh9032ofhn4o3nv'  # Secret key for generating tokens that prevent csrf
