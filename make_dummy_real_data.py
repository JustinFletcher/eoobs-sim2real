"""
Dummy data generator.

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


def cli_main(flags):

    timestamp = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    dir_name = timestamp + "_" + str(os.getpid())
    save_path = os.path.join(".", "data", "real", dir_name)
    os.makedirs(save_path, exist_ok=True)

    # TODO: externalize.
    spectral_resolution = 2048
    spectral_start_nm = 100.0
    spectral_stop_nm = 1200.0

    samples_dict = dict()

    for sample_num in range(flags.num_samples):

        sample_dict = dict()

        # First, populate the metadata for this ob. This will vary in practice.
        sample_metadata_dict = dict()
        sample_metadata_dict["observation_timestamp"] = timestamp
        sample_metadata_dict["object_identifier"] = str(uuid.uuid4())
        sample_metadata_dict["sample_mode"] = flags.sample_mode

        # Build or load the filters used for this simulated observation
        if flags.sample_mode == "multispectral":

            # TODO: Add a flag switch to load sloan filters robustly.
            # TODO: Plan: load an arb. vect., then interp. to sim'd linspace.
            # This is dummy data, so I'm building a random filter.
            filter_bands_nm = np.linspace(spectral_start_nm,
                                          spectral_stop_nm,
                                          spectral_resolution).tolist()

            # Generate random transmittances.
            filter_bands_transmittance = [float(np.random.uniform(0.0, 1.0))
                                          for _ in filter_bands_nm]
        elif flags.sample_mode == "hyperspectral":
            # In hyperspectral imaging, we get one measure/band.
            filter_bands_nm = np.linspace(spectral_start_nm,
                                          spectral_stop_nm,
                                          spectral_resolution).tolist()

            # In hyperspectral imaging, we have ~uniform transmittance.
            # TODO: Strictly, this is redundant. But it's also simple and fast.
            filter_bands_transmittance = [1.0 for _ in filter_bands_nm]

        else:
            raise ValueError('You gave an invalid "--sample_mode".')

        # Also add the metadata to enable simulation of this unique ob.
        # TODO: This storage method is extremely dumb but easy. Replace it.
        sample_metadata_dict["filter_bands_transmittance"] = filter_bands_transmittance
        sample_metadata_dict["filter_bands_nm"] = filter_bands_nm

        # TODO: All metadata needed to run FIST must be added here!

        # Switch to the selected sample mode: multi- or hyperspectral.
        if flags.sample_mode == "multispectral":

            # In multispectral imaging, we get one measure/image.
            measured_observations = float(np.random.uniform(-7.0, 23.0))

        elif flags.sample_mode == "hyperspectral":

            # In hyperspectral imaging, we get one measure/band.
            measured_observations = [float(np.random.uniform(-7.0, 23.0))
                                   for _ in filter_bands_nm]

        else:
            raise ValueError('You gave an invalid "--sample_mode".')

        # Populate the dict entry and add it uniquely to the samples dict.
        sample_dict["real"] = dict()
        sample_dict["real"]["observations"] = measured_observations
        sample_dict["metadata"] = sample_metadata_dict

        # Uniquely identify this "real" sample, and store the observation data.
        samples_dict[str(uuid.uuid4())] = sample_dict

    # Write the data out to disk.
    # save_as_json(save_path, samples_dict)
    # TODO: refactor to decouple the obs files.
    for (sample_uuid, sample_data) in samples_dict.items():
        sample_data["uuid"] = sample_uuid
        print("Writing observation: %s" % (sample_uuid))
        json_file = os.path.join(save_path, sample_uuid + ".json")
        json.dump(sample_data, open(json_file, 'w'), indent=4, sort_keys=True)

    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide arguments.')


    # Set arguments and their default values
    parser.add_argument('--num_samples',
                        type=int,
                        default=64,
                        help='The number of samples to generate.')
    parser.add_argument('--sample_mode',
                        type=str,
                        default="multispectral",
                        help='Either multispectral or hyperspectral.')

    parsed_flags, _ = parser.parse_known_args()

    cli_main(parsed_flags)