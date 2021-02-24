# Add your name if you can see this

# Paul
# James
# Matt
# Seb

# nb guest user = seb

from __future__ import annotations

import itertools

# Array Definition
pizzas = []
deliveries = []
teams = []


def distinct_ingredients(pizzas):
    return set((ingredient for pizza in pizzas for ingredient in pizza.ingredients))


class Team():
    def __init__(self, size):
        self.size = size
        self.pizzas = []


class Pizza():
    def __init__(self, ingredients, id):
        self.ingredients = ingredients
        self.id = id


def validate(numInTeam, numofPizza, num_deliveries, no_2_person_teams, no_3_person_teams, no_4_person_teams):
    if (numInTeam == numofPizza):
        if not (1 <= num_deliveries or num_deliveries >= no_2_person_teams + no_3_person_teams + no_4_person_teams):
            raise Exception(
                "Total deliveries should be between 1 and the " + no_2_person_teams + no_3_person_teams + no_4_person_teams + " teams")
        return True
    return False


input = open('a_example', 'r')

[m, no_2_person_teams, no_3_person_teams,
    no_4_person_teams] = [int(v) for v in input.readline().strip().split(' ')]


for _ in range(no_2_person_teams):
    teams.append(Team(2))
for _ in range(no_3_person_teams):
    teams.append(Team(3))
for _ in range(no_4_person_teams):
    teams.append(Team(4))

pizza_data = input.read().split('\n')
assert(len(pizza_data) == m)

for i, l in enumerate(pizza_data):
    ingredients = l.strip().split(' ')
    n = int(ingredients.pop(0))
    assert(len(ingredients) == n)
    pizzas.append(Pizza(set(ingredients), i))

for team in teams:
    # We need to maximise the number of distinct ingredients on the team's pizza, so let's try each chuck of size team.size
    combinations = [chunk for chunk in itertools.combinations(
        pizzas, team.size)]

    comb_max = 0

    for combination in combinations:
        comb_len = len(distinct_ingredients(combination))
        if comb_len > comb_max:
            comb_max = comb_len
            team.pizzas = combination

    # We need to remove the pizzas in team.pizzas from the global pizza pool, since they've been allocated
    for pizza in team.pizzas:
        pizzas.remove(pizza)

# filter out any teams with no pizzas, we will not deliver to them :(
teams = [team for team in teams if team.pizzas]

print(str(len(teams)))

for team in teams:
    print(team.size, *(pizza.id for pizza in team.pizzas))


exit()
# work in progress below this point

# Write out to output_file
output = open("output_file", "w")

output.write(
    f'{str(len(deliveries))} {str(no_2_person_teams)} {str(no_3_person_teams)} {str(no_4_person_teams)} teams'
)
output = open("output_file", "w")

output.write(str(len(deliveries)))

for delivery in deliveries:
    output.write(
        f'{delivery.num_people()} {" ".join([str(delivery) for delivery in deliveries])}')
