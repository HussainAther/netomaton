import numpy as np

import netomaton as ntm
from .rule_test import *


class TestPerturbation(RuleTest):

    def test_perturbation(self):
        np.random.seed(10)
        expected = self._convert_to_list_of_lists("perturbation.ca", dtype=float)

        adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)
        initial_conditions = [0] * 100 + [1] + [0] * 99

        noise_amount = 0.02

        def perturbation(pctx):
            # from page 976 of Stephen Wolfram's "A New Kind of Science", the perturbation amount is:
            # v + Sign[v - 1/2]Random[]δ
            return pctx.node_activity + np.sign(pctx.node_activity - 1 / 2) * np.random.uniform() * noise_amount

        def algebraic_rule_30(ctx):
            """
            This rule implements the continuous cellular automaton with generalization of Rule 30, described on
            pages 325 and 976 of Stephen Wolfram's "A New Kind of Science".
            """
            activities = ctx.neighbourhood_activities
            x = activities[0] + activities[1] + activities[2] + (activities[1] * activities[2])
            # λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]
            result = np.exp(-10 * ((x - 1) ** 2)) + np.exp(-10 * ((x - 3) ** 2))

            return result

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=100,
                                     activity_rule=algebraic_rule_30, perturbation=perturbation)

        np.testing.assert_equal(expected, activities)

    def test_perturbation_reversible(self):
        np.random.seed(0)
        expected = self._convert_to_list_of_lists("perturbation_reversible.ca")

        adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)

        initial_conditions = np.random.randint(0, 2, 200)

        def perturbed_rule(ctx):
            rule = ntm.rules.nks_ca_rule_2(90)
            if ctx.timestep % 10 == 0:
                return 1
            return rule(ctx)

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=100,
                                     activity_rule=ntm.ReversibleRule_2(perturbed_rule),
                                     past_conditions=[initial_conditions])

        np.testing.assert_equal(expected, activities)

    def test_perturbation_eca(self):
        np.random.seed(0)
        expected = self._convert_to_list_of_lists("perturbation_eca.ca")

        adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)
        initial_conditions = [0] * 100 + [1] + [0] * 99

        def perturb(pctx):
            """
            Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.
            """
            if pctx.node_label == 100:
                return np.random.randint(2)
            return pctx.node_activity

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=100,
                                     activity_rule=ntm.rules.nks_ca_rule_2(30),
                                     perturbation=perturb)

        np.testing.assert_equal(expected, activities)
