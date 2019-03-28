"""Output generation"""
import folium
import networkx
import osmnx

from sklearn.neighbors import KDTree

class HTML:
    """HTML output generation"""
    @staticmethod
    def main_output_generation(query_result, operator):
        """Main method, will probably be parametrized"""
        html_string = """
        <h3>Sentieri a disposizione per la sezione {}</h3>
        <style>table, th, td {{ border: 1px solid black; border-collapse: collapse; }}</style>
        <table><tr><th>Sentiero</th><th>Da</th><th>a</th><th>Direction</th><th>Time to reach start</th><th>Route</th><th>Duration</th></tr>
        """.format(operator)
        for track in query_result.elements():
            # here we extract the data we want to print in the table
            # print("Relation {} goes from way/{} -  to way/{}".format(track.id(), len(track.members()[0].nodes()), len(track.members()[-1].nodes())))
            cai_ref = "CAI " + track.tag('ref')
            track_from = track.tag('from')
            track_to = track.tag('to')
            map_directions = HTML.plot_route_to_html("Corso Europa 86 Faenza", track, track.tag('ref'))
            track_duration = track.tag('duration:forward') if track.tag('roundtrip') == 'yes' else "{} + {}".format(track.tag('duration:forward'), track.tag('duration:backward'))
            html_string += format("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(cai_ref, track_from, track_to, map_directions, "", "", track_duration))
            html_string += "\n"
        html_string += "</table><br><br>" + "\n"
        return html_string

    @staticmethod
    def plot_route_to_html(home_address, track, ref):
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
                print("Destination node is {}".format(destination_node.id()))
                destination_point = (destination_node.lat(), destination_node.lon())
            else:
                del track_members[0]

        #we now create the map and gather all the nodes
        
        #main_image = osmnx.graph_from_point(starting_point, distance=1000000)
        #nodes, _ = osmnx.graph_to_gdfs(main_image)
        #tree = KDTree(nodes[['y', 'x']], metric='euclidean')

        #Given starting and destination point, we query the KDTree for the nearest available node
        #starting_point_idx = tree.query([starting_point], k=1, return_distance=False)[0]
        #destination_point_idx = tree.query([destination_point], k=1, return_distance=False)[0]

        #closest_node_to_starting_point = nodes.iloc[starting_point_idx].index.values[0]
        #closest_node_to_destination_point = nodes.iloc[destination_point_idx].index.values[0]
        #print("Going from {} to {}".format(closest_node_to_starting_point, closest_node_to_destination_point))

        #route = networkx.shortest_path(main_image, closest_node_to_starting_point, closest_node_to_destination_point)
        #print(route)

        #folium_map = osmnx.plot_route_folium(main_image, route, route_color='green', tiles='openstreetmap')
        highest_diff = round(max(abs(destination_point[0] - starting_point[0]), abs(destination_point[1] - starting_point[1])), 3)
        zoom_factor = round(highest_diff * 10)
        folium_map = folium.Map(location=starting_point, zoom_start=12-zoom_factor, tiles='openstreetmap')
        folium.Marker(location=starting_point, icon=folium.Icon(color='red')).add_to(folium_map)
        folium.Marker(location=destination_point, icon=folium.Icon(color='blue')).add_to(folium_map)

        folium_map.save('./home_to_destination/home_to_CAI_{}.html'.format(ref))

        return '<iframe src="./home_to_destination/home_to_CAI_{}.html"></iframe>'.format(ref)

    @staticmethod
    def plot_relation_to_html(relation_id, relation_bounding_box, output_filename):
        """Given a relation print it on map"""
        main_image = osmnx.graph_from_bbox(44.2149289, 44.1869875, 11.8504766, 11.8353469)
        nodes, _ = osmnx.graph_to_gdfs(main_image)
        tree = KDTree(nodes[['y', 'x']], metric='euclidean')

        starting_point_idx = tree.query([(44.20079, 11.83539)], k=1, return_distance=False)[0]
        destination_point_idx = tree.query([(44.20966, 11.85049)], k=1, return_distance=False)[0]

        closest_node_to_starting_point = nodes.iloc[starting_point_idx].index.values[0]
        closest_node_to_destination_point = nodes.iloc[destination_point_idx].index.values[0]

        route = networkx.shortest_path(main_image, closest_node_to_starting_point, closest_node_to_destination_point)

        folium_map = osmnx.plot_route_folium(main_image, route, route_color='green', tiles='openstreetmap')
        folium.Marker(location=(44.20079, 11.83539), icon=folium.Icon(color='red')).add_to(folium_map)
        folium.Marker(location=(44.20966, 11.85049), icon=folium.Icon(color='blue')).add_to(folium_map)

        folium_map.save('./routes/{}.html'.format(output_filename))
