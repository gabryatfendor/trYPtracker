"""Finding the best path between 2 points"""
import urllib.request
import json
import configparser

import folium

from OSMPythonTools.api import Api


class Map:
    """Map handling"""
    @staticmethod
    def print_relation(relation_id, ref, route_start_point, operator):
        """Print relation on map using osm api"""
        api = Api()
        relation = api.query('relation/{}'.format(relation_id))
        node_list_to_draw = []
        map_setted = False
        folium_map = None
        for member in relation.members():
            for node in member.nodes():
                node_list_to_draw.append([node.lat(), node.lon()])
                if not map_setted:
                    map_setted = True
                    folium_map = folium.Map(location=node_list_to_draw[0], zoom_start=14, tiles='openstreetmap')
            folium.PolyLine(node_list_to_draw, color='green', weight=2.5).add_to(folium_map)
            node_list_to_draw = []

        folium.Marker(location=route_start_point, icon=folium.Icon(color='red')).add_to(folium_map)
        folium_map.save('./routes/{}/{}.html'.format(operator, ref))
        return '<iframe src="./routes/{}/{}.html"></iframe>'.format(operator, ref)

    @staticmethod
    def print_path(point_1, point_2, ref, operator):
        """Print path between two points on Folium map"""
        debug = False
        decoded_content_json = Routing.find_best_path(point_1, point_2)
        #Temporary writing of response, just for debugging purpose
        if debug:
            beautified_json = json.dumps(decoded_content_json, sort_keys=True, indent=4)
            route_json_file = open("home_to_destination/home_to_{}.json".format(ref), "w")
            route_json_file.write(beautified_json)
            route_json_file.close()
        #Extract point for route
        point_list = decoded_content_json["paths"][0]["points"]["coordinates"]
        ordered_point_list = point_list
        for coordinate in ordered_point_list:
            coordinate[0], coordinate[1] = coordinate[1], coordinate[0]

        #prepare map where to draw everything
        highest_diff = round(max(abs(point_2[0] - point_1[0]), abs(point_2[1] - point_1[1])), 3)
        zoom_factor = round(highest_diff * 10)
        folium_map = folium.Map(location=point_1, zoom_start=12-zoom_factor, tiles='openstreetmap')
        folium.Marker(location=point_1, icon=folium.Icon(color='red')).add_to(folium_map)
        folium.Marker(location=point_2, icon=folium.Icon(color='blue')).add_to(folium_map)
        folium.PolyLine(point_list, color='green', weight=2.5).add_to(folium_map)

        folium_map.save('./home_to_destination/{}/home_to_CAI_{}.html'.format(operator, ref))

        return decoded_content_json["paths"][0]["time"]


class Routing:
    """Using graphhopper API we retrieve the json of the route between 2 points"""
    config = configparser.ConfigParser()
    config.read('configuration')
    API_KEY = config['REQUEST']['api_key']
    REQUEST_URL = "https://graphhopper.com/api/1/"
    VEICHLE = config['MAPPING']['veichle']
    @staticmethod
    def find_best_path(point_1, point_2):
        """Route best path between two given points, using graphhopper"""
        headers = {
            'Accept': 'application/json; charset=utf-8'
        }

        request_string = "{}route?point={},{}&point={},{}&veichle={}&locale=en&points_encoded=false&key={}".format(Routing.REQUEST_URL, point_1[0], point_1[1], point_2[0], point_2[1], Routing.VEICHLE, Routing.API_KEY)
        request = urllib.request.Request(request_string, headers=headers)

        opener = urllib.request.build_opener()
        response_body = opener.open(request).read()
        decoded_content = response_body.decode('utf8')
        decoded_content_json = json.loads(decoded_content)

        return decoded_content_json
