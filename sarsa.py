import game
import numpy as np
import random
import itertools
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import time
import math
import os

N0 = 100
ITERATIONS = 100000

hit = True
stick = False
actions = [hit, stick]

lmd = 0.1

Q_matrix = np.zeros((169, 2))
N_matrix = np.zeros((169, 2))

def encode(encoded_hand):
    first_card = encoded_hand % 53
    second_card = int(encoded_hand / 53)
    
    suited = (int(first_card / 13) == int(second_card / 13))
    
    if suited:
        #return (14 - second_card, 14 - first_card)
        return 13 * (12 - ((second_card - 1) % 13)) + (12 - ((first_card - 1) % 13))
    else:
        return 13 * (12 - ((first_card - 1) % 13)) + (12 - ((second_card - 1) % 13))
        #return (14 - first_card, 14 - second_card)

def Q(state, action):
    return Q_matrix[encode(state.player)][int(action)]

def N(state, action):
    return N_matrix[encode(state.player)][int(action)]

def allQ(state):
    return Q_matrix[encode(state.player)]
    
def allN(state):
    return N_matrix[encode(state.player)]

def allE(state):
    return E_matrix[encode(state.player)]

def V(q):
    return np.max(q, axis=1)
    
def epsilon_greedy(q, n):
    epsilon = N0 / (N0 + sum(n))
    
    if np.random.random() < epsilon:
        return random.choice(actions)
    else:
        return bool(np.argmax(q))
        
if __name__ == "__main__":
 
    for k in range(1, ITERATIONS):
        terminal = False
        
        E_matrix = np.zeros_like(Q_matrix)
        
        state = game.initialise_state()
        action = epsilon_greedy(allQ(state), allN(state))

        while not terminal:
            next_state, reward = game.step(state, action)

            terminal = state.terminal
            
            if not terminal:
                next_action = epsilon_greedy(allQ(state), allN(state))
                delta = reward + Q(next_state, next_action) - Q(state, action)
            else:
                delta = reward - Q(state, action)
            
            allE(state)[int(action)] += 1
            allN(state)[int(action)] += 1
            
            alpha = 1/N(state,action)
            
            Q_matrix += alpha * delta * E_matrix
            E_matrix *= lmd
            
            if not terminal:
                state = next_state
                action = next_action
        
        if k % 10000 == 0:
            os.system('cls')
            print("Loading...  " + str(round(k/ITERATIONS*100,3)) + "%")
        
    np.save('POKER_V.npy', Q_matrix)
    game.visualise(V(Q_matrix))