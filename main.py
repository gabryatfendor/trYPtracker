"""Generate output for CAI operators"""
from modules.output import HTML
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

def main():

    nominatim = Nominatim()
    overpass = Overpass()
    area_id = nominatim.query('Italia').areaId()

    operators = ["CAI Lugo"]

    html_string = ""

    for operator in operators:
        operator_parameter = '"operator" = "{}"'.format(operator)
        query = overpassQueryBuilder(area=area_id, elementType='rel', selector=operator_parameter, out='body')
        result = overpass.query(query, timeout=600)
        #TODO: parametrize the starting address
        html_string += HTML.main_output_generation("Faenza", result, operator)

    html_file = open("output.html", "w")
    html_file.write(html_string)
    html_file.close()

if __name__ == '__main__':
    main()
