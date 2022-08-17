import numpy as np
import os
import random
import itertools
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
from holdem_hands import check_straight_flush, check_quads, check_full_house, check_flush, check_straight, check_trips, check_two_pair, check_one_pair
from gym.spaces import Discrete, Box
from gym import Env

_deck = []
    
for s in [0, 1, 2, 3]:
    for v in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        _deck.append((s, v))

class CasinoHoldemEnv(Env):

    def __init__(self):
    # Initialise Deck
        self.action_space = Discrete(2)
        self.observation_space = _deck
        self.terminal = False
        self.new = True
        self.player_hand = []
        self.community_cards = []

    def reset(self):
        self.new = True
        self.terminal = False
        
        cards = random.sample(_deck, 5)

        self.player_hand = cards[0:2]
        self.community_cards = cards[2:]
        
        return self.player_hand, self.community_cards
        
    def check_hand_value(self, hand):

        if check_straight_flush(hand)[1]:
            if check_straight_flush(hand)[0] == 9000010:
                return check_straight_flush(hand)[0], 100
            else:
                return check_straight_flush(hand)[0], 20
        elif check_quads(hand)[1]:
            return check_quads(hand)[0], 10
        elif check_full_house(hand)[1]:
            return check_full_house(hand)[0], 3
        elif check_flush(hand)[1]:
            return check_flush(hand)[0], 2
        elif check_straight(hand)[1]:
            return check_straight(hand)[0], 1
        elif check_trips(hand)[1]:
            return check_trips(hand)[0], 1
        elif check_two_pair(hand)[1]:
            return check_two_pair(hand)[0], 1
        elif check_one_pair(hand)[1]:
            return check_one_pair(hand)[0], 1
        else:
            # High card
            sorted_rank = sorted([x[1] for x in hand], reverse=True)
            code = 1000000 + sorted_rank[0]*15*15*15*15 + sorted_rank[1]*15*15*15 + sorted_rank[2]*15*15 + sorted_rank[3]*15 + sorted_rank[4]
            return code, 1
        
    def compare_hands(self, player, dealer, community):
        player_value = max([self.check_hand_value(x) for x in itertools.combinations(player + community, 5)])
        dealer_value = max([self.check_hand_value(x) for x in itertools.combinations(dealer + community, 5)])
        
        if dealer_value[0] >= 201400:
            qualifies = True
        
        if dealer_value[0] > player_value[0]:
            return -3
        elif dealer_value[0] < player_value[0]:
            if qualifies: return player_value[1] + 2
            else: return player_value[1]
        else:
            return 0 

    def step(self, action):
        
        # single step decision
        done = True
        info = {}
        
        # call
        if action == 0:
            self.terminal = True
            self.new = False
            
            truncated_deck = _deck.copy()
            [truncated_deck.remove(x) for x in self.player_hand]
            [truncated_deck.remove(x) for x in self.community_cards]
            
            cards = random.sample(truncated_deck, 4)
            
            dealer_hand = cards[0:2]
            community = self.community_cards + cards[2:]
            
            reward = self.compare_hands(self.player_hand, dealer_hand, community)
            
            return [self.player_hand, self.community_cards], reward, done, info
        # fold
        else:
            return [self.player_hand, self.community_cards], -1, done, info
    
