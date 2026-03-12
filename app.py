import streamlit as st
import pandas as pd
from digital_twin import PowerGridDigitalTwin

st.title("⚡ AI Digital Twin of Power Grid")

st.write("Simulating Grid Conditions with AI Fault Prediction")

grid = PowerGridDigitalTwin()

if st.button("Run Simulation"):

    result = grid.simulate()

    data = pd.DataFrame({
        "Metric":["Load (MW)","Voltage (p.u)","Line Loading (%)"],
        "Value":[result["load"],result["voltage"],result["line_loading"]]
    })

    st.table(data)

    if result["fault"] == 1:
        st.error("⚠️ AI Detected Potential Grid Fault")
    else:
        st.success("Grid Operating Normally")

st.subheader("Grid Monitoring Dashboard")

st.line_chart({
    "Load":[grid.simulate()["load"] for _ in range(20)],
})