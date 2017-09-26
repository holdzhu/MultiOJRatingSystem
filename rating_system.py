import math
import numpy as np
from scipy.special import erf, ndtri


class RatingSystem:
    
    def update(self, rank_list):
        raise NotImplementedError()


class TopcoderRatingSystem(RatingSystem):
    
    def __init__(self):
        self.rating = {}
        self.volatility = {}
        self.times_played = {}
        self.rating_history = {}
    
    def update(self, rank_list):
        num_coders = len(rank_list)
        rating = np.full((num_coders,), 1200)
        volatility = np.full((num_coders,), 515)
        times_played = np.zeros((num_coders,))
        rank = np.arange(num_coders) + 1
        for index, rank_item in enumerate(rank_list):
            name = rank_item[0]
            if name in self.rating:
                rating[index] = self.rating[name]
                volatility[index] = self.volatility[name]
                times_played[index] = self.times_played[name]
            else:
                self.rating_history[name] = []
        volatility_squared = np.square(volatility)
        competition_factor = math.sqrt(np.average(volatility_squared) + \
                                   np.var(rating, ddof=1))
        win_probability = np.fromfunction(lambda i, j : 0.5 * \
                                      (erf((rating[i] - rating[j]) / \
                                           np.sqrt(2 * (volatility_squared[i] + \
                                                        volatility_squared[j]))) + 1), \
                                      (num_coders, num_coders), dtype=int)
        expected_rank = .5 + np.sum(win_probability, 0)
        expected_performance = -ndtri((expected_rank - .5) / num_coders)
        actual_performance = -ndtri((rank - .5) / num_coders)
        performed_as_rating = rating + competition_factor * \
                          (actual_performance - expected_performance)
        weight = 1 / (1 - (.42 / (times_played + 1) + .18)) - 1
        cap = 150 + 1500 / (times_played + 2)
        new_rating = np.clip((rating + weight * performed_as_rating) / (1 + weight), \
                        rating - cap,
                        rating + cap)
        new_volatility = np.sqrt(np.square(new_rating - rating) / weight + \
                             np.square(volatility) / (weight + 1))
        new_times_played = times_played + 1
        for index, rank_item in enumerate(rank_list):
            name = rank_item[0]
            self.rating[name] = new_rating[index]
            self.volatility[name] = new_volatility[index]
            self.times_played[name] = new_times_played[index]
            self.rating_history[name].append((new_rating[index], rank_item[1]))

