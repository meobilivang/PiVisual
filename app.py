from flask import Flask, jsonify

from utils import aggregate_metrics

app = Flask(__name__)


@app.route("/")
def main():
    return "Hello world!"


@app.route("/api/metrics")
def metrics():
    res = aggregate_metrics()

    return jsonify(res)


@app.route("/dashboard")
def dash_board():
    return
