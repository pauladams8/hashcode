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
    return set(ingredient for pizza in pizzas for ingredient in pizza.ingredients)


class Team():
    def __init__(self, size):
        self.size = size
        self.pizzas = []


class Pizza():
    def __init__(self, ingredients):
        self.ingredients = ingredients


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

for l in pizza_data:
    ingredients = l.strip().split(' ')
    n = int(ingredients.pop(0))
    assert(len(ingredients) == n)
    pizzas.append(Pizza(ingredients))

for i, team in enumerate(teams):
    # We need to maximise the number of distinct ingredients on the team's pizza
    team.pizzas = max(
        # Generate all possible combinations of length
        itertools.combinations(
            # Retain the indexes for output
            # We must deliver pizzas to every team member
            enumerate(pizzas), team.size
        ),
        # c is a combination of (i, pizza) tuples of length team.size
        # We sort the combinations by the number of distinct ingredients on their pizzas
        key=lambda c: len(distinct_ingredients(pizza for _, pizza in c)),
        default=[]
    )

    for i, _ in team.pizzas:
        # Remove the pizzas in team.pizzas from the global pizza pool, since they've been allocated
        del pizzas[i]

# filter out any teams with insufficient pizzas, we cannot deliver to them :(
teams = [team for team in teams if len(team.pizzas) == team.size]

print(str(len(teams)))

for team in teams:
    print(team.size, *(str(i + 1) for i, _ in team.pizzas))


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
