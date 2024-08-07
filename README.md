# MagLev-2024-Coverage-Paradox-Notebook

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

***

## Purpose

This notebook was produced in support of a paper written for the [MagLev 2024 Conference](https://mkon.nu/maglev_2024) titled *"The Potential of Dynamic Skip-stop to Address the Coverage Paradox in Urban Transport through Superconducting MagLev Rail Technology"*

A key section of the paper is describing the Coverage Paradox, a phenomenon of urban rail transport systems due to the structure of the system concept. This is presented in a paper by Blumenfeld et. al. [1]. 

The purpose of this script is to illustrate the coverage paradox with an interactive notebook where users can change the parameters of a rail system and see how it has an impact on the door-to-door journey time showing the behaviour of the coverage paradox.

***

## Usage

The script is contained in the single marimo notebook file:
* `coverage_paradox_notebook.py`

### Running the notebook

To use, clone the repository (or just the file) to a local machine, open a terminal and naviagate to the saved directory.

To run the programme in app mode use the command:
`marimo run coverage_paradox_notebook.py`

To view and alter the underlying programme use the command:
`marimo edit coverage_paradox_notebook.py`

Both will open the marimo web interface.

### Using the notebook

With the notebook running, there are 3 sections:

**Variables**
The 7 parameters that the users can adjust.

**Optimum Door-to-door Journey Time**
The number of stations and interstation distance that result in the minimum average door-to-door journey time ($T_j$).

**Plots**
Altair plots for:
* Number of stations and duration of journey components
* Interstation distance and percentage of door-to-door journey time spent on vehicle

Pandas dataframe will full caculation results

***

## Methodology and Assumptions

The aim of this is to calculate the door-to-door journey time for a passenger travelling on an urban rail transport system.

The overall formula is:

$T_j = 2T_a + T_w + T_v$

Where:
* $T_j$ **Average door-to-door journey time**, the average total time to travel from origin to destination.
* $T_a$ **Access time**, the time spend walking to or from the transit vehicle.
* $T_w$ **Wait time**, the time elapsed between arriving at the transit vehicle and it departing on the journey.
* $T_v$ **Vehicle time**, the time spent travelling in the transit vehicle.

### Variable Input Parameters
The variable parameters are:
* $S_j$ **Door-to-door journey distance** ($km$), the total distance to be travelled 
* $tphpd$ **Trains per hour per direction**
* $V_{v-max}$ **Maximum Line Speed** ($m/s$), maximum speed of vehicle 
* $A_{v-acc}$ **Mean Acceleration** ($m/s^2$), the rate of acceleration of the vehicle from stationary to $V_{v-max}$ 
* $A_{v-dcc}$ **Mean Deceleration** ($m/s^2$), the rate of deceleration of the vehicle from $V_{v-max}$ to stationary 
* $T_{dwell}$ **Dwell Time** ($mins$), the time spent stationary dwelling at each station 
* $V_{walk}$ **Average walking speed** ($km/h$), average speed for passenger walking

### Calculations
The Variable Input Parameters are then taken and put into 3 classes which convert the input units to SI. The $tphpd$ is also converated into a headway ($T_{hw}$) between vehicles. The three classes and their attributes are:
* `Vehicle` (`line_speed`, `acceleration`, `deceleration`)
    * The time and distance taken to accelerate and decelerate to line speed are also calculated and recorded as attributes of the class (`acc_dcc_distance`, `acc_dcc_time`)
* `Operations` (`headway`, `dwell_time`)
* `Journey` (`journey_distance`, `walking_speed`)

The `Simulation` class runs all of the calculations, taking instances of the `Vehicle`, `Operations` and `Journey` classes. There is a minimum interstation distance, defined by the `acc_dcc_distance` from which can then be derived a maximum number of stations. The class then runs over the possible number of stations and stores the resulting journey time components in an instance of the `Individual_Simulation` class, the set of all of this are stored in a class attribute `simulation_results` list.

The calculations are then:

$S_{is} = \frac{S_j}{N_{stations}-0.5}$

$T_{is} = \frac{S_{is}-S_{acc-dcc}}{V_{v-max}} + T_{acc-dcc}$

$T_v = T_{is}(N_{stations}-1) + T_{dwell}(N_{stations}-2)$

$T_a = \frac{S_{is}/4}{V_{walk}}$

$T_{w} = \frac{T_{hw}}{2}$

Where:
* $N_{stations}$ **Number of stations**
* $S_{is}$ **interstation distance**, distance between each station
* $T_{is}$ **intersation time**, time taken for vehicle to travel between each station
* $S_{acc-dcc}$ **acceleration deceleration distance**, distance taken to accelerate and decelerate from $V_{v-max}$
* $T_{acc-dcc}$ **acceleration deceleration time**, time taken to accelerate and decelerate from $V_{v-max}$
* $T_{hw}$ **vehicle headway**

There is a function of the class `Simulation` that converts `simulation_results` from a list of instances of `Individual_Simulation` to a pandas dataframe.

There are also functions of the class `Simulation` that produce the altair charts used in the notebook

### Default Values
The National Travel Survey gave commuting figures for London of an average number of trips per year of 126 and the average distance travelled per year at 1,074 miles [2]. This gives an average commuting distance of 13.7km per commuting trip.

The average walking pace of 4.7km/h is taken from a meta-anaysis paper [3].

The other parameters are taken from a specification released by Siemens for a fleet of trains produced for the Munich metro [4].

### Assumptions
For this demonstration it is fundementally assumed that the journey exists in 1-dimensional space.

It is assumed that the population distribution is homogeneous and therefore the interstation distance is constant along the line. From this it is also derrived that the average distance for any user's origin and destination from a station is a quarter of the interstation distance.

There is no account taken of time taken to walk from the station enterance to the platform or impact of crowds at peak times. This would normally add some time and would include time to scan tickets and other station activities.

It is assumed that passengers arrive randomly and do not plan to arrive for a train at a specific time. Therefore on average they will have to wait half of the headway between two trains to board their next service.

It is assumed that the rate of acceleration and deceleration of trains is constant. A more standard method is the Davis equation but this was not chosen to be used in this case to keep the user interface simple.

It is assumed that vehicles travel with a constant headway between all services. Any fluctuations or delay is not included in this calculations.

It is also possible to set the dwell time greater than would be possible with the headway. This is a limitation and could be addressed in future revisions of the programme.

***

## Requirements

The script is tested working with `python 3.11.9` and the following packages:
* `marimo 0.7.0`
* `altair 5.3.0`
* `pandas 2.2.2`

***

## References

[1] Marcelo Blumenfeld, Clive Roberts, and Felix Schmid. “A systems approach to developing a new metro for megalopoleis”. en. In: *Proceedings of the Institution of Civil Engineers - Transport* 169.5 (Oct. 2016), pp. 249–261. ISSN: 0965-092X, 1751-7710. DOI: `10.1680/jtran.16.00018`.

[2] Department of Transport. *NTS9918: Average number of trips and distance travelled by trip purpose, ethnic group, region and rural-urban classification of residence*: England, 2002 onwards. Aug. 2023. URL: <https://assets.publishing.service.gov.uk/media/64e8b53d7af6dd001368efdf/nts9918.ods> (visited on 07/17/2024).

[3] Elaine M. Murtagh et al. “Outdoor Walking Speeds of Apparently Healthy Adults: A Systematic Review and Meta-analysis”. en. In: *Sports Medicine* 51.1 (Jan. 2021), pp. 125–141. ISSN: 0112-1642, 1179-2035. DOI: `10.1007/s40279-020-01351-3`.

[4] Siemens. *Siemens to supply new metro for Munich: Background Paper*. en. Sept. 2012. URL: <https://assets.new.siemens.com/siemens/assets/api/uuid:52c1eaca-f058-43ae-9943-7fc99f595de7/rl-metro-munich-e.pdf> (visited on 07/18/2024)

***

## Acknowledgements

This research has been funded by a PhD scholarship from the University of Birmingham.

Many thanks go to my supervisor Dr Marcelo Blumenfeld for their guidance, support and input on this project.

***

## License

MagLev-2024-Coverage-Paradox-Notebook
Copyright (C) 2024  Chris Davis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
