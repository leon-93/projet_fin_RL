import numpy as np


class EpsilonGreedy:
    def __init__(self, params):
        self.params      =  params
        self.epsilon     = 0.4
        self.arm_count   = params.edDict[0].actions
        self.Q           = np.zeros(self.arm_count) # q-value of actions
        self.N           = np.zeros(self.arm_count) # action count

    def update(self, ed):
        self.N[ed.action] += 1 # increment action count
        self.Q[ed.action] += 1/self.N[ed.action] * (ed.dr_mean - self.Q[ed.action]) # inc. update rule
 
        if np.random.uniform(0,1) > self.epsilon:
            ed.newaction = self.Q.argmax()
        else:
            ed.newaction = np.random.randint(0, self.arm_count)

'''

        if np.random.rand() < self.epsilon:
            # Exploration : choisissez une action au hasard
            return np.random.randint(0, self.params.nrBS)
        else:
            # Exploitation : choisissez l'action avec la meilleure valeur estimée
            return np.argmax(self.values)
        
    def update_values(self, action, reward):
        # Mettez à jour les valeurs estimées basées sur la récompense reçue
        self.action_counts[action] += 1
        self.values[action] += (reward - self.values[action]) / self.action_counts[action]'''

'''class Params:
    # ...

# Ajoutez d'autres classes et fonctions nécessaires ici

def sim_transmit(env, ed, bsDict, server, algo):
    while True:
        np.random.seed(100)
        yield env.timeout(random.expovariate(1/ed.period))
        
        # Choisissez l'action en fonction de l'algorithme spécifié
        if algo == "epsilon_greedy":
            chosen_action = epsilon_greedy.choose_action()
        else:
            # Ajoutez d'autres algorithmes ici si nécessaire
            chosen_action = 0  # Remplacez cela par la logique réelle
            
        yield env.timeout(ed.send(bsDict, chosen_action))
        for bsid, bs in bsDict.items():
            bs.receive(ed)
        yield env.timeout(server.send(ed))
        ed.receive()
        yield env.timeout(ed.period - ed.time - ed.wait)'''