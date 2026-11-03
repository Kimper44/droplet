from flask import Flask

app = Flask(__name__)


@app.get("/")
def hello():
    return "Server is up and running"


app.run(host="0.0.0.0", port=8000)
