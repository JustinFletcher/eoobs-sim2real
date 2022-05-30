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

    samples_dict = dict()

    # TODO: externalize.
    file_signature = "*.txt"
    print(flags.real_data_directory)

    # Iterate over each file, where each file is an observation.
    for filename in glob(os.path.join(flags.real_data_directory,
                                      file_signature)):


        print("Building observation: %s" % (filename))

        # Create a dictionary to store this observation.
        sample_dict = dict()

        # First, populate the metadata for this ob. This will vary in practice.
        sample_metadata_dict = dict()
        sample_metadata_dict["object_identifier"] = str(uuid.uuid4())
        sample_metadata_dict["sample_mode"] = "hyperspectral"

        # Create lists to hold the data and metadata for this observation.
        filter_bands = list()
        measured_observations = list()

        # Open the file containing the current observation.
        with open(filename) as file:

            # Read the lines from the file, filtering whitespace.
            lines = filter(None, (line.rstrip() for line in file))

            # Iterate over each line in the file.
            for line in lines:

                # Check if this line contains metadata and, if it does, then...
                if line[0] == "#":
                    # print("Metadata")
                    # ...remove the #, delimit by =, remove the whitespace,...
                    try:
                        (key, value) = [s.strip() for s in line[1:].split("=")]
                    except ValueError:
                        [key] = [s.strip() for s in line[1:].split("=")]
                        value = ""
                    # ...and assign the key-value pair to the metadata dict.
                    sample_metadata_dict[key] = value
                # If the line doesn't contain metadata, check for headers.
                elif (line[0] == "-") or (line[0] == "W"):
                    # print("Header")

                    pass
                # The line was neither header nor metadata, so it is data.
                else:
                    # print("Data")

                    # Remove excess white space, then split by spaces.
                    data = [float(s) for s in " ".join(line.split()).split()]

                    # The 0th element is wavelength, the second is flux.
                    filter_bands.append(data[0])
                    measured_observations.append(data[1])

        # Also add the metadata to enable simulation of this unique ob.
        sample_metadata_dict["filter_bands"] = filter_bands
        filter_bands_transmittance = [1.0 for _ in filter_bands]
        sample_metadata_dict["filter_bands_transmittance"] = filter_bands_transmittance

        # Populate the dict entry and add it uniquely to the samples dict.
        sample_dict["real"] = dict()
        sample_dict["real"]["observations"] = measured_observations
        sample_dict["metadata"] = sample_metadata_dict

        # Uniquely identify this sample, and store the observation data.
        samples_dict[sample_metadata_dict["object_identifier"]] = sample_dict

    # Write the data out to disk.
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
    parser.add_argument('--real_data_directory',
                        type=str,
                        default=os.path.join("..", "data", "vniris"),
                        help='Location of real data JSON.')

    parsed_flags, _ = parser.parse_known_args()

    cli_main(parsed_flags)