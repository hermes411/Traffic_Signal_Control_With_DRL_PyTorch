from environment import TrafficEnv
from dqn import DQNAgent
import matplotlib.pyplot as plt

NE_HIGHWAY_ID = 'hwn'
SE_HIGHWAY_ID = 'hws'
TLS_INT1_ID = 'int1'
NS_GREEN_PHASE = 0
WE_GREEN_PHASE = 4
INT1_W = 'we1'
INT1_E = 'ew3'
INT1_N = 'int1ns1'
INT1_S = 'int1sn1'
INT_SPEED_LIMIT = 15.64

if __name__ == '__main__':
    env = TrafficEnv(
        sumocfg_file_name='run.sumocfg',
        log_file_name='log.txt',
        time_steps=3600,
        n_id=INT1_N, 
        e_id=INT1_E, 
        s_id=INT1_S, 
        w_id=INT1_W, 
        tls_id=TLS_INT1_ID,
        n_highway_id=NE_HIGHWAY_ID,
        s_highway_id=SE_HIGHWAY_ID, 
        green_time=10,
        yellow_time=6,
        use_gui=False
    )

    agent = DQNAgent(
        state_size=12, 
        action_size=2,
        gamma=0.95,
        epsilon=0.1,
        learning_rate=0.0002,
        update_rate=0.001)

    num_episodes = 100
    batch_size = 32
    rewards = []

    for episode in range(num_episodes):
        state, info = env.reset()
        total_reward = 0
        truncated = False

        count = 0

        while not truncated:
            action = agent.act(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            agent.remember(state, action, reward, next_state, truncated)
            state = next_state
            total_reward += reward
            count += 1

            agent.replay(batch_size)
        
        agent.update_target_model()
        
        rewards.append(total_reward / count)
    
    state, info = env.reset()
    info = list(info.values())

    # write to log file
    log = open('log.txt', 'a')
    for i in range(num_episodes):
        log.write('episode: ' + str(i) + ',  Average Staying Time Per Vehicle: ' + str(info[i]) + ', Average Reward Per Episode: ' + str(rewards[i]) + '\n')
    log.close()

    # First plot (in the first window)
    fig1, ax1 = plt.subplots()  # Create a figure and axes for the first plot
    ax1.plot(range(num_episodes), rewards)
    ax1.set_title('Average Reward Per Episode')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Average Reward')

    # Second plot (in the second window)
    fig2, ax2 = plt.subplots()  # Create a figure and axes for the second plot
    ax2.plot(range(num_episodes), info)
    ax2.set_title('Average Staying Time Per Vehicle Per Episode')
    ax2.set_xlabel('Episode')
    ax2.set_ylabel('Average Staying Time Per Vehicle')

    # Display both plots
    plt.show()
