import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime
from functools import wraps
import time


def retry(default_return_value, tries=2, delay=0.5, backoff=2):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except (IndexError, KeyError):
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            print('failed to execute function {} with argument {}'.format(f.__name__, args, kwargs))
            return default_return_value

        return f_retry

    return deco_retry


class ContestRank:
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return self.name + ' - ' + str(self.rank) + ' ' + self.user
    
    def __hash__(self):
        return hash(self.get_contest_id())
    
    def get_contest_id(self):
        raise NotImplementedError()
    
    @staticmethod
    def from_user(user, oj):
        print('loading rank from user {} on {}'.format(user, oj))
        return sum([cls.from_user(user) for cls in ContestRank.__subclasses__() if cls.oj == oj], [])
        
        
class AtcoderRank(ContestRank):
    oj = 'atcoder'
    
    def __init__(self, user, raw_data):
        self.user = user
        self.raw_data = raw_data
        self.time = raw_data[0]
        self.rank = raw_data[2]
        self.name = raw_data[3]
        self.id = raw_data[4]
        
    def get_contest_id(self):
        return (self.oj, self.id)
    
    @staticmethod
    @retry([])
    def from_user(user):
        response = requests.get('https://atcoder.jp/user/%s' % user)
        bs = BeautifulSoup(response.text, "lxml")
        pattern = re.compile('.*parse\("(.*)"\)')
        data = pattern.match(bs.find_all("script")[12].string).groups()[0]
        raw_rating_history = json.loads(data.replace('\\', ''))
        return [AtcoderRank(user, raw_data) for raw_data in raw_rating_history]
    
    
class CodeforcesRank(ContestRank):
    oj = 'codeforces'
    
    def __init__(self, user, raw_data):
        self.user = user
        self.raw_data = raw_data
        self.time = raw_data['ratingUpdateTimeSeconds']
        self.rank = raw_data['rank']
        self.name = raw_data['contestName']
        self.id = raw_data['contestId']
        
    def get_contest_id(self):
        return (self.oj, self.id)
    
    @staticmethod
    @retry([])
    def from_user(user):
        response = requests.get('http://codeforces.com/api/user.rating?handle=%s'
                                % user)
        raw_rating_history = json.loads(response.text)['result']
        return [CodeforcesRank(user, raw_data) for raw_data in raw_rating_history]

    
class TopcoderRank(ContestRank):
    oj = 'topcoder'
    
    def __init__(self, user, raw_data):
        self.raw_data = raw_data
        self.user = user
        r = raw_data['rounds'][0]
        x = r['userSRMDetails']
        self.time = int(datetime.strptime(r['codingStartAt'], '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
        self.rank = x['divisionPlacement']
        self.name = raw_data['name']
        self.id = x['roundId']
        self.division = x['division']
        
    def get_contest_id(self):
        return (self.oj, self.id, self.division)
    
    @staticmethod
    @retry([])
    def from_user(user):
        response = requests.get('https://api.topcoder.com/v3/members/%s/srms/' \
                                % user)
        raw_rating_history = json.loads(response.text)['result']['content']
        rating_history = []
        for item in raw_rating_history:
            assert(len(item['rounds']) == 1)
            r = item['rounds'][0]
            if 'userSRMDetails' not in r:
                continue
            x = r['userSRMDetails']
            if x['rated'] == 0:
                continue
            rating_history.append(TopcoderRank(user, item))
        return rating_history
