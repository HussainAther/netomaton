import netomaton as ntm
import numpy as np
import random
from .rule_test import *


class TestLangtonsLambda(RuleTest):

    def test_average_mutual_information(self):
        np.random.seed(0)
        network = ntm.topology.cellular_automaton(n=200)

        initial_conditions = ntm.init_random(200)

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=1000,
                                activity_rule=ntm.rules.nks_ca_rule(30))

        # calculate the average mutual information between a node and itself in the next time step
        avg_mutual_information = ntm.average_mutual_information(trajectory)

        self.assertAlmostEqual(avg_mutual_information, 0.0008661819154803652)

    def test_average_node_entropy(self):
        np.random.seed(0)
        network = ntm.topology.cellular_automaton(n=200)

        initial_conditions = ntm.init_random(200)

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=1000,
                                activity_rule=ntm.rules.nks_ca_rule(30))

        # calculate the average node entropy; the value will be ~0.999 in this case
        avg_node_entropy = ntm.average_node_entropy(trajectory)

        self.assertAlmostEqual(avg_node_entropy, 0.9991515020481837)

    def test_rule_table(self):
        np.random.seed(324324)
        random.seed(43543)
        expected = self._convert_to_list_of_lists("rule_table.ca")

        rule_table, actual_lambda, quiescent_state = ntm.random_rule_table(lambda_val=0.37, k=4, r=2,
                                                                           strong_quiescence=True, isotropic=True)

        network = ntm.topology.cellular_automaton(n=128, r=2)

        initial_conditions = ntm.init_random(128, k=4, n_randomized=20)

        # evolve the cellular automaton for 200 time steps
        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=200,
                                activity_rule=ntm.table_rule(rule_table))

        activities = ntm.get_activities_over_time_as_list(trajectory)
        np.testing.assert_equal(expected, activities)

    def test_rule_table_walkthrough(self):
        np.random.seed(324324)
        random.seed(43543)
        expected = self._convert_to_list_of_list_of_lists("rule_table_walkthrough.ca")

        rule_table, actual_lambda, quiescent_state = ntm.random_rule_table(lambda_val=0.0, k=4, r=2,
                                                                           strong_quiescence=True, isotropic=True)

        lambda_vals = [0.15, 0.37, 0.75]
        ca_list = []
        avg_node_entropies = []
        avg_mutual_informations = []
        for i in range(0, 3):
            network = ntm.topology.cellular_automaton(n=128, r=2)

            initial_conditions = ntm.init_random(128, k=4)

            rule_table, actual_lambda = ntm.table_walk_through(rule_table, lambda_vals[i], k=4, r=2,
                                                               quiescent_state=quiescent_state, strong_quiescence=True)
            # evolve the cellular automaton for 200 time steps
            trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                    activity_rule=ntm.table_rule(rule_table), timesteps=200)

            activities = ntm.get_activities_over_time_as_list(trajectory)
            ca_list.append(activities)
            avg_node_entropies.append(ntm.average_node_entropy(activities))
            avg_mutual_informations.append(ntm.average_mutual_information(activities))

        np.testing.assert_equal(expected, ca_list)

        expected_avg_node_entropies = [0.37835928798494195, 1.5076786394760435, 1.985953613326983]
        expected_avg_mutual_informations = [0.07825277488429445, 0.07752959733790643, 0.038339515020537174]
        for i in range(0, 3):
            self.assertAlmostEqual(expected_avg_node_entropies[i], avg_node_entropies[i])
            self.assertAlmostEqual(expected_avg_mutual_informations[i], avg_mutual_informations[i])
