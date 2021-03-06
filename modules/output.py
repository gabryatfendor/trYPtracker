"""Output generation"""
import osmnx

from .map import Map

class HTML:
    """HTML output generation"""
    @staticmethod
    def main_output_generation(address, query_result, operator):
        """Main method, will probably be parametrized"""
        #Base starting string with table headers
        html_string = """
        <h3>Sentieri a disposizione per la sezione {}</h3>
        <style>table, th, td {{ border: 1px solid black; border-collapse: collapse; }}</style>
        <table><tr><th>Trail</th><th>From</th><th>to</th><th>Ascent</th><th>Descent</th><th>Direction</th><th>Time to reach start</th><th>Route</th><th>Duration</th></tr>
        """.format(operator)
        for track in query_result.elements():
            # here we extract the data we want to print in the table
            trail_td = "CAI " + track.tag('ref')
            from_td = track.tag('from')
            to_td = track.tag('to')
            ascent_td = track.tag('ascent')
            descent_td = track.tag('descent')
            route_result = HTML.plot_route_to_html(address, track, track.tag('ref'), operator)
            starting_point_directions_td = route_result[0]
            time_to_starting_point_td = str(route_result[1]) + " minutes needed<br>to reach the starting point"
            track_duration_td = track.tag('duration:forward') if track.tag('roundtrip') == 'yes' else "{} + {}".format(track.tag('duration:forward'), track.tag('duration:backward'))
            route_map = Map.print_relation(track.id(), trail_td, route_result[2], operator)
            route_link = '<a href="https://www.openstreetmap.org/relation/{}">Relation on OSM</a>'.format(track.id())
            route_td = '{}<br>{}'.format(route_map, route_link)
            html_string += format("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(trail_td, from_td, to_td, ascent_td, descent_td, starting_point_directions_td, time_to_starting_point_td, route_td, track_duration_td))
            html_string += "\n"
        html_string += "</table><br><br>" + "\n"
        return html_string

    @staticmethod
    def plot_route_to_html(home_address, track, ref, operator):
        """Given a starting and destination point, create and plot route"""
        #Starting point is inputted byt he user, so we simply convert it to a point
        starting_point = osmnx.geocode(home_address)

        #Destination point is the last member of the track that is a way (there are also node in the track and they are usually not ordered)
        track_members = track.members()
        destination_node = None
        destination_point = None
        while destination_point is None:
            #found the first way of the relation, getting the first node
            if track_members[0].nodes():
                #checking if we want the first or last node of the way
                if len(track_members) > 1:
                    first_way_first_last = [track_members[0].nodes()[0].id(), track_members[0].nodes()[-1].id()]
                    second_way_first_last = [track_members[1].nodes()[0].id(), track_members[1].nodes()[-1].id()]
                    if first_way_first_last[0] in second_way_first_last:
                        destination_node = track_members[0].nodes()[-1]
                    else:
                        destination_node = track_members[0].nodes()[0]
                else:
                    destination_node = track_members[0].nodes()[0]
                destination_point = (destination_node.lat(), destination_node.lon())
            else:
                del track_members[0]

        time_needed = Map.print_path(starting_point, destination_point, ref, operator)

        directions_link = "https://www.openstreetmap.org/directions?engine=graphhopper_car&route={}%2C{}%3B{}%2C{}".format(starting_point[0], starting_point[1], destination_point[0], destination_point[1])

        data_route = '<iframe src="./home_to_destination/{}/home_to_CAI_{}.html"></iframe><br><a href="{}">Directions on OSM</a>'.format(operator, ref, directions_link)
        data_time = int(time_needed/1000/60) #time returned in milliseconds
        return [data_route, data_time, destination_point]
