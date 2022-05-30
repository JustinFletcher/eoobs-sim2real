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

# import pyfist


def dummy_simulation_function(configuration_dict, adapter=None):
    """
    This function just draws random "simulated" data to illustrate the form
    of the solution that needs to be implemented using FIST.

    :param configuration_dict: a dictionary of metadata populated from real
                               observations.
    :return: a dict containing the simulation output, matching the form of the
             real data corresponding to configuration_dict.
    """

    simulated_output_dict = dict()
    # Switch to the selected sample mode: multi- or hyperspectral.
    if configuration_dict["sample_mode"] == "multispectral":

        # In multispectral imaging, we get one measure/image.
        simulated_observations = float(np.random.uniform(-7.0, 23.0))

    elif configuration_dict["sample_mode"]  == "hyperspectral":

        # In hyperspectral imaging, we get one measure/band.
        simulated_observations = [float(np.random.uniform(-7.0, 23.0))
                                  for _ in configuration_dict["filter_bands"]]
    else:
        raise ValueError("The configuration_dict has no valid sample_mode.")

    simulated_output_dict["observations"] = simulated_observations
    return (simulated_output_dict)


def pyfist_vniris_adapter(configuration_dict):
    """
    This function maps metadata from VNIRIS to pyFIST configurations.
    :param configuration_dict: A VNIRIS metadata dictionary.
    :return: A pyFIST configuration dictionary.
    """

    raise NotImplementedError("Glenn hasn't written me yet!")

    pyfist_configuration_dict = configuration_dict

    return pyfist_configuration_dict

def simulate_with_fist(configuration_dict, adapter=None):
    """
    This function should run FIST via pyFIST and post-process the results to
    match the structure specified by the metadata for direct comparison with
    the real data from which that metadata is derived.

    :param configuration_dict: a dictionary of metadata populated from real
                               observations.
    :return: a dict containing the simulation output, matching the form of the
             real data corresponding to configuration_dict.
    """


    raise NotImplementedError("Glenn hasn't implemented simulate_with_fist!")

    # Switch the adapter according to the real data provided.
    if adapter == "vniris":

        pyfist_configuration = pyfist_vniris_adapter(configuration_dict)
    else:

        pyfist_configuration = configuration_dict

    # Run pyFIST to generate the requested output.
    raw_fist_output = pyfist.simulate(arg1=pyfist_configuration["my_arg_a"])

    # Format the output to match the real data.
    simulated_output_dict = raw_fist_output

    return simulated_output_dict

def cli_main(flags):

    # Build the storage directory.
    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    dir_name = timestamp + "_" + str(os.getpid())
    save_path = os.path.join(".", "data", "sim", dir_name)
    os.makedirs(save_path, exist_ok=True)

    # Switch by the sim_method flag using function-as-interface.
    if flags.sim_method == "dummy":
        simulate_observation = dummy_simulation_function
    elif flags.sim_method == "fist":
        simulate_observation = simulate_with_fist
    else:
        raise ValueError("You provided an invalid --sim_method flag.")

    # Iterate over each datafile, each corresponding to one observation.
    print(flags.real_data_directory)
    for json_file in glob(os.path.join(flags.real_data_directory, "*.json")):

        # TODO: decouple from runtime via persistence here. Maybe parallelize.

        # Load and parse the metadata from the real example.
        sim_and_real_data_dict = json.load(open(json_file))
        real_observation_metadata = sim_and_real_data_dict["metadata"]

        # Simulate the real observation using only the provided metadata.
        print("Simulating observation: %s" % (sim_and_real_data_dict["uuid"]))
        simulated_output_dict = simulate_observation(real_observation_metadata,
                                                     adapter=flags.adapter)
        sim_and_real_data_dict["sim"] = simulated_output_dict

        # Write the complete collection out.
        output_file = os.path.join(save_path,
                                   sim_and_real_data_dict["uuid"] + ".json")
        json.dump(sim_and_real_data_dict,
                  open(output_file, 'w'),
                  indent=4,
                  sort_keys=True)

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide arguments.')

    # Set arguments and their default values
    latest_dir = os.path.basename(glob(os.path.join(".",
                                                    "data",
                                                    "real",
                                                    "*"))[-1])
    parser.add_argument('--real_data_directory',
                        type=str,
                        default=os.path.join(".", "data", "real", latest_dir),
                        help='Location of real data JSON.')

    parser.add_argument('--real_data_json',
                        type=str,
                        default="results.json",
                        help='Location of real data JSON.')

    parser.add_argument('--sim_method',
                        type=str,
                        default="dummy",
                        help='Either dummy or fist.')

    parser.add_argument('--adapter',
                        type=str,
                        default="vniris",
                        help='If not None, run the specified adapter.')

    parsed_flags, _ = parser.parse_known_args()

    cli_main(parsed_flags)