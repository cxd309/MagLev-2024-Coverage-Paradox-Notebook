import marimo

__generated_with = "0.7.0"
app = marimo.App(width="medium")


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
def __(dwell_time_ui, tphpd_ui):
    ## Check if the dwell time is greater than would be possible with the tphpd
    warning_text = ""
    if (60/dwell_time_ui.value) < tphpd_ui.value:
        warning_text = f"""<span style="color:red">WARNING! The Trains Per Hour Per Direction is greater than possible with the Dwell Time per Station</span>"""
    return warning_text,


@app.cell
def __(mo, warning_text):
    mo.md(warning_text)
    return


@app.cell
def __(mo):
    mo.accordion({
        "**Variable Input Parameters**": """    
    * $S_j$ **Door-to-door journey distance** ($km$), the total distance to be travelled 
    * $tphpd$ **Trains per hour per direction**
    * $V_{v-max}$ **Maximum Line Speed** ($m/s$), maximum speed of vehicle 
    * $A_{v-acc}$ **Mean Acceleration** ($m/s^2$), the rate of acceleration of the vehicle from stationary to $V_{v-max}$ 
    * $A_{v-dcc}$ **Mean Deceleration** ($m/s^2$), the rate of deceleration of the vehicle from $V_{v-max}$ to stationary 
    * $T_{dwell}$ **Dwell Time** ($mins$), the time spent stationary dwelling at each station 
    * $V_{walk}$ **Average walking speed** ($km/h$), average speed for passenger walking
        """,

        "**Source of Default Values**":"""
    The National Travel Survey gave commuting figures for London of an average number of trips per year of 126 and the average distance travelled per year at 1,074 miles [1]. This gives an average commuting distance of 13.7km per commuting trip.

    The average walking pace of 4.7km/h is taken from a meta-anaysis paper [2].

    The other parameters are taken from a specification released by Siemens for a fleet of trains produced for the Munich metro [3].

    [1] Department of Transport. *NTS9918: Average number of trips and distance travelled by trip purpose, ethnic group, region and rural-urban classification of residence*: England, 2002 onwards. Aug. 2023. URL: <https://assets.publishing.service.gov.uk/media/64e8b53d7af6dd001368efdf/nts9918.ods> (visited on 07/17/2024).

    [2] Elaine M. Murtagh et al. “Outdoor Walking Speeds of Apparently Healthy Adults: A Systematic Review and Meta-analysis”. en. In: *Sports Medicine* 51.1 (Jan. 2021), pp. 125–141. ISSN: 0112-1642, 1179-2035. DOI: `10.1007/s40279-020-01351-3`.

    [3] Siemens. *Siemens to supply new metro for Munich: Background Paper*. en. Sept. 2012. URL: <https://assets.new.siemens.com/siemens/assets/api/uuid:52c1eaca-f058-43ae-9943-7fc99f595de7/rl-metro-munich-e.pdf> (visited on 07/18/2024)
        """,

    "**Explanation of Calculations**": """    
    The Variable Input Parameters are then taken and put into 3 classes which convert the input units to SI. The $tphpd$ is also converated into a headway ($T_{hw}$) between vehicles. The three classes and their attributes are:

    * `Vehicle` (`line_speed`, `acceleration`, `deceleration`)
        * The time and distance taken to accelerate and decelerate to line speed are also calculated and recorded as attributes of the class (`acc_dcc_distance`, `acc_dcc_time`)
    * `Operations` (`headway`, `dwell_time`)
    * `Journey` (`journey_distance`, `walking_speed`)

    The `Simulation` class runs all of the calculations, taking instances of the `Vehicle`, `Operations` and `Journey` classes. There is a minimum interstation distance, defined by the `acc_dcc_distance` from which can then be derived a maximum number of stations. The class then runs over the possible number of stations and stores the resulting journey time components in an instance of the `Individual_Simulation` class, the set of all of this are stored in a class attribute `simulation_results` list.

    The calculations are then:

    $S_{is} = \\frac{S_j}{N_{stations}-0.5}$

    $T_{is} = \\frac{S_{is}-S_{acc-dcc}}{V_{v-max}} + T_{acc-dcc}$

    $T_v = T_{is}(N_{stations}-1) + T_{dwell}(N_{stations}-2)$

    $T_a = \\frac{S_{is}/4}{V_{walk}}$

    $T_{w} = \\frac{T_{hw}}{2}$

    Where:

    * $N_{stations}$ **Number of stations**
    * $S_{is}$ **interstation distance**, distance between each station
    * $T_{is}$ **intersation time**, time taken for vehicle to travel between each station
    * $S_{acc-dcc}$ **acceleration deceleration distance**, distance taken to accelerate and decelerate from $V_{v-max}$
    * $T_{acc-dcc}$ **acceleration deceleration time**, time taken to accelerate and decelerate from $V_{v-max}$
    * $T_{hw}$ **vehicle headway**

    There is a function of the class `Simulation` that converts `simulation_results` from a list of instances of `Individual_Simulation` to a pandas dataframe.

    There are also functions of the class `Simulation` that produce the altair charts used in the notebook
        """,

        "**Assumptions**":"""
    For this demonstration it is fundementally assumed that the journey exists in 1-dimensional space.

    It is assumed that the population distribution is homogeneous and therefore the interstation distance is constant along the line. From this it is also derrived that the average distance for any user's origin and destination from a station is a quarter of the interstation distance.

    There is no account taken of time taken to walk from the station enterance to the platform or impact of crowds at peak times. This would normally add some time and would include time to scan tickets and other station activities.

    It is assumed that passengers arrive randomly and do not plan to arrive for a train at a specific time. Therefore on average they will have to wait half of the headway between two trains to board their next service.

    It is assumed that the rate of acceleration and deceleration of trains is constant. A more standard method is the Davis equation but this was not chosen to be used in this case to keep the user interface simple.

    It is assumed that vehicles travel with a constant headway between all services. Any fluctuations or delay is not included in this calculations.

    It is also possible to set the dwell time greater than would be possible with the headway. This is a limitation and could be addressed in future revisions of the programme.
        """
    })
    return


@app.cell
def __(mo, seconds_to_minutes, sim):
    optimum_result = sim.Find_Optimum_Result()

    mo.md(f"""
        ## Optimum Door-to-door Journey Time \n
        The number of stations and interstation distance that result in the minimum average door-to-door journey time ($T_j$). \n
        **Number of Stations**: {optimum_result.n_stations:0.0f} \n
        **Journey Time**: {seconds_to_minutes(optimum_result.journey_time):0.1f} minutes \n
        **Interstation Distance**: {optimum_result.is_distance/1000:0.2f}km
    """)
    return optimum_result,


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
    tphpd_ui = mo.ui.number(
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
        tphpd_ui, 
        vehicle_line_speed_ui, 
        vehicle_acceleration_ui, 
        vehicle_deceleration_ui, 
        dwell_time_ui,
        walking_speed_ui
    ]
    return (
        dwell_time_ui,
        journey_distance_ui,
        tphpd_ui,
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
    tphpd_ui,
    vehicle_acceleration_ui,
    vehicle_deceleration_ui,
    vehicle_line_speed_ui,
    walking_speed_ui,
):
    veh = Vehicle(vehicle_line_speed_ui, vehicle_acceleration_ui, vehicle_deceleration_ui)
    ops = Operations(tphpd_ui, dwell_time_ui)
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
        def __init__(self, tphpd_ui, dwell_time_ui):
            # Vehicle Headway (s) -- convert from trains per hour per direction
            self.headway = 3600 / tphpd_ui.value
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
