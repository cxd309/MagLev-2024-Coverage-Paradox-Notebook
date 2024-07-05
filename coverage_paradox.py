import marimo

__generated_with = "0.7.0"
app = marimo.App()


@app.cell
def __(mo):
    mo.md(r"# MagLev 2024 - Coverage Paradox")
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
        step= 1,
        value = 21,
        label="Total Journey Distance ($km$)"
    )
    tphph_ui = mo.ui.number(
        start=1, 
        stop=30,
        step=1,
        value = 6,
        label="Trains Per Hour Per Direction"#
    )
    vehicle_line_speed_ui = mo.ui.number(
        start=10, 
        stop=150,
        step= 5,
        value = 80,
        label="Maximum Line Speed ($km/h$)"
    )
    vehicle_acceleration_ui = mo.ui.number(
        start=0.1, 
        stop=1.0,
        step=0.1,
        value = 1,
        label="Acceleration ($m/s^2$)"
    )
    vehicle_deceleration_ui = mo.ui.number(
        start=0.1, 
        stop=1.0, 
        step=0.1,
        value=0.7,
        label="Deceleration($m/s^2$)"
    )
    dwell_time_ui = mo.ui.number(
        start=0.5, 
        stop=10.0, 
        step=0.5,
        value=3,
        label="Dwell Time per Station ($mins$)"
    )
    walking_speed_ui = mo.ui.number(
        start=3, 
        stop=6, 
        step=0.5,
        value=5,
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
def __(Run_Tot_Simulation, sim):
    sim_results = Run_Tot_Simulation(sim)
    return sim_results,


@app.cell
def __(alt, mo, sim_results):
    ## Plot for number of stations and timing
    # reduce the df to a select number of columns (wide format)
    n_stations_timing_wide_df = sim_results[["Number of Stations", "Vehicle Time (s)", "Access Time (s)", "Door-to-Door Journey Time (s)"]]

    # melt to long form for altair
    n_stations_timing_long_df = n_stations_timing_wide_df.melt("Number of Stations", var_name="Time Measure", value_name="Time (s)")

    n_stations_timing_chart = mo.ui.altair_chart(alt.Chart(n_stations_timing_long_df).mark_line().encode(x="Number of Stations",y="Time (s)",color="Time Measure"))
    return (
        n_stations_timing_chart,
        n_stations_timing_long_df,
        n_stations_timing_wide_df,
    )


@app.cell
def __(n_stations_timing_chart):
    n_stations_timing_chart
    return


@app.cell
def __(alt, mo, sim_results):
    ## Plot for interstation distance and percentage of time in vehicle

    is_distance_vehicle_percentage_chart = mo.ui.altair_chart(alt.Chart(sim_results).mark_line().encode(x="Interstation Distance (m)",y="Percentage Time In Vehicle"))
    return is_distance_vehicle_percentage_chart,


@app.cell
def __(is_distance_vehicle_percentage_chart):
    is_distance_vehicle_percentage_chart
    return


@app.cell
def __(sim_results):
    sim_results
    return


@app.cell
def __(math):
    ## Classes

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

    class Operations:
        def __init__(self, tphph_ui, dwell_time_ui):
            # Vehicle Headway (s) -- convert from trains per hour per direction
            self.headway = 3600 / tphph_ui.value
            # Dwell Time (s) -- convert from minutes
            self.dwell_time = dwell_time_ui.value * 60

    class Journey:
        def __init__(self, journey_distance_ui, walking_speed_ui):
            # Journey Distance (m) -- convert from km
            self.journey_distance = journey_distance_ui.value * 1000
            # Walking Speed (m/s) -- convert from km/h
            self.walking_speed = walking_speed_ui.value * (1000/3600)

    class Simulation:
        def __init__(self, veh, ops, jny):
            self.jny = jny
            self.veh = veh
            self.ops = ops

            # Find the limit for the number of stations
            # reached when the vehicle cannot accelerate and declerate in the interstation distance
            self.max_stations = math.ceil((self.jny.journey_distance/(self.veh.acc_dcc_distance)) + 0.5)
    return Journey, Operations, Simulation, Vehicle


@app.cell
def __(jny, ops, pd):
    ## Simulation Functions

    def Run_Tot_Simulation(sim):
        total_results = []
        for n_stations in range(2, sim.max_stations):
            total_results.append(Run_Ind_Simulation(sim, n_stations))

        return pd.DataFrame.from_dict(total_results) 

    def Run_Ind_Simulation(sim, n_stations):
        # Distance between stations
        is_distance = sim.jny.journey_distance/(n_stations-0.5)
        # Time travelling at line speed
        line_speed_time = (is_distance-sim.veh.acc_dcc_distance)/sim.veh.line_speed
        # Time travelling between stations
        is_time = sim.veh.acc_dcc_time + line_speed_time

        # Total time in vehicle
        vehicle_time = is_time*(n_stations-1) + sim.ops.dwell_time*(n_stations-2)

        # Access Distance (walking) at each end
        access_distance = is_distance / 4
        # total access time (both ends)
        access_time = 2*(access_distance / jny.walking_speed)

        # Door to door journey time
        journey_time = vehicle_time + access_time + ops.headway/2

        return {
            "Number of Stations": n_stations,
            "Interstation Distance (m)": is_distance,
            "Vehicle Time (s)": vehicle_time,
            "Access Time (s)": access_time,
            "Door-to-Door Journey Time (s)": journey_time,
            "Percentage Time In Vehicle": 100 * vehicle_time / journey_time
        }
    return Run_Ind_Simulation, Run_Tot_Simulation


@app.cell
def __():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import math
    return alt, math, mo, pd


if __name__ == "__main__":
    app.run()
