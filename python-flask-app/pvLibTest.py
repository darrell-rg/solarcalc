from pvlib import pvsystem
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import PySAM.PySSC as pssc
from scipy.interpolate import CubicSpline

# Example module parameters for the Canadian Solar CS5P-220M:
parameters = {
    "Name": "Canadian Solar CS5P-220M",
    "BIPV": "N",
    "Date": "10/5/2009",
    "T_NOCT": 42.4,
    "A_c": 1.7,
    "N_s": 96,
    "I_sc_ref": 5.1,
    "V_oc_ref": 59.4,
    "I_mp_ref": 4.69,
    "V_mp_ref": 46.9,
    "alpha_sc": 0.004539,
    "beta_oc": -0.22216,
    "a_ref": 2.6373,
    "I_L_ref": 5.114,
    "I_o_ref": 8.196e-10,
    "R_s": 1.065,
    "R_sh_ref": 381.68,
    "Adjust": 8.7,
    "gamma_r": -0.476,
    "Version": "MM106",
    "PTC": 200.1,
    "Technology": "Mono-c-Si",
}

samples = 255


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



def getPvSystem(parameters):

    cases = [(1000, 55), (800, 55), (600, 55), (400, 0), (400, 25), (400, 55)]

    conditions = pd.DataFrame(cases, columns=["Geff", "Tcell"])

    # adjust the reference parameters according to the operating
    # conditions using the De Soto model:
    IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
        conditions["Geff"],
        conditions["Tcell"],
        alpha_sc=parameters["alpha_sc"],
        a_ref=parameters["a_ref"],
        I_L_ref=parameters["I_L_ref"],
        I_o_ref=parameters["I_o_ref"],
        R_sh_ref=parameters["R_sh_ref"],
        R_s=parameters["R_s"],
        EgRef=1.121,
        dEgdT=-0.0002677,
    )

    # plug the parameters into the SDE and solve for IV curves:
    SDE_params = {
        "photocurrent": IL,
        "saturation_current": I0,
        "resistance_series": Rs,
        "resistance_shunt": Rsh,
        "nNsVth": nNsVth,
    }
    curve_info = pvsystem.singlediode(method="lambertw", **SDE_params)

    v = pd.DataFrame(np.linspace(0.0, curve_info["v_oc"], samples))
    i = pd.DataFrame(pvsystem.i_from_v(voltage=v, method="lambertw", **SDE_params))

    return conditions, curve_info, v, i


# draw trend arrows
def draw_arrow(ax, label, x0, y0, rotation, size, direction):
    style = direction + "arrow"
    bbox_props = dict(boxstyle=style, fc=(0.8, 0.9, 0.9), ec="b", lw=1)
    t = ax.text(
        x0,
        y0,
        label,
        ha="left",
        va="bottom",
        rotation=rotation,
        size=size,
        bbox=bbox_props,
        zorder=-1,
    )

    bb = t.get_bbox_patch()
    bb.set_boxstyle(style, pad=0.6)


def plotPanelCurve(parameters,Rload=9.9):

    conditions, curve_info, v, i = getPvSystem(parameters)

    # plot the calculated curves:

    i_load = []
    v_load = []
    plt.figure()
    for idx, case in conditions.iterrows():
        label = (
            "$G_{eff}$ " + f"{case['Geff']} $W/m^2$\n"
            "$T_{cell}$ " + f"{case['Tcell']} $\\degree C$"
        )
        plt.plot(v[idx], i[idx], label=label)
        v_mp = curve_info["v_mp"][idx]
        i_mp = curve_info["i_mp"][idx]
        r_mp = v_mp / i_mp
        p_mp = v_mp * i_mp
        label_Rmp = f"Rmp   {r_mp:2.1f} {p_mp:3.0f}W"
        # pprint.pp(v[idx])
        closest_v_idx = 0
        closest_r_delta = 99999999
        for j, volts in v[idx].items():
            r = v[idx][j] / i[idx][j]
            delta = abs(r - Rload)
            if delta < closest_r_delta:
                closest_v_idx = j
                closest_r_delta = delta

        p_load = v[idx][closest_v_idx] * i[idx][closest_v_idx]

        percent = p_load / p_mp * 100
        label_Rload = f"RLoad {Rload:2.1f}   {percent:.0f}%"

        # mark the MPP
        plt.plot([v_mp], [i_mp], ls="", marker="o", c="k", label=label_Rmp)
        plt.plot(
            [v[idx][closest_v_idx]],
            [i[idx][closest_v_idx]],
            ls="",
            marker="s",
            c="k",
            label=label_Rload,
        )
        v_load = pd.DataFrame(np.linspace(0.0, curve_info["v_oc"][idx], samples))
        i_load = pd.DataFrame(
            np.linspace(0.0, curve_info["v_oc"][idx] / Rload, samples)
        )

    plt.plot(v_load, i_load, c="k", label=f"RLoad {Rload:2.1f}")
    plt.legend(loc=(1.0, 0))
    plt.xlabel("Module voltage [V]")
    plt.ylabel("Module current [A]")
    plt.title(parameters["Name"])
    plt.gcf().set_tight_layout(True)

    ax = plt.gca()
    draw_arrow(ax, "Irradiance", 20, 2.5, 90, 15, "r")
    draw_arrow(ax, "Temperature", 18, 1, 0, 15, "l")
    plt.show()

    print(
        pd.DataFrame(
            {
                "i_sc": curve_info["i_sc"],
                "v_oc": curve_info["v_oc"],
                "i_mp": curve_info["i_mp"],
                "v_mp": curve_info["v_mp"],
                "p_mp": curve_info["p_mp"],
            }
        )
    )


# Returns python dictionary representing SSC compute module w/ all required inputs/outputs defined
def ssc_table_to_dict(cmod, dat):
    ssc = pssc.PySSC()
    i = 0
    ssc_out = {}
    while True:
        p_ssc_entry = ssc.module_var_info(cmod, i)
        ssc_output_data_type = ssc.info_data_type(p_ssc_entry)
        if ssc_output_data_type <= 0 or ssc_output_data_type > 5:
            break
        ssc_output_data_name = str(ssc.info_name(p_ssc_entry).decode("ascii"))
        ssc_data_query = ssc.data_query(dat, ssc_output_data_name.encode("ascii"))
        if ssc_data_query > 0:
            if ssc_output_data_type == 1:
                ssc_out[ssc_output_data_name] = ssc.data_get_string(
                    dat, ssc_output_data_name.encode("ascii")
                ).decode("ascii")
            elif ssc_output_data_type == 2:
                ssc_out[ssc_output_data_name] = ssc.data_get_number(
                    dat, ssc_output_data_name.encode("ascii")
                )
            elif ssc_output_data_type == 3:
                ssc_out[ssc_output_data_name] = ssc.data_get_array(
                    dat, ssc_output_data_name.encode("ascii")
                )
            elif ssc_output_data_type == 4:
                ssc_out[ssc_output_data_name] = ssc.data_get_matrix(
                    dat, ssc_output_data_name.encode("ascii")
                )
            elif ssc_output_data_type == 5:
                ssc_out[ssc_output_data_name] = ssc.data_get_table(
                    dat, ssc_output_data_name.encode("ascii")
                )
        i = i + 1

    return ssc_out


# Returns python dictionary with empty lists for each SSC NUMBER input/output
def ssc_table_numbers_to_dict_empty(cmod_name):
    ssc = pssc.PySSC()
    cmod = ssc.module_create(cmod_name.encode("utf-8"))
    i = 0
    ssc_out = {}
    while True:

        p_ssc_entry = ssc.module_var_info(cmod, i)

        ssc_output_data_type = ssc.info_data_type(p_ssc_entry)

        # 1 = String, 2 = Number, 3 = Array, 4 = Matrix, 5 = Table
        if ssc_output_data_type <= 0 or ssc_output_data_type > 5:
            break

        ssc_output_data_name = str(ssc.info_name(p_ssc_entry).decode("ascii"))

        if ssc_output_data_type == 1:
            ssc_out[ssc_output_data_name] = []
        elif ssc_output_data_type == 2:
            ssc_out[ssc_output_data_name] = []
        elif ssc_output_data_type == 3:
            ssc_out[ssc_output_data_name] = []
        elif ssc_output_data_type == 4:
            ssc_out[ssc_output_data_name] = []
        elif ssc_output_data_type == 5:
            ssc_out[ssc_output_data_name] = []

        i = i + 1

    pssc.PySSC().module_free(cmod)

    return ssc_out



def getPowerAtLoad(parameters, Geff, Tcell, R_load):
    # adjust the reference parameters according to the operating
    # conditions using the De Soto model:
    IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
        Geff,
        Tcell,
        alpha_sc=parameters["alpha_sc"],
        a_ref=parameters["a_ref"],
        I_L_ref=parameters["I_L_ref"],
        I_o_ref=parameters["I_o_ref"],
        R_sh_ref=parameters["R_sh_ref"],
        R_s=parameters["R_s"],
        EgRef=1.121,
        dEgdT=-0.0002677,
    )

    # plug the parameters into the SDE and solve for IV curves:
    SDE_params = {
        "photocurrent": IL,
        "saturation_current": I0,
        "resistance_series": Rs,
        "resistance_shunt": Rsh,
        "nNsVth": nNsVth,
    }
    curve_info = pvsystem.singlediode(method="lambertw", **SDE_params)

    v = np.linspace(0.0, curve_info["v_oc"], samples)
    i = pvsystem.i_from_v(voltage=v, method="lambertw", **SDE_params)
    # r = v/i
    # spl = CubicSpline(v,r)
    # i_load = spl(R_load)
    # v_load = pvsystem.v_from_i(current=i_load, method="lambertw", **SDE_params)
    p_load = np.zeros_like(Geff)

    #fix backwards numpy indexing
    v=np.transpose(v)
    i=np.transpose(i)

    for idx, Geff in enumerate(p_load):
        closest_v_idx = 0
        closest_r_delta = 99999999
        # print(v[idx])
        # print(i[idx])
        # print()
        for j, volts in enumerate(v[idx]):
            r = volts / i[idx][j]
            delta = abs(r - R_load)
            if delta < closest_r_delta:
                closest_v_idx = j
                closest_r_delta = delta

        p_load[idx] = v[idx][closest_v_idx] * i[idx][closest_v_idx]

    

    return p_load


if __name__ == "__main__":
    r=3.3
    p = getPowerAtLoad(module_params, np.array([400,600,800,1000]), np.array([55,55,55,55]), r)
    print(f"power at {r}R = {p}W")
    plotPanelCurve(module_params,r)
    # runSimJson()
