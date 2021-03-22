import netomaton as ntm


if __name__ == '__main__':

    adjacency_matrix = ntm.network.cellular_automaton(n=200)

    initial_conditions = [0]*100 + [1] + [0]*99

    activities, adjacencies = ntm.evolve_2(initial_conditions, adjacency_matrix, timesteps=100,
                                           activity_rule=ntm.rules.totalistic_ca_2(k=3, rule=777))

    ntm.plot_grid(activities)
