# Copyright (c) 2023, Darrell Taylor

# This file is under the Apache License,
# Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and Limitations
# under the License.

import json
import ast
from flask import Flask, request, send_file
from types import SimpleNamespace

app = Flask(__name__)
import sys, os
import pandas as pd
import numpy as np
import hashlib
from datetime import datetime, timedelta
import json
# from IPython.display import display
import urllib.request
import os

# import additional module for SAM simulation:
# import site
# Use site.addsitedir() to set the path to the SAM SDK API. Set path to the python directory.
# site.addsitedir('/Applications/sam-sdk-2015-6-30-r3/languages/python/')
from matplotlib import pyplot as plt
from matplotlib import dates as mdates

plt.style.use("ggplot")

import PySAM.PySSC as pssc
import pvLibTest
import pprint


# Download PySAM here: https://pypi.org/project/NREL-PySAM/
# You must request an NSRDB api key from the link above
api_key = os.getenv("NRDSBAPIKEY", "UF7n")
# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
# attributes = "ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle"
# Set leap year to true or false. True will return leap day data if present, false will not.
# leap_year = "false"
# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
interval = 30
# Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
# NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
# local time zone.
utc = "false"
# Your full name, use '+' instead of spaces.
your_name = "Darrell+Taylor"
# Your reason for using the NSRDB.
reason_for_use = "PV_hot_water_sim_at_pvh2o_dot_com"
# Your email address
email = "darrell@pvh2o.com"

folder = "/tmp"


module_params = {
    "Name": "SunSpark Technology Inc. SST-M156(HCBF)-600W",
    "Manufacturer": "SunSpark Technology Inc.",
    "Technology": "Mono-c-Si",
    "Bifacial": 1,
    "STC": 601.437,
    "PTC": 562.8,
    "A_c": 2.77,
    "N_s": 78,
    "I_sc_ref": 13.86,
    "V_oc_ref": 55.1,
    "I_mp_ref": 12.99,
    "V_mp_ref": 46.3,
    "alpha_sc": 0.0066528,
    "beta_oc": -0.141607,
    "T_NOCT": 44.6,
    "a_ref": 2.048,
    "I_L_ref": 13.8753,
    "I_o_ref": 2.80156e-11,
    "R_s": 0.184367,
    "R_sh_ref": 166.971,
    "Adjust": 11.8772,
    "gamma_r": -0.338,
    "BIPV": "N",
    "Version": "2023.10.31",
    "Date": 44881
}

def downloadTMYWeatherData(lat=40.57, lon=-105.07, year=2022, folder="/tmp"):
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # "weather_data_source":"NSRDB PSM V3 GOES tmy-2022 3.2.0"

    # Declare url string, docs at 
    # https://developer.nrel.gov/docs/solar/nsrdb/psm3-2-2-tmy-download/

    # TMY seems to only have 60 min intervals

    weather_dataset_name = f"tmy-{year}" 
    url = f"https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-tmy-download.csv?wkt=POINT({lon:.2f}+{lat:.2f})&names={weather_dataset_name}&utc={utc}&email={email}&reason={reason_for_use}&api_key={api_key}"


    hash = hashlib.shake_128(url.encode()).hexdigest(8)
    filename = os.path.join(folder, "weather_"+hash + ".csv")
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

    return filename, hash


def downloadWeatherData(lat=40.57, lon=-105.07, year=2022, folder="/tmp"):
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # "weather_data_source":"NSRDB PSM V3 GOES tmy-2022 3.2.0"

    # Declare url string, docs at 
    # https://developer.nrel.gov/docs/solar/nsrdb/psm3-2-2-download/


    url = f"https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-2-2-download.csv?wkt=POINT({lon:.2f}+{lat:.2f})&names={year}&utc={utc}&email={email}&reason={reason_for_use}&api_key={api_key}&interval={interval}"

    # print(url)

    hash = hashlib.shake_128(url.encode()).hexdigest(8)
    filename = os.path.join(folder, "weather_"+hash + ".csv")
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

    return filename, hash



def runMonthlySimJson(
    lat=40.57,
    lon=-105.07,
    year=2022,
    power_kW=1,
    tilt=40,
    azimuth=180,
    module_type=0,
    losses=14,
    folder="/tmp",
):

    # this will run PvWatts V8 on nrel's api
    # https://developer.nrel.gov/docs/solar/pvwatts/v8/

    url = f"https://developer.nrel.gov/api/pvwatts/v8.json?api_key={api_key}&azimuth={azimuth}&system_capacity={power_kW:.2f}&losses={losses}&array_type=1&module_type={module_type}&gcr=0.4&dc_ac_ratio=1.2&inv_eff=96.0&radius=0&dataset=nsrdb&tilt={tilt}&lat={lat:.2f}&lon={lon:.2f}&year={year}"

    # print(url)
    hash = hashlib.shake_128(url.encode()).hexdigest(8)
    filename_api_json = os.path.join(folder, "monthly_api_" + hash + ".json")
    filename_monthly = os.path.join(folder, "monthly_" + hash + ".json")

    if not os.path.exists(filename_monthly):
        # urllib.request.urlretrieve(url, filename_api_json)

        df, filename, filename_monthly = runSim(
            lat, lon, year, power_kW, tilt, azimuth, module_type, losses, folder
        )
        

    return filename_monthly, hash


def runSim(
    lat=40.57,
    lon=-105.07,
    year=2022,
    power_kW=1,
    tilt=40,
    azimuth=180,
    module_type=0,
    losses=14,
    folder="/tmp",
):

    filename, hash = downloadWeatherData(lat=lat, lon=lon, year=year, folder=folder)

    extraVars = "hash={hash}&azimuth={azimuth}&system_capacity={power_kW}&losses={losses}&array_type=1&module_type={module_type}&gcr=0.4&dc_ac_ratio=1.2&inv_eff=96.0&radius=0&dataset=nsrdb&tilt={tilt}&lat={lat}&lon={lon}"

    hash = hashlib.shake_128(extraVars.encode()).hexdigest(8)


    # load the data
    # Return just the first 2 lines to get metadata:
    info = pd.read_csv(filename, nrows=1)
    # See metadata for specified properties, e.g., timezone and elevation
    timezone, elevation = info["Local Time Zone"], info["Elevation"]

    # Return all but first 2 lines of csv to get data:
    df = pd.read_csv(filename, skiprows=2)

    # Set the time index in the pandas dataframe:
    df = df.set_index(
        pd.date_range(
            "1/1/{yr}".format(yr=year),
            freq=f"{interval}Min",
            periods=525600 / int(interval),
        )
    )

    # now run the solar simulator
    ssc = pssc.PySSC()
    # Resource inputs for SAM model:
    # Must be byte strings
    wfd = ssc.data_create()
    ssc.data_set_number(wfd, b"lat", lat)
    ssc.data_set_number(wfd, b"lon", lon)
    ssc.data_set_number(wfd, b"tz", timezone)
    ssc.data_set_number(wfd, b"elev", elevation)
    ssc.data_set_array(wfd, b"year", df.index.year)
    ssc.data_set_array(wfd, b"month", df.index.month)
    ssc.data_set_array(wfd, b"day", df.index.day)
    ssc.data_set_array(wfd, b"hour", df.index.hour)
    ssc.data_set_array(wfd, b"minute", df.index.minute)
    ssc.data_set_array(wfd, b"dn", df["DNI"])
    ssc.data_set_array(wfd, b"df", df["DHI"])
    ssc.data_set_array(wfd, b"wspd", df["Wind Speed"])
    ssc.data_set_array(wfd, b"tdry", df["Temperature"])

    # Create SAM compliant object
    dat = ssc.data_create()
    ssc.data_set_table(dat, b"solar_resource_data", wfd)
    ssc.data_free(wfd)

    # Specify the system Configuration
    # Set system capacity in kW
    system_capacity = power_kW
    ssc.data_set_number(dat, b"system_capacity", system_capacity)
    # Set DC/AC ratio (or power ratio). See https://sam.nrel.gov/sites/default/files/content/virtual_conf_july_2013/07-sam-virtual-conference-2013-woodcock.pdf
    ssc.data_set_number(dat, b"dc_ac_ratio", 1.0)
    # Set tilt of system in degrees
    ssc.data_set_number(dat, b"tilt", tilt)
    # Set azimuth angle (in degrees) from north (0 degrees)
    ssc.data_set_number(dat, b"azimuth", azimuth)
    # Set the inverter efficency
    ssc.data_set_number(dat, b"inv_eff", 96)
    # Set the system losses, in percent
    ssc.data_set_number(dat, b"losses", losses)

    ssc.data_set_number(dat, b"module_type", module_type)
    # Specify fixed tilt system (0=Fixed, 1=Fixed Roof, 2=1 Axis Tracker, 3=Backtracted, 4=2 Axis Tracker)
    ssc.data_set_number(dat, b"array_type", 1)
    # Set ground coverage ratio
    ssc.data_set_number(dat, b"gcr", 0.4)
    # Set constant loss adjustment
    ssc.data_set_number(dat, b"adjust:constant", 0)

    # execute and put generation results back into dataframe
    mod = ssc.module_create(b"pvwattsv8")
    ssc.module_exec(mod, dat)
    df["generation"] = np.array(ssc.data_get_array(dat, b"gen"))
    df["tcell"] = np.array(ssc.data_get_array(dat, b"tcell"))
    df["tpoa"] = np.array(ssc.data_get_array(dat, b"tpoa"))
    df["poa"] = np.array(ssc.data_get_array(dat, b"poa"))

    monthly = {
            "ac_monthly": ssc.data_get_array(dat, b"ac_monthly"),
            "poa_monthly": ssc.data_get_array(dat, b"poa_monthly"),
            "solrad_monthly": ssc.data_get_array(dat, b"solrad_monthly"),
            "dc_monthly": ssc.data_get_array(dat, b"dc_monthly"),
        }

    #simData = pvLibTest.ssc_table_to_dict(mod, dat)
    # pprint.pp(simData.keys())
    #dict_keys(['gen', 'annual_energy_distribution_time', 'solar_resource_data', 'albedo_default', 'albedo_default_snow', 'use_wf_albedo', 'system_use_lifetime_output', 'system_capacity', 'module_type', 'dc_ac_ratio', 'bifaciality', 'array_type', 'tilt', 'azimuth', 'gcr', 'rotlim', 'losses', 'enable_wind_stow', 'stow_wspd', 'wind_stow_angle', 'en_snowloss', 'inv_eff', 'xfmr_nll', 'xfmr_ll', 'shading_en_string_option', 'shading_string_option', 'shading_en_timestep', 'shading_en_mxh', 'shading_en_azal', 'shading_en_diff', 'batt_simple_enable', 'gh', 'dn', 'df', 'tamb', 'wspd', 'snow', 'alb', 'soiling_f', 'sunup', 'shad_beam_factor', 'ss_beam_factor', 'ss_sky_diffuse_factor', 'ss_gnd_diffuse_factor', 'aoi', 'poa', 'tpoa', 'tcell', 'dcsnowderate', 'dc', 'ac', 'ac_pre_adjust', 'inv_eff_output', 'poa_monthly', 'solrad_monthly', 'dc_monthly', 'ac_monthly', 'monthly_energy', 'solrad_annual', 'ac_annual', 'ac_annual_pre_adjust', 'annual_energy', 'capacity_factor', 'capacity_factor_ac', 'kwh_per_kw', 'location', 'city', 'state', 'lat', 'lon', 'tz', 'elev', 'inverter_efficiency', 'ts_shift_hours', 'percent_complete', 'adjust_constant', 'adjust_en_timeindex', 'adjust_en_periods'])


    # free the memory
    ssc.data_free(dat)
    ssc.module_free(mod)

    # Divide sum of generation by the number of periods times the system size
    cap_factor = df["generation"].sum() / (525600 / int(interval) * system_capacity)

    print(f"cap_factor = {cap_factor}")

    total_energy = df["generation"].sum()

    print(f"total_energy = {total_energy}")

    filename_sim = os.path.join(folder, "daily_" + hash + ".csv")
    df.to_csv(filename_sim)
    filename_json = os.path.join(folder, "monthly_" + hash + ".json")

    jOut = {"outputs":monthly}
    with open(filename_json, 'w') as fp:
        json.dump( jOut, fp)



    return df, filename_sim, filename_json


def convert_day_of_year(day_of_year, year=2022):
    # Create a date object for the first day of the year
    start_date = datetime(year, 1, 1)

    # Calculate the actual date by adding the number of days (minus one)
    actual_date = start_date + timedelta(days=day_of_year - 1)

    # Format the date to "Month, Day"
    return actual_date.strftime("%B %d")

    # returns standby loss in watts


def standbyLoss(ef=0.9, Ttank=40, Tamb=16):
    # formula 4 from in Water_Heater_Energy_Storage_wStaffResponse.pdf
    ua = 8.445 / ef - 8.617
    # add 22% for pipe losses per SS84_Panel5_Paper_06.pdf
    # append conversion from C to F
    return 1.22 * ua * ((Ttank - Tamb) * (9.0 / 5.0))


# water heater search:  https://www.ahridirectory.org/NewSearch?programId=24&searchTypeId=3
# https://www.centerpointenergy.com/en-us/SaveEnergyandMoney/Pages/CNP_Calculators/Thermal-Efficiency-Calculator.aspx?sa=MN&au=res
# 98%, 100BTU/hr = 0.93 EF  = 29.3 w
# 98%, 200BTU/hr = 0.88 EF  = 58.61 w
# Tank temp = 58.61, amb temp = 19.4 = delta is 40 C
#  https://www.energytrust.org/wp-content/uploads/2017/11/Water_Heater_Energy_Storage_wStaffResponse.pdf
#
#
def nsrdb_plot(df, day, filename, tankSize=189, startingTemp=40, uef=0.9, elementR = 9.9, stringLen=3, losses=14):

    timeSteps = 24

    if int(interval) < 59:
        timeSteps = 48
    i = day * timeSteps
    j = i + timeSteps
    filename = filename.replace(".csv", f"_{tankSize}_{startingTemp}_{uef}_{day}_{elementR}_{stringLen}_{losses}.png")
    filenameCsv = filename.replace(".png", f"_data.csv")

    if not os.path.exists(filename):
        # Create a figure
        fig = plt.figure(figsize=(15, 8))
        tkw = dict(size=4, width=1.5)
        ax = fig.add_subplot(4, 1, (1))
        twin1 = ax.twinx()
        ax.set_ylim(-50, 1050)
        twin1.set_ylim(-10, 40)

        ax2 = fig.add_subplot(4, 1, (2, 4), sharex=ax)
        twin2 = ax2.twinx()
        ax2.set_ylim(-10, 100)
        twin2.set_ylim(-200, 2000)

        df["90 Degree Zenith"] = 90

        singleDay = df[:][i:j]

        # heat capacity Cp of water is 4.186kJ/kg-K
        heatCapOfWater = 4186
        # j/l/k
        singleDay["Mixing Valve Limit"] = 85
        singleDay["T&P Valve Limit"] = 98
        singleDay["Desired Output Temp"] = startingTemp

        # do a rough first pass with rough standby losses
        singleDay["standbyLoss"] = 60
        if uef > 0.92:
            singleDay["standbyLoss"] = 40
        if uef > 0.94:
            singleDay["standbyLoss"] = 20

        singleDay["Net Power"] = singleDay["generation"] - singleDay["standbyLoss"]
        singleDay["energyFlux"] = singleDay["Net Power"] * 60 * float(interval)
        singleDay["Tank Temperature"] = (
            singleDay["energyFlux"].cumsum() / (heatCapOfWater * tankSize)
        ) + startingTemp

        # now do a better calculation with more accurate standby loss
        singleDay["Ambient Temperature"] = 16
        singleDay["standbyLoss"] = standbyLoss(
            uef, singleDay["Tank Temperature"], singleDay["Ambient Temperature"]
        )
        singleDay["Net Power"] = singleDay["generation"] - singleDay["standbyLoss"]
        singleDay["energyFlux"] = singleDay["Net Power"] * 60 * float(interval)
        singleDay["Tank Temperature"] = (
            singleDay["energyFlux"].cumsum() / (heatCapOfWater * tankSize)
        ) + startingTemp

        # one more round to converge better
        singleDay["standbyLoss"] = standbyLoss(
            uef, singleDay["Tank Temperature"], singleDay["Ambient Temperature"]
        )
        singleDay["Net Power"] = singleDay["generation"] - singleDay["standbyLoss"]
        singleDay["energyFlux"] = singleDay["Net Power"] * 60 * float(interval)
        singleDay["Tank Temperature"] = (
            singleDay["energyFlux"].cumsum() / (heatCapOfWater * tankSize)
        ) + startingTemp

        jouleSum = singleDay["energyFlux"].sum()
        maxStandbyLoss = singleDay["standbyLoss"].max()
        maxSolarPower = singleDay["generation"].max()
        maxTankTemp = singleDay["Tank Temperature"].max()

        total_kWh = jouleSum * 0.0000002778

        # tpoa, poa = (Transmitted) plane of array irradiance [W/m2]
        
        #pvlib is a bit more optimistic then pvwatts, so we add a fudge factor
        conversion_factor = 0.9
        singleDay["No MPPT Power"] = pvLibTest.getPowerAtLoad(module_params,singleDay["tpoa"].to_numpy(), singleDay["tcell"].to_numpy(),elementR/stringLen) * stringLen * (1.0-(losses/100.0))
        singleDay["No MPPT Power"] = (singleDay["No MPPT Power"] * conversion_factor) - singleDay["standbyLoss"]

        d = convert_day_of_year(day)
        ax.set_title(
            f"{d},  Net Thermal Energy Gain = {total_kWh:.2f} (kWh)", size="xx-large"
        )
        # fig.supxlabel(f"uef= {uef:.2f} tankSize ={tankSize}")
        fig.supxlabel(
            f"UEF={uef:.2f}   Max Solar Power={maxSolarPower:.1f}(W)   Max Standby Loss={maxStandbyLoss:.1f}(W)   Max Tank Temp={maxTankTemp:.1f}(℃)",
            size="large",
        )

        ax.plot("DNI", "-s", data=singleDay, label="DNI")
        ax.plot("DHI", "->", data=singleDay)
        ax.plot("GHI", "-o", data=singleDay)
        ax.grid(False)
        ax.tick_params("x", labelbottom=False)
        ax.set_ylabel("Solar Radiation (W/m2)")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

        twin1.plot("Temperature", "k--", data=singleDay)
        twin1.yaxis.label.set_color("k")
        twin1.set_ylabel("Outside Air(℃)")
        twin1.tick_params(axis="y", colors="k", **tkw)

        ax2.plot("T&P Valve Limit", "r-", data=singleDay)
        ax2.plot("Mixing Valve Limit", "r--", data=singleDay)
        ax2.plot("Tank Temperature", "b-o", data=singleDay)
        ax2.plot("Desired Output Temp", "k-.", data=singleDay)
        ax2.set_ylabel("Mean Water Tank Temperature (℃)")
        ax2.yaxis.label.set_color("b")
        ax2.tick_params(axis="y", colors="b", **tkw)

        twin2.plot("Net Power", "g-", data=singleDay)
        twin2.plot("No MPPT Power", "g.", data=singleDay)
        twin2.set_ylabel("Net Water Heating Power(W)")
        twin2.tick_params(axis="y", colors="g", **tkw)
        twin2.yaxis.label.set_color("g")
        twin2.grid(False)

        ax.legend(loc=2, ncol=4, frameon=False)
        ax2.legend(loc=2, ncol=4, frameon=False)
        twin2.legend(loc=1, ncol=1, frameon=False)
        twin1.legend(loc=1, ncol=1, frameon=False)

        plt.tight_layout()

        fig.savefig(filename)
        singleDay.to_csv(filenameCsv)

    return filenameCsv, filename


@app.route("/sim/graph", methods=["POST", "GET"])
@app.route("/graph", methods=["POST", "GET"])
def getGraph():

    lat = float(request.args.get("lat", "40.57"))
    lon = float(request.args.get("lon", "-105.07"))
    year = int(request.args.get("year", "2022"))
    day = int(request.args.get("day", "180"))
    power_kW = float(request.args.get("pwr", "1000"))
    tilt = float(request.args.get("tilt", "40"))
    startingTemp = float(request.args.get("startingTemp", "40"))
    liters = int(request.args.get("liters", "189"))
    uef = float(request.args.get("uef", "0.90"))
    azimuth = int(request.args.get("azimuth", "180"))
    losses = int(request.args.get("losses", "14"))
    module_type = int(request.args.get("module_type", "0"))
    string_length = int(request.args.get("pps", "3"))
    elementR = float(request.args.get("Re", "10.2"))

    df, filename, filenameJson = runSim(
        lat, lon, year, power_kW, tilt, azimuth, module_type, losses, folder
    )

    csv, graph = nsrdb_plot(
        df, day, filename, tankSize=liters, startingTemp=startingTemp, uef=uef, elementR=elementR,stringLen=string_length,losses=losses
    )

    if os.path.exists(graph):
        response = send_file(graph, mimetype="image/png")
        return response

    return "error making graph"


@app.route("/sim/csv", methods=["POST", "GET"])
@app.route("/csv", methods=["POST", "GET"])
def getCsv():

    lat = float(request.args.get("lat", "40.57"))
    lon = float(request.args.get("lon", "-105.07"))
    year = int(request.args.get("year", "2022"))
    power_kW = float(request.args.get("pwr", "1000"))
    tilt = float(request.args.get("tilt", "40"))
    azimuth = float(request.args.get("azimuth", "180"))
    losses = float(request.args.get("losses", "14"))
    module_type = int(request.args.get("module_type", "0"))

    df, filename, filename_json = runSim(
        lat, lon, year, power_kW, tilt, azimuth, module_type, losses, folder
    )

    if os.path.exists(filename):
        response = send_file(filename, mimetype="text/csv")
        return response

    return "error making csv"


@app.route("/sim/json", methods=["POST", "GET"])
@app.route("/json", methods=["POST", "GET"])
def getJson():

    lat = float(request.args.get("lat", "40.57"))
    lon = float(request.args.get("lon", "-105.07"))
    power_kW = float(request.args.get("pwr", "1000"))
    tilt = float(request.args.get("tilt", "40"))
    azimuth = float(request.args.get("azimuth", "180"))
    losses = float(request.args.get("losses", "14"))
    module_type = int(request.args.get("module_type", "0"))
    year = int(request.args.get("year", "2022"))

    filename, hash = runMonthlySimJson(
        lat, lon, year, power_kW, tilt, azimuth, module_type, losses, folder
    )

    if os.path.exists(filename):
        response = send_file(filename, mimetype="application/json")
        response.access_control_allow_origin = "*"
        return response

    return "error making json"


@app.route("/sim/healthCheck", methods=["GET"])
@app.route("/sim/", methods=["GET"])
@app.route("/", methods=["GET"])
def health_check_root():
    return "Hello, the server is alive!"


if __name__ == "__main__":
   #app.run()
    runSim()
    #runMonthlySimJson()
