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
# specific language governing permissions and limitations
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
# from IPython.display import display
import urllib.request
import os

# import additional module for SAM simulation:
# import site
# Use site.addsitedir() to set the path to the SAM SDK API. Set path to the python directory.
# site.addsitedir('/Applications/sam-sdk-2015-6-30-r3/languages/python/')
from matplotlib import pyplot as plt

plt.style.use("ggplot")

import PySAM.PySSC as pssc




# Download PySAM here: https://pypi.org/project/NREL-PySAM/
# You must request an NSRDB api key from the link above
api_key = "UF7nTkUNme6EZw09aZhSG0HZeaPVHcmrBohZLdHX"
# Set the attributes to extract (e.g., dhi, ghi, etc.), separated by commas.
attributes = "ghi,dhi,dni,wind_speed,air_temperature,solar_zenith_angle"
# Set leap year to true or false. True will return leap day data if present, false will not.
leap_year = "false"
# Set time interval in minutes, i.e., '30' is half hour intervals. Valid intervals are 30 & 60.
interval = "60"
# Specify Coordinated Universal Time (UTC), 'true' will use UTC, 'false' will use the local time zone of the data.
# NOTE: In order to use the NSRDB data in SAM, you must specify UTC as 'false'. SAM requires the data to be in the
# local time zone.
utc = "false"
# Your full name, use '+' instead of spaces.
your_name = "Darrell+Taylor"
# Your reason for using the NSRDB.
reason_for_use = "testing"
# Your affiliation
your_affiliation = "none"
# Your email address
your_email = "darrell@realgo.com"
# Please join our mailing list so we can keep you up-to-date on new developments.
mailing_list = "false"


def downloadWeatherData(lat=40.57, lon=-105.07, year=2010, folder="tmp"):
    # Declare all variables as strings. Spaces must be replaced with '+', i.e., change 'John Smith' to 'John+Smith'.
    # Define the lat, long of the location and the year

    # Declare url string
    url = "https://developer.nrel.gov/api/nsrdb/v2/solar/psm3-download.csv?wkt=POINT({lon}%20{lat})&names={year}&leap_day={leap}&interval={interval}&utc={utc}&full_name={name}&email={email}&affiliation={affiliation}&mailing_list={mailing_list}&reason={reason}&api_key={api}&attributes={attr}".format(
        year=year,
        lat=lat,
        lon=lon,
        leap=leap_year,
        interval=interval,
        utc=utc,
        name=your_name,
        email=your_email,
        mailing_list=mailing_list,
        affiliation=your_affiliation,
        reason=reason_for_use,
        api=api_key,
        attr=attributes,
    )

    hash = hashlib.shake_128(url.encode()).hexdigest(32)
    filename = os.path.join(folder,hash + ".csv")
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

    # # Return just the first 2 lines to get metadata:
    # info = pd.read_csv(filename, nrows=1)
    # # See metadata for specified properties, e.g., timezone and elevation
    # timezone, elevation = info['Local Time Zone'], info['Elevation']

    # # Return all but first 2 lines of csv to get data:
    # df = pd.read_csv(filename, skiprows=2)

    # # Set the time index in the pandas dataframe:
    # df = df.set_index(pd.date_range('1/1/{yr}'.format(yr=year), freq=interval+'Min', periods=525600/int(interval)))

    return filename, hash


def runSim(lat=40.57, lon=-105.07, year=2010, folder="tmp"):

    filename, hash = downloadWeatherData(lat, lon, year, folder)
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
            freq=interval + "Min",
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
    # Set system capacity in MW
    system_capacity = 1500.0 / 1.0e6
    ssc.data_set_number(dat, b"system_capacity", system_capacity)
    # Set DC/AC ratio (or power ratio). See https://sam.nrel.gov/sites/default/files/content/virtual_conf_july_2013/07-sam-virtual-conference-2013-woodcock.pdf
    ssc.data_set_number(dat, b"dc_ac_ratio", 1.0)
    # Set tilt of system in degrees
    ssc.data_set_number(dat, b"tilt", 25)
    # Set azimuth angle (in degrees) from north (0 degrees)
    ssc.data_set_number(dat, b"azimuth", 180)
    # Set the inverter efficency
    ssc.data_set_number(dat, b"inv_eff", 96)
    # Set the system losses, in percent
    ssc.data_set_number(dat, b"losses", 14.0757)
    # Specify fixed tilt system (0=Fixed, 1=Fixed Roof, 2=1 Axis Tracker, 3=Backtracted, 4=2 Axis Tracker)
    ssc.data_set_number(dat, b"array_type", 0)
    # Set ground coverage ratio
    ssc.data_set_number(dat, b"gcr", 0.4)
    # Set constant loss adjustment
    ssc.data_set_number(dat, b"adjust:constant", 0)

    # execute and put generation results back into dataframe
    mod = ssc.module_create(b"pvwattsv5")
    ssc.module_exec(mod, dat)
    df[b"generation"] = np.array(ssc.data_get_array(dat, b"gen"))

    # free the memory
    ssc.data_free(dat)
    ssc.module_free(mod)

    # Divide sum of generation by the number of periods times the system size
    cap_factor = df[b"generation"].sum() / (525600 / int(interval) * system_capacity)

    print(f"cap_factor = {cap_factor}")

    total_energy = df[b"generation"].sum()

    print(f"total_energy = {total_energy}")

    filename_sim = os.path.join(folder , "sim_" + hash + ".csv")
    df.to_csv(filename_sim)
    return df, filename_sim


def nsrdb_plot(df, day, filename):
    i = day * 24
    filename = filename.replace(".csv", ".png")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    df["90 Degree Zenith"] = 90
    df[["GHI", "DNI", "DHI", "Solar Zenith Angle", "90 Degree Zenith"]][
        i : i + int(interval)
    ].plot(
        ax=ax,
        figsize=(15, 8),
        yticks=(np.arange(0, 900, 100)),
        style={
            "90 Degree Zenith": "--",
            "Solar Zenith Angle": "-o",
            "DNI": "-o",
            "DHI": "-o",
            "GHI": "-o",
        },
        legend=False,
    )
    df[b"generation"][i : i + 30].plot(
        ax=ax2, yticks=(np.arange(0, 4.5, 0.5)), style={"generation": "y-o"}
    )
    ax.grid()
    ax.set_ylabel("W/m2")
    ax2.set_ylabel("kW")
    ax.legend(loc=2, ncol=5, frameon=False)
    ax2.legend(loc=1, frameon=False)
    fig.savefig(filename)
    return filename




# defines initial reservations
with open('data.txt') as f:
    reservations = ast.literal_eval(f.read())

folder="tmp"

@app.route('/graph', methods=['POST', 'GET'])
def getGraph():

    lat = float(request.args.get('lat', '40.57'))
    lon = float(request.args.get('lon', '-105.07'))
    year = int(request.args.get('year', '2020'))
    day = int(request.args.get('day', '180'))

    df, filename = runSim(lat, lon, year)
    
    graph = nsrdb_plot(df, day, filename)


    if os.path.exists(graph):
        response =  send_file(graph, mimetype='image/png')
        return response

    return "error making graph"


# route relevant to the hello world
@app.route('/rs/healthCheck', methods=['GET'])
def health_check():
    return "Hello, the server is alive!"



if __name__ == "__main__":
    app.run()
