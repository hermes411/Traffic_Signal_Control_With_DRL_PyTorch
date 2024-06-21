import numpy as np

class TrafficGenerator:
    def __init__(self, time_steps):
        self._timp_steps = time_steps
        self._num_cars = 0

    def generate_routefile(self, seed):
        '''
        Generate the route file.
        '''

        np.random.seed(seed)    # make tests reproducible

        # demand per second for different destinations
        pW1 = 1. / 10
        pN1 = 1. / 14
        pS1 = 1. / 14
        pN2 = 1. / 17
        pS2 = 1. / 17
        pHN = 1. / 30
        pHS = 1. / 25

        with open('config/routes.rou.xml', 'w') as routes:
            print('''<routes>\n\t<vType id="average_car" vClass="passenger" accel="3" decel="4.5" minGap="2.5" maxSpeed="45" />
            ''', file=routes)

            # routes leading to north highway
            print('    <route id="W1_HN" edges="we1 we2 we3 we4 hwn" />', file=routes)
            print('    <route id="N1_HN" edges="int1ns1 we2 we3 we4 hwn" />', file=routes)
            print('    <route id="S1_HN" edges="int1sn1 we2 we3 we4 hwn" />', file=routes)
            print('    <route id="N2_HN" edges="int2ns1 we3 we4 hwn" />', file=routes)
            print('    <route id="S2_HN" edges="int2sn1 we3 we4 hwn" />', file=routes)

            # routes leading to the south highway
            print('    <route id="W1_HS" edges="we1 we2 we3 se1 hws" />', file=routes)
            print('    <route id="N1_HS" edges="int1ns1 we2 we3 se1 hws" />', file=routes)
            print('    <route id="S1_HS" edges="int1sn1 we2 we3 se1 hws" />', file=routes)
            print('    <route id="N2_HS" edges="int2ns1 we3 se1 hws" />', file=routes)
            print('    <route id="S2_HS" edges="int2sn1 we3 se1 hws" />', file=routes)

            # routes leading to north road of intersection two
            print('    <route id="W1_N2" edges="we1 we2 int2sn2" />', file=routes)
            print('    <route id="N1_N2" edges="int1ns1 we2 int2sn2" />', file=routes)
            print('    <route id="S1_N2" edges="int1sn1 we2 int2sn2" />', file=routes)
            print('    <route id="S2_N2" edges="int2sn1 int2sn2" />', file=routes)
            print('    <route id="HN_N2" edges="-hwn ew1 ew2 int2sn2" />', file=routes)
            print('    <route id="HS_N2" edges="-hws nw1 ew2 int2sn2" />', file=routes)

            # routes leading to south road of intersection two
            print('    <route id="W1_S2" edges="we1 we2 int2ns2" />', file=routes)
            print('    <route id="N1_S2" edges="int1ns1 we2 int2ns2" />', file=routes)
            print('    <route id="S1_S2" edges="int1sn1 we2 int2ns2" />', file=routes)
            print('    <route id="N2_S2" edges="int2ns1 int2ns2" />', file=routes)
            print('    <route id="HN_S2" edges="-hwn ew1 ew2 int2ns2" />', file=routes)
            print('    <route id="HS_S2" edges="-hws nw1 ew2 int2ns2" />', file=routes)

            # routes leading to north road of intersection one
            print('    <route id="W1_N1" edges="we1 int1sn2" />', file=routes)
            print('    <route id="S1_N1" edges="int1sn1 int1sn2" />', file=routes)
            print('    <route id="N2_N1" edges="int2ns1 ew3 int1sn2" />', file=routes)
            print('    <route id="S2_N1" edges="int2sn1 ew3 int1sn2" />', file=routes)
            print('    <route id="HN_N1" edges="-hwn ew1 ew2 ew3 int1sn2" />', file=routes)
            print('    <route id="HS_N1" edges="-hws nw1 ew2 ew3 int1sn2" />', file=routes)

            # routes leading to south road of intersection one
            print('    <route id="W1_S1" edges="we1 int1ns2" />', file=routes)
            print('    <route id="N1_S1" edges="int1ns1 int1ns2" />', file=routes)
            print('    <route id="N2_S1" edges="int2ns1 ew3 int1ns2" />', file=routes)
            print('    <route id="S2_S1" edges="int2sn1 ew3 int1ns2" />', file=routes)
            print('    <route id="HN_S1" edges="-hwn ew1 ew2 ew3 int1ns2" />', file=routes)
            print('    <route id="HS_S1" edges="-hws nw1 ew2 ew3 int1ns2" />', file=routes)

            # routes leading to west road of intersection one
            print('    <route id="N1_W1" edges="int1ns1 ew4" />', file=routes)
            print('    <route id="S1_W1" edges="int1sn1 ew4" />', file=routes)
            print('    <route id="N2_W1" edges="int2ns1 ew3 ew4" />', file=routes)
            print('    <route id="S2_W1" edges="int2sn1 ew3 ew4" />', file=routes)
            print('    <route id="HN_W1" edges="-hwn ew1 ew2 ew3 ew4" />', file=routes)
            print('    <route id="HS_W1" edges="-hws nw1 ew2 ew3 ew4" />', file=routes)
        
            for i in range(self._timp_steps):
                # destination is west road of intersection one
                if np.random.uniform() < pW1:
                    rl = np.random.uniform()
                    if rl < 0.25:  # take a route with a left turn 
                        route_choice = np.random.randint(1, 4)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="S1_W1_%i" type="average_car" route="N1_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S2_W1_%i" type="average_car" route="N2_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="HS_W1_%i" type="average_car" route="N2_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        self._num_cars += 1
                    else: # take one of the reamining routes
                        route_choice = np.random.randint(1, 4)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N1_W1_%i" type="average_car" route="N1_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="N2_W1_%i" type="average_car" route="N2_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="HN_W1_%i" type="average_car" route="N2_W1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is north road of intersection one
                if np.random.uniform() < pN1:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn 
                        route_choice = np.random.randint(1, 4)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="W1_N1_%i" type="average_car" route="W1_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S2_N1_%i" type="average_car" route="S2_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="HS_N1_%i" type="average_car" route="HS_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn 
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N2_N1_%i" type="average_car" route="N2_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="HN_N1_%i" type="average_car" route="HN_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the remaining route with no turns
                        print('    <vehicle id="S1_N1_%i" type="average_car" route="S1_N1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is south road of intersection one
                if np.random.uniform() < pS1:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn 
                        route_choice = np.random.randint(1, 5)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N2_S1_%i" type="average_car" route="N2_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S2_S1_%i" type="average_car" route="S2_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="HS_S1_%i" type="average_car" route="HS_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        elif route_choice == 4:
                            print('    <vehicle id="HN_S1_%i" type="average_car" route="HN_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn 
                        print('    <vehicle id="W1_S1_%i" type="average_car" route="W1_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the remaining route with no turns
                        print('    <vehicle id="N1_S1_%i" type="average_car" route="N1_S1" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is north road of intersection two
                if np.random.uniform() < pN2:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn 
                        route_choice = np.random.randint(1, 5)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="W1_N2_%i" type="average_car" route="W1_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="N1_N2_%i" type="average_car" route="N1_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="S1_N2_%i" type="average_car" route="S1_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        elif route_choice == 4:
                            print('    <vehicle id="HS_N2_%i" type="average_car" route="HS_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn 
                        print('    <vehicle id="HN_N2_%i" type="average_car" route="HN_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the remaining route with no turns
                        print('    <vehicle id="S2_N2_%i" type="average_car" route="S2_N2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is south road of intersection two
                if np.random.uniform() < pS2:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn 
                        route_choice = np.random.randint(1, 4)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N1_S2_%i" type="average_car" route="N1_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="HN_S2_%i" type="average_car" route="HN_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 3:
                            print('    <vehicle id="HS_S2_%i" type="average_car" route="HS_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)                        
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="W1_S2_%i" type="average_car" route="W1_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S1_S2_%i" type="average_car" route="S1_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the remaining route with no turns
                        print('    <vehicle id="N2_S2_%i" type="average_car" route="N2_S2" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is the north highway
                if np.random.uniform() < pHN:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn not including turn to enter highway
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N1_HN_%i" type="average_car" route="N1_HN" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="N2_HN_%i" type="average_car" route="N2_HN" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="S1_HN_%i" type="average_car" route="S1_HN" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S2_HN_%i" type="average_car" route="S2_HN" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the route with only turn being turn into highway
                        print('    <vehicle id="W1_HN_%i" type="average_car" route="W1_HN" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1

                # destination is the south highway
                if np.random.uniform() < pHS:
                    rls = np.random.uniform()
                    if rls < 0.25:  # take a route with a left turn
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="N1_HS_%i" type="average_car" route="N1_HS" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="N2_HS_%i" type="average_car" route="N2_HS" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    elif rls < 0.55: # take one of the remaining routes with a right turn
                        route_choice = np.random.randint(1, 3)   # choose a random source
                        if route_choice == 1:
                            print('    <vehicle id="S1_HS_%i" type="average_car" route="S1_HS" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        elif route_choice == 2:
                            print('    <vehicle id="S2_HS_%i" type="average_car" route="S2_HS" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
                    else: # take the route with only turn being turn into highway
                        print('    <vehicle id="W1_HS_%i" type="average_car" route="W1_HS" depart="%i" departLane="random" />' % (self._num_cars, i), file=routes)
                        self._num_cars += 1
  
            print('</routes>', file=routes)
        
        self._num_cars = 0