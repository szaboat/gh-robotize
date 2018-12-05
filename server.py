import shelve
import time
import schedule
import requests
import logging

from flask import Flask, request, jsonify
from threading import Thread
from gh import check_pr


app = Flask(__name__)
POLL_INTERVAL = 300


class PullRequest(object):
    def __init__(self, url):
        self.url = url
        self.status = "open"
        self.created_at = time.time()


@app.route("/add/", methods=["POST"])
def add():
    with shelve.open("database") as database:
        content = request.get_json()
        prs = database.get("prs", dict())
        url = content["url"]
        pr = PullRequest(url=content["url"])
        prs[url] = pr
        database["prs"] = prs
    return "OK"


@app.route("/")
def index():
    with shelve.open("database", "r") as database:
        prs = database.get("prs", {})
        return jsonify([{key: {"status": prs[key].status}} for key in prs.keys()])


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def check_prs():
    logging.info('running schedule')
    with shelve.open("database", "r") as database:
        prs = database.get("prs")
        for key, pr in prs.items():
            logging.info("check %s" % pr.url)
            gpr = check_pr(pr.url)
            if gpr and gpr.mergeable:
                try:
                    gpr.merge()
                    logging.info("Merged %s" % pr.url)
                except Exception as e:
                    logging.error("Failed to merge %s" % pr.url)


if __name__ == "__main__":
    schedule.every(POLL_INTERVAL).seconds.do(check_prs)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
