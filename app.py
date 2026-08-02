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
        total_labour =
