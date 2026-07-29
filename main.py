import random
import simpy

# ---------------------------------------------------------
# SIMULATION CONFIGURATION (The Parameters You Control)
# ---------------------------------------------------------
RANDOM_SEED = 42
NUM_TECHNICIANS = 2        # Number of available maintenance teams
MEAN_ARRIVAL_INTERVAL = 3  # A new aircraft arrives every ~3 hours
MAINTENANCE_TIME = 5       # It takes ~5 hours to service an aircraft
SIM_TIME = 48              # Run the simulation for 48 hours total

# Tracking metrics
wait_times = []


def aircraft(env, name, hangar):
    """
    Represents an individual aircraft arriving for maintenance.
    """
    arrival_time = env.now
    print(f"✈️  [{arrival_time:.1f} hrs] {name} arrived at the facility.")

    # Request an available technician team (Resource)
    with hangar.request() as request:
        yield request  # Wait in line until a technician is free

        wait = env.now - arrival_time
        wait_times.append(wait)
        print(f"🔧 [{env.now:.1f} hrs] {name} entering maintenance bay (Waited: {wait:.1f} hrs).")

        # Simulate the actual maintenance work being done
        service_duration = random.expovariate(1.0 / MAINTENANCE_TIME)
        yield env.timeout(service_duration)

        print(f"✅ [{env.now:.1f} hrs] {name} maintenance complete and departed.")


def aircraft_generator(env, hangar):
    """
    Generates new aircraft arriving at the facility over time.
    """
    aircraft_count = 0
    while True:
        # Wait a random time before the next aircraft arrives
        yield env.timeout(random.expovariate(1.0 / MEAN_ARRIVAL_INTERVAL))
        aircraft_count += 1
        env.process(aircraft(env, f"Aircraft-{aircraft_count}", hangar))


# ---------------------------------------------------------
# RUN THE SIMULATION
# ---------------------------------------------------------
print("=== STARTING AIRCRAFT MAINTENANCE SIMULATION ===")
random.seed(RANDOM_SEED)

# Create the SimPy Environment and Hangar Resource
env = simpy.Environment()
hangar = simpy.Resource(env, capacity=NUM_TECHNICIANS)

# Start generating aircraft and run for 48 hours
env.process(aircraft_generator(env, hangar))
env.run(until=SIM_TIME)

# Calculate results
avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
print("\n=== SIMULATION SUMMARY ===")
print(f"Total Aircraft Processed: {len(wait_times)}")
print(f"Average Queue Wait Time: {avg_wait:.2f} hours")
