from flask import Flask, jsonify, render_template, redirect, url_for
from utils import MetricsUtils
from config import config

app = Flask(__name__)
app.config.from_object(config)
metrics_utils = MetricsUtils()


@app.route("/")
def main():
    return redirect(url_for("dash_board"))


@app.route("/api/metrics")
def metrics():
    data = metrics_utils.aggregate_metrics()

    return jsonify(data)


@app.route("/api/machine-info")
def machine_info():
    data = metrics_utils.collect_machine_info()

    return jsonify(data)


@app.route("/dashboard")
def dash_board():
    system_info = metrics_utils.collect_machine_info()
    metrics = metrics_utils.aggregate_metrics()

    return render_template("dashboard.html", system_info=system_info, metrics=metrics)
