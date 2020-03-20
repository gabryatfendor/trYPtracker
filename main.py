"""Generate output for CAI operators"""
import configparser
import ast
import os

from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

from modules.output import HTML

def main():
    """Main function to create the output file"""
    nominatim = Nominatim()
    overpass = Overpass()
    config = configparser.ConfigParser()
    config.read('configuration')
    area_id = nominatim.query('Italia').areaId()

    html_string = ""

    for operator in ast.literal_eval(config.get("MAPPING", "operators")):
        #create folders for needed saving operations later
        if not os.path.exists("./home_to_destination/{}".format(operator)):
            os.mkdir("./home_to_destination/{}".format(operator))
        if not os.path.exists("./routes/{}".format(operator)):
            os.mkdir("./routes/{}".format(operator))
        operator_parameter = '"operator" = "{}"'.format(operator)
        query = overpassQueryBuilder(area=area_id, elementType='rel', selector=operator_parameter, out='body')
        result = overpass.query(query, timeout=600)
        html_string += HTML.main_output_generation(config['MAPPING']['address'], result, operator)

    html_file = open("output.html", "w")
    html_file.write(html_string)
    html_file.close()

if __name__ == '__main__':
    main()
