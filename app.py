import os
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import logging

from Dijkstra.Graph import Graph, inf
from FileIO.file_io import read_csv, write_in_csv
from Errors.errors import NodeDoestExist, WrongEdgesError
from ultis import check_input_format

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

default_file = '{}/{}'.format(os.getcwd(), 'input-routes.csv')
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


def return_not_found():
    return {'result': 'This node is not registered yet.'}, 404


def return_no_path():
    return {'result': 'There is no path for the requested route.'}


def return_bad_request():
    return {'result': 'Please provide a valid input.'}, 400


def return_internal_error():
    return {'result': 'There was a error in server while loading the csv input file.'}, 500


class Route(Resource):
    @staticmethod
    def get():
        try:
            start = request.args.get('start')
            end = request.args.get('end')
            if not check_input_format(start) or not check_input_format(end):
                return return_bad_request()

            input_edges = read_csv(default_file)
            graph = Graph(input_edges)
            result_route, value = graph.dijkstra(start.upper(), end.upper())

            if value == inf:
                return return_no_path()
            output = ' - '.join(result_route)
            return {'result': 'Best route: {} > ${}'.format(output, value)}

        except TypeError as e:
            logging.error(e)
            return return_bad_request()
        except FileNotFoundError as e:
            logging.error(e)
            return return_internal_error()
        except WrongEdgesError as e:
            logging.error(e)
            return_internal_error()
        except NodeDoestExist as e:
            logging.error(e)
            return return_not_found()
        except ValueError as e:
            logging.error(e)
            return return_bad_request()


class AddRoute(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()
            start, end, cost = data.values()

            if not check_input_format(start) or not check_input_format(end) or type(int(cost)) != int:
                return return_bad_request()

            write_in_csv(default_file, (start.upper(), end.upper(), cost))
            return {'result': 'Route added with success'}

        except FileNotFoundError as e:
            logging.error(e)
            return return_internal_error()
        except ValueError as e:
            logging.error(e)
            return return_bad_request()


api.add_resource(Route, '/getRoute')
api.add_resource(AddRoute, '/addRoute')

if __name__ == "__main__":
    app.run(port=5001)
