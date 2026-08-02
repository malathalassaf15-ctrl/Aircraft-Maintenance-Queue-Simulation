import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import simpy
import streamlit as st

# Streamlit Page Setup
st.set_page_config(
    page_title="Aircraft Maintenance Capacity Simulator", layout="wide"
)
st.title("✈️ Aircraft Maintenance Operations & Capacity Optimization")
st.write(
    "Adjust the operational inputs in the sidebar to simulate hangar queue bottlenecks, "
    "analyze wait times, and find the cost-optimal staffing level."
)

# Sidebar Configuration Controls
st.sidebar.header("⚙️ Simulation Parameters")
num_technicians = st.sidebar.slider("Technician Teams", 1, 10, 5)
arrival_interval = st.sidebar.slider(
    "Mean Arrival Interval (Hours)", 1.0, 5.0, 2.5
)
maintenance_time = st.sidebar.slider(
    "Mean Maintenance Duration (Hours)", 2.0, 10.0, 6.0
)
sim_time = st.sidebar.slider("Simulation Time Horizon (Hours)", 500, 5000, 5000)
tech_cost = st.sidebar.number_input("Labor Cost ($/hr)", value=50)
delay_cost = st.sidebar.number_input("Aircraft Delay Penalty ($/hr)", value=1500)


# Core Simulation Logic
def aircraft_process(
    env, name, hangar, metrics, maintenance_time, delay_cost_rate
):
    arrival_time = env.now
    with hangar.request() as request:
        yield request
        wait_time = env.now - arrival_time
        metrics["wait_times"].append(wait_time)
        service_duration = random.expovariate(1.0 / maintenance_time)
        metrics["service_times"].append(service_duration)
        yield env.timeout(service_duration)


def aircraft_generator(
    env, hangar, metrics, arrival_interval, maintenance_time, delay_cost_rate
):
    count = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        count += 1
        env.process(
            aircraft_process(
                env,
                f"Aircraft-{count}",
                hangar,
                metrics,
                maintenance_time,
                delay_cost_rate,
            )
        )


# Run Simulation Button
if st.button("🚀 Run Live Optimization Analysis"):
    random.seed(42)
    env = simpy.Environment()
    hangar = simpy.Resource(env, capacity=num_technicians)
    metrics = {"wait_times": [], "service_times": []}
    env.process(
        aircraft_generator(
            env,
            hangar,
            metrics,
            arrival_interval,
            maintenance_time,
            delay_cost,
        )
    )
    env.run(until=sim_time)
    total_aircraft = len(metrics["wait_times"])
    avg_wait = (
        sum(metrics["wait_times"]) / total_aircraft if total_aircraft > 0 else 0
    )
    total_wait_hours = sum(metrics["wait_times"])
    total_labour = num_technicians * tech_cost * sim_time
    total_delay = total_wait_hours * delay_cost
    total_cost = total_labour + total_delay

    # Display High-Level Key Performance Indicators (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Aircraft Processed", f"{total_aircraft}")
    col2.metric("Average Queue Wait", f"{round(avg_wait, 2)} hrs")
    col3.metric("Total Delay Penalties", f"${total_delay:,.2f}")
    col4.metric("Total Operating Cost", f"${total_cost:,.2f}")

    # Plot Visual Analysis
    st.subheader("📊 Queueing & Operating Cost Dashboard")
    fig, ax1 = plt.subplots(figsize=(8, 4))
    sns.set_theme(style="whitegrid")
    costs = [total_labour, total_delay]
    labels = ["Labor Costs", "Delay Penalties"]
    colors = ["#2b5c8f", "#d9534f"]
    ax1.bar(labels, costs, color=colors, width=0.4)
    ax1.set_ylabel("Financial Cost ($)")
    ax1.set_title("Operational Cost Breakdown for Selected Staffing Level")
    st.pyplot(fig)


st.divider()
st.subheader("📊 Compare All Staffing Levels")
st.write(
    "Runs the simulation across a range of technician team sizes and "
    "reports the same cost breakdown as the project README."
)

if st.button("🔍 Run Full Comparison"):
    results = []

    for teams in range(2, 7):
        random.seed(42)  # same seed each run for a fair apples-to-apples comparison
        env = simpy.Environment()
        hangar = simpy.Resource(env, capacity=teams)
        metrics = {"wait_times": [], "service_times": []}

        env.process(
            aircraft_generator(
                env,
                hangar,
                metrics,
                arrival_interval,
                maintenance_time,
                delay_cost,
            )
        )
        env.run(until=sim_time)

        total_aircraft = len(metrics["wait_times"])
        avg_wait = (
            sum(metrics["wait_times"]) / total_aircraft if total_aircraft > 0 else 0
        )
        total_wait_hours = sum(metrics["wait_times"])
        total_labour = teams * tech_cost * sim_time
        total_delay = total_wait_hours * delay_cost
        total_cost = total_labour + total_delay

        results.append({
            "Technician Teams": teams,
            "Total Aircraft Processed": total_aircraft,
            "Avg Wait Time (Hrs)": round(avg_wait, 2),
            "Labour Cost ($)": total_labour,
            "Delay Cost ($)": round(total_delay, 2),
            "Total Operating Cost ($)": round(total_cost, 2),
        })

    df = pd.DataFrame(results)
    optimal_row = df.loc[df["Total Operating Cost ($)"].idxmin()]

    st.dataframe(
        df.style.format({
            "Labour Cost ($)": "${:,.2f}",
            "Delay Cost ($)": "${:,.2f}",
            "Total Operating Cost ($)": "${:,.2f}",
        }),
        use_container_width=True,
    )

    st.success(
        f"✅ Optimal staffing level: **{int(optimal_row['Technician Teams'])} teams** "
        f"at a total operating cost of **${optimal_row['Total Operating Cost ($)']:,.2f}**"
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.set_theme(style="whitegrid")
    ax2.plot(df["Technician Teams"], df["Total Operating Cost ($)"], marker="o", color="#2b5c8f")
    ax2.set_xlabel("Technician Teams")
    ax2.set_ylabel("Total Operating Cost ($)")
    ax2.set_title("Total Operating Cost vs. Staffing Level")
    st.pyplot(fig2)
