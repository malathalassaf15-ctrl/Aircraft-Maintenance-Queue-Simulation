import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import simpy

# ---------------------------------------------------------
# GLOBAL EXPERIMENT CONFIGURATION
# ---------------------------------------------------------
RANDOM_SEED = 42
MEAN_ARRIVAL_INTERVAL = 2.5  # Aircraft arrive every ~2.5 hours
MAINTENANCE_TIME = 6.0  # Maintenance takes ~6 hours
SIM_TIME = 5000  # Long simulation run for statistical accuracy

# Financial Parameters for Cost Trade-off Analysis
COST_PER_TECH_PER_HOUR = 50  # $50/hr technician wage
COST_PER_DELAY_HOUR = 1500  # $1500/hr downtime penalty for grounded aircraft


def aircraft_process(env, name, hangar, metrics):
    arrival_time = env.now
    with hangar.request() as request:
        yield request
        wait_time = env.now - arrival_time
        metrics["wait_times"].append(wait_time)

        service_duration = random.expovariate(1.0 / MAINTENANCE_TIME)
        metrics["service_times"].append(service_duration)
        yield env.timeout(service_duration)


def aircraft_generator(env, hangar, metrics):
    count = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / MEAN_ARRIVAL_INTERVAL))
        count += 1
        env.process(aircraft_process(env, f"Aircraft-{count}", hangar, metrics))


def run_experiment(num_technicians):
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    hangar = simpy.Resource(env, capacity=num_technicians)

    metrics = {"wait_times": [], "service_times": []}

    env.process(aircraft_generator(env, hangar, metrics))
    env.run(until=SIM_TIME)

    total_aircraft = len(metrics["wait_times"])
    avg_wait = (
        sum(metrics["wait_times"]) / total_aircraft if total_aircraft > 0 else 0
    )
    total_wait_hours = sum(metrics["wait_times"])

    # Financial Cost Calculations
    labour_cost = num_technicians * COST_PER_TECH_PER_HOUR * SIM_TIME
    delay_cost = total_wait_hours * COST_PER_DELAY_HOUR
    total_cost = labour_cost + delay_cost

    return {
        "Technicians": num_technicians,
        "Total Aircraft": total_aircraft,
        "Avg Wait (Hrs)": round(avg_wait, 2),
        "Labour Cost ($)": round(labour_cost, 2),
        "Delay Cost ($)": round(delay_cost, 2),
        "Total Cost ($)": round(total_cost, 2),
    }


# ---------------------------------------------------------
# EXECUTE MULTI-SCENARIO TRADE-OFF ANALYSIS
# ---------------------------------------------------------
results = []
staffing_levels = range(2, 7)  # Test 2 to 7 technicians

for techs in staffing_levels:
    res = run_experiment(techs)
    results.append(res)

df = pd.DataFrame(results)

print("=== INDUSTRIAL ENGINEERING TRADE-OFF ANALYSIS ===")
print(df.to_string(index=False))

# ---------------------------------------------------------
# GENERATE PUBLICATION-READY DASHBOARD CHART
# ---------------------------------------------------------
sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Total Operating Cost
color = "tab:red"
ax1.set_xlabel("Number of Technician Teams", fontsize=12, fontweight="bold")
ax1.set_ylabel("Total Operating Cost ($)", color=color, fontsize=12, fontweight="bold")
ax1.plot(
    df["Technicians"],
    df["Total Cost ($)"],
    color=color,
    marker="o",
    linewidth=2.5,
    label="Total Cost ($)",
)
ax1.tick_params(axis="y", labelcolor=color)

# Plot Average Wait Time on secondary axis
ax2 = ax1.twinx()
color = "tab:blue"
ax2.set_ylabel(
    "Average Wait Time (Hours)", color=color, fontsize=12, fontweight="bold"
)
ax2.plot(
    df["Technicians"],
    df["Avg Wait (Hrs)"],
    color=color,
    marker="s",
    linestyle="--",
    linewidth=2.5,
    label="Avg Wait (Hrs)",
)
ax2.tick_params(axis="y", labelcolor=color)

plt.title(
    "Aircraft Maintenance Capacity Planning: Cost vs. Queue Bottleneck",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
fig.tight_layout()
plt.savefig("optimization_dashboard.png", dpi=300)
print("\n[SUCCESS] Generated high-resolution graph: 'optimization_dashboard.png'")
