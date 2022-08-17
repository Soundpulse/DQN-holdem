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

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

# Initialise Deck
suit = [0, 1, 2, 3]
value = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

deck = []
call = True
fold = False
actions = [call, fold]

for s in suit:
    for v in value:
        deck.append((s, v))

class State:
    def __init__(self, player, terminal):
        self.player = player
        self.terminal = terminal
    
    def __repr__(self):
        return "(" + str(self.player) + ","  + str(self.terminal) + ")"

def initialise_state():

    # Card Encoding:
    #       0: undefined
    #  1 ~ 13: Spade 23456789TJQKA
    # 14 ~ 26: Heart 23456789TJQKA
    # 27 ~ 39: Club 23456789TJQKA
    # 40 ~ 52: Diamond 23456789TJQKA
    
    # Check suit: int(n/13)
    # 0: Spade
    # 1: Heart
    # 2: Club
    # 3: Diamond
    
    # Find Value: n - int(n/13)*13

    cards = random.sample(deck, 2)
    
    encoded_player = 53*encode_card(cards[0]) + encode_card(cards[1])
    #encoded_community = 53*53*cards[2][1] + 53*cards[3][1] + cards[4][1] 
    
    return State(encoded_player, False)
    
def encode_card(card):
    # mapping:
    # From: 2~14 s,h,c,d
    # To: 1~13 (s), 14~26 (h), 27~39 (c), 40~52 (d)
    return card[0]*13 + (card[1] - 1)
    
def decode_card(encoded_card):
    # From: 1~13 (s), 14~26 (h), 27~39 (c), 40~52 (d)
    # To: 2~14 s,h,c,d
    suit = int((encoded_card-1) / 13)
    value = encoded_card - (suit-1)*13 - 12
    
    return (suit, value)
    
def decode_hand(encoded_cards):

    # 3 cards
    if encoded_cards > 53*53:
        t = encoded_cards % 53
        s = int(((encoded_cards - t % (53*53))/53) % 53)
        f = int((encoded_cards - 53*s - t) / (53*53))
        
        cards = [decode_card(f), decode_card(s), decode_card(t)]
    # 2 cards
    else:
        s = encoded_cards % 53
        f = int((encoded_cards - s) / 53)
        
        cards = [decode_card(f), decode_card(s)]
        
    return cards
    
def check_hand_value(hand):

    if check_straight_flush(hand)[1]:
        if check_straight_flush(hand)[0] == 9000010:
            return check_straight_flush(hand)[0], 1
        else:
            return check_straight_flush(hand)[0], 1
    elif check_quads(hand)[1]:
        return check_quads(hand)[0], 1
    elif check_full_house(hand)[1]:
        return check_full_house(hand)[0], 1
    elif check_flush(hand)[1]:
        return check_flush(hand)[0], 1
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
    
def compare_hands(player, dealer, community):
    player_value = max([check_hand_value(x) for x in itertools.combinations(player + community, 5)])
    dealer_value = max([check_hand_value(x) for x in itertools.combinations(dealer + community, 5)])
    
    if dealer_value[0] >= 201400:
        qualifies = True
    
    if dealer_value[0] > player_value[0]:
        return -1.5
    elif dealer_value[0] < player_value[0]:
        if qualifies: return player_value[1] + 1
        else: return player_value[1]
    else:
        return 0

def step(s, a):

    player = s.player
    
    if a == call:
        player_cards = decode_hand(player)
        
        truncated_deck = deck.copy()
        
        [truncated_deck.remove(x) for x in player_cards]
        
        dealt_cards = random.sample(truncated_deck, 7)
        
        full_community = dealt_cards[0:5]
        dealer_cards = [dealt_cards[5], dealt_cards[6]]
        
        # On Win: Base bet 1:1~100
        # On Qualify: Call Bet 1:2
        return State(s.player, True), compare_hands(player_cards, dealer_cards, full_community)
        
    elif a == fold:
        return State(s.player, True), -1
            
def visualise(matrix):

    # Make the plot
    fig = plt.figure(figsize=plt.figaspect(0.5))
    fig.set_size_inches(18.5, 10.5)

    # =============
    # First subplot
    # =============
    
    X = np.arange(0, 13, 1)
    Y = np.arange(0, 13, 1)
    X,Y = np.meshgrid(X, Y)
    M = matrix.reshape([13, 13])
    
    print(M)
    
    #M = pd.DataFrame(M)
    #df=M.unstack().reset_index()
    #df.columns=["X","Y","Z"]
     
    # And transform the old column name in something numeric
    #df['X']=pd.Categorical(df['X'])
    #df['X']=df['X'].cat.codes
    
    ax = fig.add_subplot(1, 2, 1, projection='3d')

    ax.plot_surface(X, Y, M, cmap=plt.cm.viridis, rstride=1, cstride=1, edgecolor='none')
    ax.set_xticks(np.arange(0, 13, 1))
    ax.set_yticks(np.arange(0, 13, 1))
    ax.set_xticklabels([2,3,4,5,6,7,8,9,10,'J','Q','K','A'])
    ax.set_yticklabels([2,3,4,5,6,7,8,9,10,'J','Q','K','A'])
    ax.set_title('Poker (Ignore dealt cards)', fontsize=16)
    ax.set_xlabel("Suited Hands", fontsize=14)
    ax.set_ylabel("Non Suited Hands", fontsize=14)
    ax.set_zlabel("Expected Reward", fontsize=14)
    ax.view_init(45, 20)

    plt.show()