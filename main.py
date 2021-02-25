"""
          _______  _______           _______  _______  ______   _______ 
|\     /|(  ___  )(  ____ \|\     /|(  ____ \(  ___  )(  __  \ (  ____ \
| )   ( || (   ) || (    \/| )   ( || (    \/| (   ) || (  \  )| (    \/
| (___) || (___) || (_____ | (___) || |      | |   | || |   ) || (__    
|  ___  ||  ___  |(_____  )|  ___  || |      | |   | || |   | ||  __)   
| (   ) || (   ) |      ) || (   ) || |      | |   | || |   ) || (      
| )   ( || )   ( |/\____) || )   ( || (____/\| (___) || (__/  )| (____/\
|/     \||/     \|\_______)|/     \|(_______/(_______)(______/ (_______/
                                                                    
"""
# The following code is made by the "Gallery Gang" for the hashcode coding competition
# James
# Paul
# Seb
# Matt

from datetime import time as Time
from typing import List
from collections import deque

# To run the program, pipe the input file to stdin and read from stdout
[duration, intersection_len, street_len, car_len, bonus_points] = [v.strip()
                                                                   for v in input().strip().split(' ')]

duration = int(duration)

initial = duration

total_score = 0

# Schedule class


class Schedule():
    # __init__ function
    def __init__(self, street, period: int):
        self.street = street
        self.period = period

    # switch function
    def switch(self):
        self.street.allow_traffic = not self.street.allow_traffic

# Intersection class


class Intersection():
    # __init__ function
    def __init__(self):
        self.exits = 0
        self.entrances = 0
        self.schedules = deque([])
        self.active_schedule = None

    # us when we win 😎

    def add_schedule(self, schedule: Schedule):
        if len(self.schedules) == 0:
            self.active_schedule = schedule
        self.schedules.append(schedule)

    def increment(self, time: int):
        if time % self.active_schedule.period == 0:
            # current schedule ends, move on to next schedule
            self.active_schedule.switch()
            self.schedules.rotate(-1)
            self.active_schedule = self.schedules[0]
            self.active_schedule.switch()

# Car class


class Car():
    # __init__ function
    def __init__(self, streets):
        self.streets = streets
        # Since a car can only be on one street at a time
        self.time_taken = 0
        # total time take, as time_taken gets reset
        self.total_time_taken = 0

    def move(self, duration: int):
        # remove current street from path
        # join next street's queue
        street = self.streets.pop(0)
        self.total_time_taken += self.time_taken
        if street:
            street.add_car(self)
            self.time_taken = 0
        else:
            total_score += bonus_points
            total_score += initial - self.total_time_taken


class Street():
    def __init__(self, start: int, end: int, name: str, length: int):
        self.start = start
        self.end = end
        self.name = name
        # Length is the time taken to go from start to end
        self.length = length
        # The duration for which the street's traffic light is green
        self.window = 0
        # traffic light boolean state
        self.allow_traffic = False
        self.queue: List[Car] = []

    def add_car(self, car: Car):
        self.queue.append(car)

    def pop_queue(self):
        for car in self.queue:
            # Move every car along one
            # 🚗 beep beep 👵
            car.time_taken += 1
        if not self.allow_traffic:
            return
        if len(self.queue) == 0:
            return
        if self.queue[0].time_taken < self.length:
            return
        car = self.queue.pop(0)
        car.move()


"""
        _______           _______  _______  _                     ______   _______ 
|\     /|(  ____ \         (  ____ \(  ___  )( (    /|             (  __  \ (  ___  )
| )   ( || (    \/         | (    \/| (   ) ||  \  ( |             | (  \  )| (   ) |
| | _ | || (__             | |      | (___) ||   \ | |             | |   ) || |   | |
| |( )| ||  __)            | |      |  ___  || (\ \) |             | |   | || |   | |
| || | || (               | |      | (   ) || | \   |             | |   ) || |   | |
| () () || (____/\         | (____/\| )   ( || )  \  |             | (__/  )| (___) |
(_______)(_______/         (_______/|/     \||/    )_)             (______/ (_______)
                                                                   
_________         _________ _______  _  _ 
\__   __/|\     /|\__   __/(  ____ \( )( )
   ) (   | )   ( |   ) (   | (    \/| || |
   | |   | (___) |   | |   | (_____ | || |
   | |   |  ___  |   | |   (_____  )| || |
   | |   | (   ) |   | |         ) |(_)(_)
   | |   | )   ( |___) (___/\____) | _  _ 
   )_(   |/     \|\_______/\_______)(_  _)
"""


# global arrays
cars: List[Car] = []
streets: List[Street] = []
intersections: List[Intersection] = []

for _ in range(int(intersection_len)):
    intersections.append(Intersection())


def output():
    print(len(intersections))

    for intersection in intersections:
        print(intersections.index(intersection))
        print(len(intersection.schedules))
        for schedule in intersection.schedules:
            print(f'{schedule.street.name} {schedule.period}')


for _ in range(int(street_len)):
    [start, end, name, length] = [v.strip()
                                  for v in input().strip().split(' ')]
    streets.append(
        Street(
            start=int(start),
            end=int(end),
            name=name,
            length=length
        )
    )

for _ in range(int(car_len)):
    paths = [v.strip() for v in input().strip().split(' ')]
    # convert to Street objects
    path_len = int(paths.pop(0))
    assert(len(paths) == path_len)
    paths = [street for path in paths for street in streets if street.name == path]
    cars.append(
        Car(streets=paths)
    )

# array of time to roads with traffic (queue > 0)
#

# schedule = Time => Intersection[]
#            Intersection => Road[]
#            Road => Queue


def gen_schedule():
    for i in range(intersection_len):
        streets = [street for street in streets if street.end == i]
        for street in streets:
            for window in range(1, duration):
                yield Schedule(street, window)


# simulate correct answer:

intersections[0].add_schedule(Schedule(streets[0], 2))
intersections[1].add_schedule(Schedule(streets[2], 2))
intersections[1].add_schedule(Schedule(streets[1], 1))
intersections[2].add_schedule(Schedule(streets[3], 1))


while duration:
    duration -= 1
    for intersection in intersections:
        if intersection.active_schedule == None:
            continue
        intersection.increment(initial - duration)

    for street in streets:
        street.pop_queue()


output()
