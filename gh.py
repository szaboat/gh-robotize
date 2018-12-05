import github3
import os
import logging

token = os.environ['GH_TOKEN']

g = github3.login(token=token)

def check_pr(pr_url):
    _, _, _, user, repo, _, id, _ = pr_url.split('/')
    try:
        pr = g.pull_request(user, repo, id)
    except Exception:
        pr = None
        logging.exception("g.pull_request failed")
    return pr
