import marimo

__generated_with = "0.7.0"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(
        r"""
        # MagLev 2024 - Coverage Paradox

        The purpose of this script is to illustrate the coverage paradox with an interactive notebook where users can change the parameters of a rail system and see how it has an impact on the door-to-door journey time showing the behaviour of the coverage paradox.

        For further details see `README.md`
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## Variables")
    return


@app.cell
def __(mo):
    journey_distance_ui = mo.ui.number(
        start=2, 
        stop=100,
        step= 0.1,
        value = 13.7,
        label="Total Journey Distance ($km$)"
    )
    tphph_ui = mo.ui.number(
        start=1, 
        stop=40,
        step=1,
        value = 30,
        label="Trains Per Hour Per Direction"#
    )
    vehicle_line_speed_ui = mo.ui.number(
        start=10, 
        stop=200,
        step= 1,
        value = 90,
        label="Maximum Line Speed ($km/h$)"
    )
    vehicle_acceleration_ui = mo.ui.number(
        start=0.1, 
        stop=2.0,
        step=0.1,
        value = 1.3,
        label="Mean Acceleration ($m/s^2$)"
    )
    vehicle_deceleration_ui = mo.ui.number(
        start=0.1, 
        stop=2.0, 
        step=0.1,
        value=1.2,
        label="Mean Deceleration($m/s^2$)"
    )
    dwell_time_ui = mo.ui.number(
        start=0.2, 
        stop=10.0, 
        step=0.1,
        value=1.5,
        label="Dwell Time per Station ($mins$)"
    )
    walking_speed_ui = mo.ui.number(
        start=1, 
        stop=7, 
        step=0.1,
        value=4.7,
        label="Average Walking Pace ($km/h$)"
    )

    [
        journey_distance_ui, 
        tphph_ui, 
        vehicle_line_speed_ui, 
        vehicle_acceleration_ui, 
        vehicle_deceleration_ui, 
        dwell_time_ui,
        walking_speed_ui
    ]
    return (
        dwell_time_ui,
        journey_distance_ui,
        tphph_ui,
        vehicle_acceleration_ui,
        vehicle_deceleration_ui,
        vehicle_line_speed_ui,
        walking_speed_ui,
    )


@app.cell
def __(mo, seconds_to_minutes, sim):
    optimum_result = sim.Find_Optimum_Result()

    mo.md(f"""
        ## Optimum Result \n
        The number of stations / interstation distance with the minimum Door-to-Door journey time \n
        **Number of Stations**: {optimum_result.n_stations:0.0f} \n
        **Journey Time**: {seconds_to_minutes(optimum_result.journey_time):0.1f} minutes \n
        **Interstation Distance**: {optimum_result.is_distance:0.1f}m
    """)
    return optimum_result,


@app.cell
def __(mo):
    mo.md(r"## Plots")
    return


@app.cell
def __(
    Journey,
    Operations,
    Simulation,
    Vehicle,
    dwell_time_ui,
    journey_distance_ui,
    tphph_ui,
    vehicle_acceleration_ui,
    vehicle_deceleration_ui,
    vehicle_line_speed_ui,
    walking_speed_ui,
):
    veh = Vehicle(vehicle_line_speed_ui, vehicle_acceleration_ui, vehicle_deceleration_ui)
    ops = Operations(tphph_ui, dwell_time_ui)
    jny = Journey(journey_distance_ui, walking_speed_ui)
    sim = Simulation(veh, ops, jny)
    return jny, ops, sim, veh


@app.cell
def __(sim):
    sim.N_Stations_Journey_Time_Chart()
    return


@app.cell
def __(sim):
    sim.IS_Distance_Perc_Veh_Time_Chart()
    return


@app.cell
def __(sim):
    sim.to_df()
    return


@app.cell
def __():
    class Vehicle:
        def __init__(self, line_speed_ui, acceleration_ui, deceleration_ui):
            # Vehicle Linespeed (m/s) -- convert from km/h
            self.line_speed = line_speed_ui.value * (1000/3600)
            # Vehicle Acceleration (m/s^2)
            self.acceleration = acceleration_ui.value
            # Vehicle Deceleration (m/s^2)
            self.deceleration = deceleration_ui.value

            self.acceleration_distance = (self.line_speed ** 2)/(2*self.acceleration)
            self.deceleration_distance = (self.line_speed ** 2)/(2*self.deceleration)
            self.acceleration_time = self.line_speed / self.acceleration
            self.deceleration_time = self.line_speed / self.deceleration

            self.acc_dcc_distance = self.acceleration_distance + self.deceleration_distance
            self.acc_dcc_time = self.acceleration_time + self.deceleration_time
    return Vehicle,


@app.cell
def __():
    class Operations:
        def __init__(self, tphph_ui, dwell_time_ui):
            # Vehicle Headway (s) -- convert from trains per hour per direction
            self.headway = 3600 / tphph_ui.value
            # Dwell Time (s) -- convert from minutes
            self.dwell_time = dwell_time_ui.value * 60
    return Operations,


@app.cell
def __():
    class Journey:
        def __init__(self, journey_distance_ui, walking_speed_ui):
            # Journey Distance (m) -- convert from km
            self.journey_distance = journey_distance_ui.value * 1000
            # Walking Speed (m/s) -- convert from km/h
            self.walking_speed = walking_speed_ui.value * (1000/3600)
    return Journey,


@app.cell
def __():
    class Individual_Simulation:
        def __init__(self, n_stations, is_distance, vehicle_time, access_time, waiting_time):
            self.n_stations = n_stations
            self.is_distance = is_distance
            self.vehicle_time = vehicle_time
            self.access_time = access_time
            self.waiting_time = waiting_time

            self.journey_time = vehicle_time + 2*access_time + waiting_time

            self.perc_time_in_vehicle = 100 * vehicle_time / self.journey_time

        def to_dict(self):
            return {
                "Number of Stations": self.n_stations,
                "Interstation Distance (m)": self.is_distance,
                "Vehicle Time (s)": self.vehicle_time,
                "Access Time (s)": self.access_time,
                "Waiting Time (s)": self.waiting_time,
                "Door-to-Door Journey Time (s)": self.journey_time,
                "Percentage Time In Vehicle": self.perc_time_in_vehicle
            }
    return Individual_Simulation,


@app.cell
def __():
    def seconds_to_minutes(time_seconds):
        return time_seconds / 60
    return seconds_to_minutes,


@app.cell
def __(Individual_Simulation, alt, math, mo, pd, seconds_to_minutes):
    class Simulation:
        def __init__(self, veh, ops, jny):
            self.jny = jny
            self.veh = veh
            self.ops = ops

            self.simulation_results = []

            self.Run_Simulation()

        def to_df(self):
            temp_array = []
            for ind_sim in self.simulation_results:
                temp_array.append(ind_sim.to_dict())

            return pd.DataFrame.from_dict(temp_array) 

        def Run_Individual_Simulation(self, n_stations):
            # Distance between stations
            is_distance = self.jny.journey_distance/n_stations-0.5

            # Time travelling at line speed
            line_speed_time = (is_distance-self.veh.acc_dcc_distance)/self.veh.line_speed

            # Time travelling between stations
            is_time = self.veh.acc_dcc_time + line_speed_time

            # Total time in vehicle
            vehicle_time = is_time*(n_stations-1) + self.ops.dwell_time*(n_stations-2)

            # Access Distance (walking) at each end
            access_distance = is_distance / 4
            # Access time
            access_time = access_distance / self.jny.walking_speed

            # Waiting Time to board vehicle
            waiting_time = self.ops.headway / 2

            ind_result = Individual_Simulation(n_stations, is_distance, vehicle_time, access_time, waiting_time)

            self.simulation_results.append(ind_result)

        def Run_Simulation(self):
            # Find the limit for the number of stations
            # reached when the vehicle cannot accelerate and declerate in the interstation distance
            max_stations = math.ceil((self.jny.journey_distance/(self.veh.acc_dcc_distance)) + 0.5)

            for n_stations in range(2, max_stations):
                self.Run_Individual_Simulation(n_stations)

        def Find_Optimum_Result(self):
            optimum_result = self.simulation_results[0]

            for ind_sim in self.simulation_results:
                if ind_sim.journey_time<=optimum_result.journey_time:
                    optimum_result = ind_sim

            return optimum_result

        def N_Stations_Journey_Time_Chart(self):
            # Get a wide DF
            wide_df = self.to_df()[["Number of Stations", "Vehicle Time (s)", "Access Time (s)", "Door-to-Door Journey Time (s)", "Waiting Time (s)"]]


            # melt to long form for altair
            long_df = wide_df.melt("Number of Stations", var_name="Time Measure", value_name="Time (mins)")
            long_df["Time (mins)"] = long_df["Time (mins)"].apply(seconds_to_minutes)

            chart = mo.ui.altair_chart(
                alt.Chart(long_df).mark_line().encode(
                    x="Number of Stations",
                    y="Time (mins)",
                    color="Time Measure"
                ).properties(title="Number of stations and duration of journey components")
            )
            return chart

        def IS_Distance_Perc_Veh_Time_Chart(self):
            ## Plot for interstation distance and percentage of time in vehicle

            chart = mo.ui.altair_chart(
                alt.Chart(self.to_df()).mark_line().encode(
                    x="Interstation Distance (m)",
                    y="Percentage Time In Vehicle"
                ).properties(title="Interstation distance and percentage of door-to-door journey time spent in vehicle")
            )

            return chart
    return Simulation,


@app.cell
def __():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import math
    return alt, math, mo, pd


if __name__ == "__main__":
    app.run()
