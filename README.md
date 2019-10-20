
<p align="center"><img src="http://i.imgur.com/wOGZico.png" width="300" align="middle"></p>


# USFQ-Traffic-in-Ecuador
Research in data analysis, machine learning and mathematical modeling, leading to solve complex logistics problems in various industries across Ecuador, Mexico, and other countries of Latin America. Project lead by University of San Fransicso in Quito, in Cooperation with MIT Center for Transportation and Logistics.


## Overview

The street has a limited number of parking places. Some of them are common and some part of it is reserved for trucks which deliver goods to the stores. Cars randomly arrive at the street and park on the spots, however after some time all the places are occupied. New, upcoming cars are forced to stop at the street, what leads to the traffic jams. In this project we create a Discrete Event Simulation (DES) to mimic and analyse the traffic, basing on real data collected on the streets of Quito, Ecuador. We believe that this project will allow to simplify logistic and transport processes and in result will lead to solving the problem of traffic jams.

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
- 0 - parking in the selected zone
- 1 - small disruption (<5 minutes)
- 2 - significant disruption (>5 minutes)
- 3 - big disruption (>15 minutes)

Moreover, we also analyse the time of parking and specific part of the street:
- SUR-NORTE (station C)
- NORTE-SUR (station D)



### How to run?
>~~~~
>git clone https://github.com/Borzyszkowski/USFQ-Traffic-in-Ecuador.git
>pip install simpy
>python traffic_simulation.py
>~~~~



### Usefull links

* [SimPy](https://simpy.readthedocs.io/en/latest/) - SimPy is a process-based discrete-event simulation framework based on standard Python.
* [Fulcrum App](https://www.fulcrumapp.com/) - Fulcrum is a mobile data collection platform that allows to easily build mobile forms & collect data.
* [USFQ DIE](https://www.usfq.edu.ec/programas_academicos/colegios/politecnico/Paginas/default.aspx) - Universidad San Francisco de Quito: Department of Industrial Engineering
* [MIT CTL](https://ctl.mit.edu/) - Massachusetts Institute of Technology:
 Center for Transportation and Logistics

