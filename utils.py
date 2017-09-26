import requests
import re
import json
from bs4 import BeautifulSoup
import numpy as np

def get_discretize_dict(values):
    invs = np.unique(values, return_inverse=True)[1]
    discretize_dict = {}
    for value, inv in zip(values, invs):
        discretize_dict[value] = inv
    return discretize_dict

def get_codeforces_users_by_organization(organization_id, rated=True, max_user=10):
    response = requests.get('http://codeforces.com/ratings/organization/%d' % organization_id)
    bs = BeautifulSoup(response.content, "lxml")
    table = bs.find_all('table')[5]
    users = []
    for user in table.find_all('tr')[1:]:
        if rated and user.span:
            continue
        users.append(user.a.text)
        max_user -= 1
        if max_user <= 0:
            break
    return users
