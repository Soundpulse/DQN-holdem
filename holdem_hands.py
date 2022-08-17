import numpy as np
import random
import itertools
from collections import Counter

def check_straight_flush(hand):
    if check_straight(hand)[1] and check_flush(hand)[1]:
        return 4000000 + check_straight(hand)[0], True
    else:
        return 0, False
    
def check_quads(hand):
    counted_cards = Counter([x[1] for x in hand])
    three_most_common, count = zip(*counted_cards.most_common(3))
    
    if count == (4, 1):
        return 8000000 + three_most_common[0]*15 + three_most_common[1], True
    else:
        return 0, False
    
def check_full_house(hand):
    counted_cards = Counter([x[1] for x in hand])
    three_most_common, count = zip(*counted_cards.most_common(3))
    
    if count == (3, 2):
        return 7000000 + three_most_common[0]*15 + three_most_common[1], True
    else:
        return 0, False

def check_flush(hand):
    if len(set([x[0] for x in hand])) == 1:
        sorted_rank = sorted([x[1] for x in hand], reverse=True)
        return 6000000 + sorted_rank[0]*15*15*15*15 + sorted_rank[1]*15*15*15 + sorted_rank[2]*15*15 + sorted_rank[3]*15 + sorted_rank[4], True
    else:
        return 0, False

def check_straight(hand):
    # 2,3,4,5,6 to 10,11,12,13,14
    # 14,2,3,4,5 smallest
    rank_set = { card[1] for card in hand }
    if(all(x in rank_set for x in [14,2,3,4,5])): return 5000001, True
    rank_range = max(rank_set) - min(rank_set) + 1
    
    if rank_range == len(hand) and len(rank_set) == len(hand):
        return 5000000 + min(rank_set), True
    else:
        return 0, False
    
def check_trips(hand):
    counted_cards = Counter([x[1] for x in hand])
    three_most_common, count = zip(*counted_cards.most_common(3))
    
    if count == (3, 1, 1):
        return 4000000 + three_most_common[0]*15*15 + three_most_common[1]*15 + three_most_common[2], True
    else:
        return 0, False

def check_two_pair(hand):
    counted_cards = Counter([x[1] for x in hand])
    three_most_common, count = zip(*counted_cards.most_common(3))
    
    if count == (2, 2, 1):
    
        larger_pair, smaller_pair = max(three_most_common[0:1]), min(three_most_common[0:1])
    
        return 3000000 + larger_pair*15*15 + smaller_pair*15 + three_most_common[2], True
    else:
        return 0, False

def check_one_pair(hand):
    counted_cards = Counter([x[1] for x in hand])
    four_most_common, count = zip(*counted_cards.most_common(4))
    
    if count == (2, 1, 1, 1):
        return 2000000 + four_most_common[0]*15*15*15 + four_most_common[1]*15*15 + four_most_common[2]*15 + four_most_common[3], True
    else:
        return 0, False