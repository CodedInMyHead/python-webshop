from flask import Flask

app = Flask(__name__)


@app.route("/<int:number>")
def get_pki(number):
    return "<p>Not found item with PKI " + number + "</p>"