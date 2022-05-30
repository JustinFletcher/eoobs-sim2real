"""
Simulation framework.

Author: Justin Fletcher
Date: 26 April 2022
"""
import os
import json
import uuid
import shutil
import argparse
import datetime
import numpy as np
from glob import glob

from matplotlib import pyplot as plt


def mse(a, b):
    mses = list()
    for (a_el, b_el) in zip(a, b):
        mses.append(np.mean((np.array(a_el) - np.array(b_el)) ** 2))

    return np.array(mses)
def mae(a, b):

    return np.mean(np.abs(np.array(a) - np.array(b)))

def absolute_error(a, b):

    return np.abs(np.array(a) - np.array(b))

def squared_error(a, b):

    return (np.array(a) - np.array(b)) ** 2

def cli_main(flags):

    # Build the storage directory.
    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    dir_name = timestamp + "_" + str(os.getpid())
    save_path = os.path.join(".", "data", "analysis", dir_name)
    os.makedirs(save_path, exist_ok=True)

    # Create lists for population-level-statistics.
    real_observations = list()
    sim_observations = list()

    # Construct a function-as-interface analytic dict.
    analytic_dict = dict()
    analytic_dict["mse"] = {"function": mse}
    # analytic_dict["mae"] = {"function": mae}
    # analytic_dict["absolute_error"] = {"function": absolute_error}
    # analytic_dict["squared_error"] = {"function": squared_error}
    # TODO: Add other population-scale analytics here!

    # Iterate over each datafile, each corresponding to one observation.
    for json_file in glob(os.path.join(flags.sim_data_directory, "*.json")):

        print("Parsing file: %s" % json_file)

        # TODO: decouple from runtime via persistence here. Maybe parallelize.

        # Load and parse the metadata from the real example.
        sim_and_real_data_dict = json.load(open(json_file))
        observation_metadata = sim_and_real_data_dict["metadata"]
        real_observation = sim_and_real_data_dict["real"]["observations"]
        sim_observation = sim_and_real_data_dict["sim"]["observations"]

        # Accumulate population measurements.
        real_observations.append(real_observation)
        sim_observations.append(sim_observation)

    # Run the population-scale analytics.
    for (analytic_name, analytic) in analytic_dict.items():

        print("Running analytic: %s." % (analytic_name))
        analytic_result = analytic["function"](real_observations,
                                               sim_observations)
        if analytic_result.size == 1:
            print("Result: %s = %f." % (analytic_name, analytic_result))
        else:
            print("Result: %s =" % (analytic_name))
            print(analytic_result)
        analytic_dict[analytic_name]["result"] = analytic_result

    # TODO: add plot functions from the analytic dict.
    # plt.hist(analytic_dict["absolute_error"]["result"],
    #          bins=128)

    plt.hist(analytic_dict["mse"]["result"],
             bins=128)
    plt.show()

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide arguments.')

    # Set arguments and their default values
    latest_dir = os.path.basename(glob(os.path.join(".",
                                                    "data",
                                                    "sim",
                                                    "*"))[-1])
    parser.add_argument('--sim_data_directory',
                        type=str,
                        default=os.path.join(".", "data", "sim", latest_dir),
                        help='Location of real data JSON.')

    parser.add_argument('--real_data_json',
                        type=str,
                        default="results.json",
                        help='Location of real data JSON.')

    parser.add_argument('--sim_method',
                        type=str,
                        default="dummy",
                        help='Either dummy or fist.')

    parsed_flags, _ = parser.parse_known_args()

    cli_main(parsed_flags)