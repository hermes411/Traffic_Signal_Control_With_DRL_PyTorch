import os
import sys

if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from generator import TrafficGenerator

class TrafficEnv(gym.Env):
    def __init__(
        self,
        sumocfg_file_name,
        log_file_name,
        time_steps,
        n_id, 
        e_id, 
        s_id, 
        w_id, 
        tls_id,
        n_highway_id,
        s_highway_id, 
        green_time,
        yellow_time,
        use_gui = False):

        if use_gui:
            self._sumo_binary = checkBinary("sumo-gui")
        else:
            self._sumo_binary = checkBinary("sumo")

        self.sumocfg_file_name = sumocfg_file_name
        self.log_file_name = log_file_name
        self.time_steps = time_steps
        self.n_id = n_id
        self.e_id = e_id
        self.s_id = s_id
        self.w_id = w_id
        self.tls_id = tls_id
        self.n_highway_id = n_highway_id
        self.s_highway_id = s_highway_id
        self.green_time = green_time
        self.yellow_time = yellow_time

        self.average_staying_time_per_vehicle = {}
        self.episode = 0
        self.sumo_step = 0
        self.traffic_generator = TrafficGenerator(time_steps)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=np.zeros(12), high=(np.ones(12) * np.inf), dtype=np.float32)

    def step(self, action):
        #reward1 = self.compute_reward()
        if action is None or self.prev_action is None or self.prev_action == action:
            # chosen action is the same so keep traffic signal light unchanged
            phase = traci.trafficlight.getPhase(self.tls_id)

            for i in range(self.green_time):
                traci.trafficlight.setPhase(self.tls_id, phase)
                self.sumo_step += 1
                traci.simulationStep()
                self.update_highway_speeds(self.highway_speeds, self.n_highway_id)
                self.update_highway_speeds(self.highway_speeds, self.s_highway_id)
                self.update_staying_times()
        else:
            # chosen action is not the same
            # transition phase
            phase = traci.trafficlight.getPhase(self.tls_id)

            for i in range(self.yellow_time): # turn on yellow light for either NS traffic or WE traffic
                traci.trafficlight.setPhase(self.tls_id, phase + 1)
                self.sumo_step += 1
                traci.simulationStep()
                self.update_highway_speeds(self.highway_speeds, self.n_highway_id)
                self.update_highway_speeds(self.highway_speeds, self.s_highway_id)
                self.update_staying_times()
            for i in range(self.green_time): # turn on green light for left turn
                traci.trafficlight.setPhase(self.tls_id, phase + 2)
                self.sumo_step += 1
                traci.simulationStep()
                self.update_highway_speeds(self.highway_speeds, self.n_highway_id)
                self.update_highway_speeds(self.highway_speeds, self.s_highway_id)
                self.update_staying_times()
            for i in range(self.yellow_time): # turn on yellow light for left turn
                traci.trafficlight.setPhase(self.tls_id, phase + 3)
                self.sumo_step += 1
                traci.simulationStep()
                self.update_highway_speeds(self.highway_speeds, self.n_highway_id)
                self.update_highway_speeds(self.highway_speeds, self.s_highway_id)
                self.update_staying_times()
            
            # turn on green light for phase transitioning to
            for i in range(self.green_time):
                traci.trafficlight.setPhase(self.tls_id, (phase + 4) % 8)
                self.sumo_step += 1
                traci.simulationStep()
                self.update_highway_speeds(self.highway_speeds, self.n_highway_id)
                self.update_highway_speeds(self.highway_speeds, self.s_highway_id)
                self.update_staying_times()
        
        self.prev_action = action
        reward2 = -self.compute_reward()
        #reward = reward1 - reward2

        truncated = False

        if self.sumo_step >= self.time_steps or traci.simulation.getMinExpectedNumber() <= 0:
            truncated = True
        
        return self.get_state(), reward2, False, truncated, {}

    def reset(self, seed=None, options=None):
        '''
        Reset the environment.
        '''
        super().reset(seed=seed)

        if self.episode != 0:
            self.close()
            self.average_staying_time_per_vehicle[self.episode] = np.mean(self.staying_time_per_vehicle)
        
        self.episode += 1

        self.traffic_generator.generate_routefile(seed)
        self._start_simulation()

        self.prev_action = None
        self.staying_times = {self.n_id: {}, self.e_id: {}, self.s_id: {}, self.w_id: {}}
        self.num_vehicles = {self.n_id: 0, self.e_id: 0, self.s_id: 0, self.w_id: 0}
        self.staying_time_per_vehicle = []
        self.sumo_step = 0
        self.vehicles = dict()
        self.highway_speeds = {} # key is vehID and value is the speed they entered the highway

        return self.get_state(), self.average_staying_time_per_vehicle

    def close(self):
        '''
        Closes the environment and stops the SUMO simulation.
        '''
        traci.close(wait=False)

    def get_state(self):
        '''
        Get the state of the SUMO environment.
        '''
        state = [0] * 12
        roads = [self.n_id, self.e_id, self.s_id, self.w_id]
        for i in range(len(roads)):
            for vehID in traci.edge.getLastStepVehicleIDs(roads[i]):
                state[i * 3 + traci.vehicle.getLaneIndex(vehID)] += 1

        return np.array(state, dtype=np.float32)

    def compute_reward(self):
        '''
        Computes the reward.
        '''
        reward = 0
        self.remove_departed_vehicles()
        avg_staying_times = []
        overall_avg_staying_time = 0
        for road in [self.n_id, self.e_id, self.s_id, self.w_id]:
            avg_staying_time = self.avg_staying_time_of_road(road)
            avg_staying_times.append(avg_staying_time)
            overall_avg_staying_time += avg_staying_time
        
        overall_avg_staying_time /= 4

        for avg_staying_time in avg_staying_times:
            reward += abs(overall_avg_staying_time - avg_staying_time)
        
        return reward

    def remove_departed_vehicles(self):
        '''
        Remove the vehicles that have left the intersection from the dictionary of staying times.
        '''
        roads = [self.n_id, self.e_id, self.s_id, self.w_id]
        vehicles_in_roads = []
        for road in roads:
            vehicles_in_roads += traci.edge.getLastStepVehicleIDs(road)
        for road in self.staying_times:
            for vehID, staying_time in list(self.staying_times[road].items()):
                if vehID not in vehicles_in_roads:
                    self.staying_time_per_vehicle.append(self.staying_times[road][vehID])
                    del self.staying_times[road][vehID]
                    self.num_vehicles[road] -= 1

    def update_staying_times(self):
        '''
        Update the staying time of all vehicles in the intersection.
        '''
        roads = [self.n_id, self.e_id, self.s_id, self.w_id]
        for road in roads:
            for vehID in traci.edge.getLastStepVehicleIDs(road):
                if vehID not in self.staying_times[road]:
                    self.staying_times[road][vehID] = 1
                    self.num_vehicles[road] += 1
                else:
                    self.staying_times[road][vehID] += 1

    def avg_staying_time_of_road(self, road):
        '''
        Get the average staying time of a particular road.
        '''
        return 0 if self.num_vehicles[road] == 0 else (sum(self.staying_times[road].values()) / self.num_vehicles[road])

    def update_highway_speeds(self, highway_speeds: dict, highway_id: str) -> None:
        '''Check if a vehicle has just entered the highway. If they did, add the
        speed with the vehID as the key to the dictionary.'''
        for vehID in traci.edge.getLastStepVehicleIDs(highway_id):
                if vehID not in highway_speeds:
                    highway_speeds[vehID] = traci.vehicle.getSpeed(vehID)

    def average_highway_speed(self, highway_speeds: dict):
        '''
        Calculate the average highway speed.
        '''
        return sum(list(highway_speeds.values())) / len(list(highway_speeds.values()))

    def _start_simulation(self):
        '''
        Starts the SUMO simulation.
        '''
        sumo_cmd = [
            self._sumo_binary, 
            "-c", 
            os.path.join('config', self.sumocfg_file_name), 
            "--no-step-log", 
            "true"
        ]

        traci.start(sumo_cmd)
    
