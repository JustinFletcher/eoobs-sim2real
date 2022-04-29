

import argparse
import numpy as np
from matplotlib import pyplot as plt
from flask import Flask

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/test/endpoint', methods=['GET', 'POST'])
def test_endpoint():

    post_count = 0

    # If a POST has been received.
    if request.method == 'POST':

        # Increment the POST count. This doesn't work - no persistence.
        # use cookies.
        post_count += 1

        # print(request.form['question'])
        # Get JSON from the Flask request object.
        input_json = request.get_json(force=True)
        print('Received POST content:')
        print(input_json)

        # Formulate a return dictionary.
        return_dict = {'post_count': post_count}

        # f = request.files['the_file']
        # f.save('./example.txt')
        print("You have POSTed")
        return return_dict
    else:
        return "You have GETed"


@app.route('/', methods=['GET', 'POST'])
def application_index():

    if request.method == 'POST':
        request.form['username']

        f = request.files['the_file']
        f.save('./example.txt')
        return "You have POSTed"
    else:
        return "You have GETed an index page"

def cli_main(flags):


    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Provide arguments.')

    # Set arguments and their default values
    parser.add_argument('--my_string', type=str,
                        default="0",
                        help='A sample string.')

    parsed_flags, _ = parser.parse_known_args()

    cli_main(parsed_flags)