# The underwear problem in computational form, using pomegrantae
#
# Simon Parsons
# October 2018

from pomegranate import *

prior_cheat = 0.04

# Variables are Underwear and Cheated.
#
# We have a prior for Cheated, two values 'c'heated and 'f'aithful:
Cheated   = DiscreteDistribution({'c': prior_cheat, 'f': (1-prior_cheat)})

# Conditional distribution relating underwear and cheating
#
# Notation for the conditional probability table is:
#
# [ 'Cheated', 'Underwear', <probability>]
#
# for the conditional value P(Underwear|Cheated).
#
# Values for Underwear are 'w'rong and 'r'ight:
Underwear = ConditionalProbabilityTable(
        [['c', 'w', 0.5],
         ['c', 'r', 0.5],
         ['f', 'w', 0.05],
         ['f', 'r', 0.95]], [Cheated])

# After creating the distributions, create a network to capture the
# relationship between the variables. This is:
#
# Cheated -> Underwear
#
# Two nodes:
s1 = Node(Cheated, name="Cheated")
s2 = Node(Underwear, name="Underwear")
# Create a network that includes nodes and an edge between them:
model = BayesianNetwork("Underwear Problem")
model.add_states(s1, s2)
model.add_edge(s1, s2)
# Fix the model structure
model.bake()

# Given we see the wrong underwear, does the model say they cheated or
# were faithful:
#
# model.predict reports the most probable value given the evidence
# provided.
prediction =  model.predict([[None, 'w']])
# model.predict.proba returns the distribution, wrapped in some
# meta-data:
predict_proba =  model.predict_proba([[None, 'w']])
dist = predict_proba[0][0].items()

# Pretty printing the output of the model:

print "Here's the prediction:"
if prediction[0][0] == 'c':
    print "Cheated!"
else:
    print "Faithful!"

print "And by the numbers:"
for i in range(len(Cheated)):
    if dist[i][0] == 'c':
        print "Cheated:", dist[i][1]
    if dist[i][0] == 'f':
        print "Faithful:", dist[i][1]
