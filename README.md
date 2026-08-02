# ✈️ Aircraft Maintenance Operations & Capacity Optimization Model
## 📌 Executive Summary
In commercial aviation maintenance, understaffing leads to massive aircraft downtime penalties ($1,500/hr), while overstaffing creates idle labor inefficiencies. This project utilizes **Stochastic Discrete-Event Simulation (`SimPy`)** and **Financial Trade-Off Modeling** to analyze capacity bottlenecks and identify the optimal staffing model for an aircraft maintenance facility over 5,000 operational hours.
---
## 🔬 Engineering Problem & Key Findings
* **The Queueing Bottleneck:** At low staffing levels ($\le 3$ teams), incoming aircraft face severe queueing delays due to stochastic arrival spikes and variable service times.
* **The Cost Sweet Spot:** While adding technicians increases payroll, it exponentially reduces aircraft downtime penalties.
* **Optimal Recommendation:** Increasing staffing from **3 to 4 technician teams** reduces total operating costs by over **50%**, eliminating catastrophic queueing backlogs.
---
## 📊 Performance & Optimization Results
| Technician Teams | Total Aircraft Processed | Avg Wait Time (Hrs) | Labour Cost ($) | Delay Cost ($) | Total Operating Cost ($) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **2** | 1,981 | 142.30 | $500,000 | $14,094,750 | $14,594,750 |
| **3** | 1,996 | 18.45 | $750,000 | $1,841,250 | $2,591,250 |
| **4** | 2,002 | 2.10 | $1,000,000 | $210,200 | **$1,210,200 (Optimal)** |
| **5** | 2,001 | 0.35 | $1,250,000 | $35,000 | $1,285,000 |
| **6** | 2,002 | 0.05 | $1,500,000 | $5,000 | $1,505,000 |
---
## 🛠 Tech Stack & Tools
* **Simulation Framework:** Python 3.x, `SimPy` (Discrete-event simulation)
* **Data Processing & Analytics:** `Pandas`, `NumPy`
* **Data Visualization:** `Matplotlib`, `Seaborn`
---
## 🚀 How to Execute the Simulation
1. Clone the repository:
```bash
   git clone https://github.com/malathalassaf15-ctrl/Aircraft-Maintenance-Queue-Simulation.git
```
2. Navigate into the project folder:
```bash
   cd Aircraft-Maintenance-Queue-Simulation
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Run the simulation:
```bash
   python main.py
```
## 🖥 Interactive Dashboard
Launch the live Streamlit dashboard to explore staffing scenarios interactively:
```bash
streamlit run app.py
```
Adjust parameters in the sidebar, then use **Run Live Optimization Analysis** for a single staffing level, or **Run Full Comparison** to sweep 2–6 teams and find the cost-optimal staffing level automatically.
