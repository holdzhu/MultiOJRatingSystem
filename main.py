from rating_system import TopcoderRatingSystem
from user_manager import UserManager
from datetime import datetime
from utils import get_discretize_dict, get_codeforces_users_by_organization
from datetime import datetime

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

user_manager = UserManager()

user_manager.add_user(
    u'何柱', {
        'codeforces': 'Hezhu',
        'atcoder': 'Hezhu',
        'topcoder': 'Herzu',
    }
)
user_manager.add_user(
    u'陈鑫', {
        'codeforces': 'missever',
        'atcoder': 'missever',
        'topcoder': 'missever',
    }
)
user_manager.add_user(
    u'廖奇', {
        'codeforces': 'liao772002',
        'topcoder': 'liao772002',
    }
)
user_manager.add_user(
    u'杨宇同', {
        'codeforces': 'Orenji.Sora',
        'topcoder': 'Orenji.Sora',
    }
)
user_manager.add_user(
    u'徐浩', {
        'codeforces': 'femsub',
        'atcoder': 'femsub',
        'topcoder': 'femsub',
    }
)
user_manager.add_user(
    u'万笛文', {
        'codeforces': 'dnvtmf',
        'topcoder': 'dnvtmf',
    }
)
user_manager.add_user(
    u'潘星霖', {
        'codeforces': 'UESTC_Sphinx',
        'topcoder': 'UESTC_Sphinx',
    }
)
user_manager.add_user(
    u'沈柯', {
        'codeforces': 'xiper',
        'atcoder': 'xiper',
        'topcoder': 'xiper',
    }
)

rating_system = TopcoderRatingSystem()
least_num_coders = 2
least_time=None # datetime(2016, 1, 1).timestamp()

user_manager.update_rating(rating_system, least_num_coders=least_num_coders, least_time=least_time, verbose=False)

time_dict = get_discretize_dict(list(user_manager.time_values))

for name, ratings in rating_system.rating_history.items():
    plt.plot([time_dict.get(item[1].time) for item in ratings], 
             [item[0] for item in ratings], 'o-', label=name)
plt.xlim((-1, len(time_dict)))
plt.xticks(range(len(time_dict))[::5])
ax = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)).axes
ax.set_xticklabels([datetime.fromtimestamp(x).date() for x in sorted(time_dict.keys())][::5])
for tick in ax.get_xticklabels():
    tick.set_rotation(45)
plt.show()
