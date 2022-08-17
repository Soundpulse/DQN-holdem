import game
import numpy as np
import sarsa

if __name__ == "__main__":

    total_bet = 0
    total_reward = 0

    V = np.load('POKER_V.npy')
    
    for i in range(1000000):
        state = game.initialise_state()
        action = ( V[sarsa.encode(state.player)][1] >= 0)
        _, reward = game.step(state, action)
        
        if action: total_bet += 3
        else: total_bet += 1
        
        total_reward += reward
        
        if i % 10000 == 0:
            print("Loading.. " + str(i/10000) +"%")
    
    print(total_reward/total_bet*100)
    
   