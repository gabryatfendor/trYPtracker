import requests

from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

def main():
    nominatim = Nominatim()
    overpass = Overpass()

    osmr_server = "http://router.project-osrm.org/"
    routing_query = osmr_server + "route/v1/driving/11.8929,44.2820;11.4839,44.0387"

    r = requests.get(routing_query)
    print(r.json())

    area_id = nominatim.query('Italia').areaId()

    operators = ["CAI Faenza", "CAI Lugo", "CAI Imola"]

    html_string = ""

    for operator in operators:
        operator_parameter = '"operator" = "{}"'.format(operator)
        query = overpassQueryBuilder(area=area_id, elementType='rel', selector=operator_parameter, out='body')
        result = overpass.query(query, timeout=60)
        html_string += """
        <h3>Sentieri a disposizione per la sezione {}</h3>
        <style>table, th, td {{ border: 1px solid black; border-collapse: collapse; }}</style>
        <table><tr><th>Sentiero</th><th>Da</th><th>a</th><th>Roundtrip?</th><th>Duration</th><th>stretch</th></tr>
        """.format(operator)
        for track in result.elements():
            # here we extract the data we want to print in the table
            cai_ref = "CAI " + track.tag('ref')
            track_from = track.tag('from')
            track_to = track.tag('to')
            track_roundtrip = track.tag('roundtrip')
            track_duration = track.tag('duration:forward')
            image_url = 'https://geocachernoob.files.wordpress.com/2019/03/img_0857.jpg?w=100&h=100'
            html_string += format("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><img src='{}'/></td></tr>".format(cai_ref, track_from, track_to, track_roundtrip, track_duration, image_url))
        html_string += "</table><br><br>"

    html_file = open("test.html", "w")
    html_file.write(html_string)
    html_file.close()

if __name__ == '__main__':
    main()