from flask import Flask, jsonify, render_template

from utils import MetricsUtils
from config import config


def create_app():

    app = Flask(__name__)

    app.config.from_object(config)

    metrics_utils = MetricsUtils()

    @app.route("/")
    def main():
        return "Hello world!"

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

        return render_template(
            "dashboard.html", system_info=system_info, metrics=metrics
        )
