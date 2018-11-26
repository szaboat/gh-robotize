import shelve
import time
import schedule
import requests

from flask import Flask, request
from threading import Thread
from gh import check_pr

app = Flask(__name__)


class PullRequest(object):
    def __init__(self, url):
        self.url = url
        self.status = 'open'
        self.created_at = time.time()


@app.route("/add/", methods=['POST'])
def add():
    with shelve.open('database') as database:
        content = request.get_json()
        prs = database.get('prs', dict())
        url = content['url']
        pr = PullRequest(url=content['url'])
        prs[url] = pr
        database['prs'] = prs
    return "OK"


@app.route("/")
def hello():
    with shelve.open('database') as database:
        prs = database.get('prs', {})
        return "".join(prs.keys())


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def check_prs():
    with shelve.open('database', 'r') as database:
        prs = database.get('prs')
        for key, pr in prs.items():
            print("check %s" % pr.url)
            pr = check_pr(pr.url)
            if pr.mergeable:
                pr.merge()
                print("Merged %s" % pr.url)


start_time = time.time()


if __name__ == '__main__':
    schedule.every(60).seconds.do(check_prs)
    t = Thread(target=run_schedule)
    t.start()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
