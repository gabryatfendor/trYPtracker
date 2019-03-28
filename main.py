"""Generate output for CAI operators"""
from modules.output import HTML
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

def main():

    #plot_route_to_html(osmnx.geocode('Corso Europa 86 Faenza'), osmnx.geocode('Via Orzolari 18 Faenza'))
    nominatim = Nominatim()
    overpass = Overpass()
    area_id = nominatim.query('Italia').areaId()

    #result = overpass.query('rel(4259555); out bb;')
    #print(result.elements()[0].bounds('minlat'))

    #plot_relation_to_html(4259555, result.elements()[0])

    operators = ["CAI Lugo"]

    html_string = ""

    for operator in operators:
        operator_parameter = '"operator" = "{}"'.format(operator)
        query = overpassQueryBuilder(area=area_id, elementType='rel', selector=operator_parameter, out='body')
        result = overpass.query(query, timeout=600)
        html_string += HTML.main_output_generation(result, operator)

    html_file = open("output.html", "w")
    html_file.write(html_string)
    html_file.close()

if __name__ == '__main__':
    main()
