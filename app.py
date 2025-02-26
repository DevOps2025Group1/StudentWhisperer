from flask import Flask
import dotenv

app = Flask(__name__)
dotenv.load_dotenv()

@app.route('/')
def index():
    return 'Hello, World!'

app.run()
