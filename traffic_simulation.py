"""
Traffic in Quito simulation

Scenario:
    The street has a limited number of parking places. Some of them are common and some part of it is reserved for
    trucks which deliver goods to the stores. Cars randomly arrive at the street and park on the spots, however
    after some time all the places are occupied. New, upcoming cars are forced to stop at the street, what leads to
    the traffic jams. In this project we simulate the traffic and analyse it basing on the real data collected
    on the streets in Quito, Ecuador. We believe that this project will allow to simplify logistic and transport
    processes and in result will lead to solving the problem of traffic jams.

Types of vehicles:
1. Big Truck
2. Medium Truck
3. Small Truck
4. Regular Car
5. Motorcycle

Reason of parking:
1. Delivery of goods
2. Transport of people

Level of disruption:
0 - parking in the selected zone
1 - small disruption (<5 minutes)
2 - significant disruption (>5 minutes)
3 - big disruption (>15 minutes)

Moreover, we also analyse the time of parking and specific part of the street:
- SUR-NORTE (station C)
- NORTE-SUR (station D)

Bartlomiej Borzyszkowski,
Universidad San Francisco de Quito

"""

import itertools
import random
import simpy
import csv

data_file_path = 'paradas_y_parqueos.csv'
RANDOM_SEED = 42
PARKING_SPOTS_NO = 50  # Number of parking spots in the street
THRESHOLD = 10  # Threshold to inform when the parking is becoming full (in %)
FULL_DELIVERY_SIZE = 50  # Nominated value
DELIVERY_SPEED = 2  # Size / second
SIM_TIME = 10000  # Simulation time in seconds
DELIVERY_LEVEL = [5, 25]  # Min/max levels of goods to delivery (Nominated value)
T_INTER = [30, 300]  # Create a car every [min, max] seconds


class Event:
    """Class of events, where each of them has a unique id and an information stored as a dictionary"""

    def __init__(self, event_type, event_name, category, classes):
        self.event_type = event_type
        self.id = event_name
        self.original_data = category
        self.information = self.create_frame(category, classes)

    def create_frame(self, category, classes):
        info = classes
        counter = 0
        for i in info:
            info[i] = category[counter]
            counter += 1
        return info


def pursue_data(path):
    """Reads the data from a given csv file. Creates objects which are saved in the list of all events."""
    with open(path, 'r', encoding="utf8") as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',')
        for row in csv_file:
            class_names = row
            break
        classes = {}
        for i in class_names:
            classes[i] = []
        all_events = []
        arrivals = []
        for category in csv_file:
            event_name = category[0]
            car_arrival = Event('arrival', event_name, category, classes.copy())
            all_events.append(car_arrival)
            arrivals.append(car_arrival)
            if category[22]:
                car_leave = Event('leave', event_name, category, classes.copy())
                all_events.append(car_leave)
        print('Number of arriving cars: ', len(arrivals))
        print('Total unmber of events: ', len(all_events), '\n')
        return all_events


def sort_data(data):
    """Sorts the data using QuickSort, depending on the time of event."""

    # This function takes last element as pivot, places
    # the pivot element at its correct position in sorted
    # array, and places all smaller (smaller than pivot)
    # to left of pivot and all greater elements to right of pivot
    def partition(arr, low, high):
        i = (low - 1)  # index of smaller element
        if arr[high].event_type == 'arrival':
            pivot = arr[high].information['hora_a_la_que_comenz_el_parqueo'].replace(":", "")  # pivot
        else:
            pivot = arr[high].information['hora_a_la_que_finaliz_el_parqueo'].replace(":", "")  # pivot
        pivot = int(float(pivot))

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if arr[j].event_type == 'arrival':
                equal = arr[j].information['hora_a_la_que_comenz_el_parqueo'].replace(":", "")
            else:
                equal = arr[j].information['hora_a_la_que_finaliz_el_parqueo'].replace(":", "")
            try:
                equal = int(equal)
            except ValueError:
                equal = 0
            if equal <= pivot:
                # increment index of smaller element
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    # The main function that implements QuickSort

    # arr[] --> Array to be sorted,
    # low  --> Starting index,
    # high  --> Ending index

    # Function to do Quick sort
    def quick_sort(arr, low, high):
        if low < high:
            # pi is partitioning index, arr[p] is now
            # at right place
            pi = partition(arr, low, high)

            # Separately sort elements before
            # partition and after partition
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)
        return arr

    n = len(data)
    return quick_sort(data, 0, n - 1)


def car(name, env, street, parking, data):
    """A car arrives at the parking to stop there.

    It requests one parking spot to sop. If the parking spots are fully occupied,
    the car stops and leads to a traffic jam.

    """
    delivery_level = random.randint(*DELIVERY_LEVEL)

    # it is possible to print every information about an event from the dataset here
    if data.event_type == 'arrival':
        print('Real time of arrival: ', data.information['hora_a_la_que_comenz_el_parqueo'])
    else:
        print('End of parking: ', data.information['hora_a_la_que_finaliz_el_parqueo'])
    print('%s arriving at street at simuation artificial time %.1f' % (name, env.now))
    print('Location of the car: ', data.information['sentido_de_la_calle_donde_estacion'])
    print('Type of the car: ', data.information['tipo_de_vehculo'])
    print('Reason for parking: ', data.information['propsito_del_parqueo'])
    print('Level of disruption: ', data.information['nivel_de_disrupcin'])
    print('Event number: ', data.id)

    with street.request() as req:
        start = env.now
        # Request one parking spot
        yield req

        # Get the required delivery
        delivery_required = FULL_DELIVERY_SIZE - delivery_level
        yield parking.get(delivery_required)

        # The "actual" delivery process takes some time
        yield env.timeout(delivery_required / DELIVERY_SPEED)

        print('%s finished delivery in simuation artificial time %.1f seconds.' % (name, env.now - start))


def traffic_control(env, parking):
    """Periodically check the capacity of the *parking* and inform if the number of spots falls below a threshold."""
    while True:
        if parking.level / parking.capacity * 100 < THRESHOLD:
            # The parking is becoming full
            print('Parking is becoming full at %d' % env.now)
        yield env.timeout(10)  # Check every 10 seconds


def car_generator(env, street, parking, data):
    """Generate new cars that arrive at the street."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(car('Car %d' % i, env, street, parking, data[i]))
        print()


if __name__ == "__main__":
    # Setup and start the simulation
    print(f'Reading the data from a specified path ({data_file_path}).')
    data = pursue_data(data_file_path)
    data = sort_data(data)
    print('Traffic in Quito simulation: ')
    random.seed(RANDOM_SEED)

    # Create environment and start processes
    env = simpy.Environment()
    street = simpy.Resource(env, 2)

    parking = simpy.Container(env, PARKING_SPOTS_NO, init=PARKING_SPOTS_NO)

    env.process(traffic_control(env, parking))
    env.process(car_generator(env, street, parking, data))

    # Execute!
    env.run(until=SIM_TIME)
