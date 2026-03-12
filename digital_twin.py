import pandapower as pp
import numpy as np
import joblib

class PowerGridDigitalTwin:

    def __init__(self):

        self.model = joblib.load("fault_model.pkl")
        self.net = self.create_grid()

    def create_grid(self):

        net = pp.create_empty_network()

        b1 = pp.create_bus(net, vn_kv=110)
        b2 = pp.create_bus(net, vn_kv=110)
        b3 = pp.create_bus(net, vn_kv=110)

        pp.create_ext_grid(net, bus=b1)

        pp.create_line_from_parameters(
            net,
            from_bus=b1,
            to_bus=b2,
            length_km=10,
            r_ohm_per_km=0.1,
            x_ohm_per_km=0.1,
            c_nf_per_km=0,
            max_i_ka=1
        )

        pp.create_line_from_parameters(
            net,
            from_bus=b2,
            to_bus=b3,
            length_km=8,
            r_ohm_per_km=0.1,
            x_ohm_per_km=0.1,
            c_nf_per_km=0,
            max_i_ka=1
        )

        pp.create_load(net, bus=b3, p_mw=50)

        return net


    def simulate(self):

        load = np.random.normal(80,15)
        voltage = np.random.normal(1.0,0.03)
        line_loading = np.random.normal(60,10)

        features = [[load,voltage,line_loading]]

        fault_prob = self.model.predict(features)[0]

        return {
            "load": load,
            "voltage": voltage,
            "line_loading": line_loading,
            "fault": fault_prob
        }