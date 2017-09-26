from contest_rank import ContestRank

class UserManager:
    
    def __init__(self):
        self.user_list = {}
        self.user_ranks = {}
        self.contest_dict = {}\
    
    def add_user(self, name, alias):
        if name in self.user_list:
            raise ValueError("duplicate name '{0}' found".format(name))
        self.user_list[name] = alias
        ranks = sum([ContestRank.from_user(user, oj) for oj, user in alias.items()], [])
        self.user_ranks[name] = ranks
        for rank in ranks:
            id = rank.get_contest_id()
            if id not in self.contest_dict:
                self.contest_dict[id] = []
            self.contest_dict[id].append((name, rank))
            
    def update_rating(self, rating_system, least_num_coders=2, least_time=None, verbose=True):
        self.time_values = set({})
        contest_list = list(self.contest_dict.values())
        contest_list.sort(key=lambda rank_list: rank_list[0][1].time)
        for rank_list in contest_list:
            if least_time and rank_list[0][1].time < least_time:
                continue
            if len(rank_list) >= least_num_coders:
                self.time_values.add(rank_list[0][1].time)
                rank_list.sort(key=lambda item: item[1].rank)
                rating_system.update(rank_list)
                if verbose:
                    print(rating_system.rating)
                