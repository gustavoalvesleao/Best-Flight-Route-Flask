import sys
import os

from Dijkstra.Graph import Graph, inf
from FileIO.file_io import read_csv
from Errors.errors import WrongEdgesError, NodeDoestExist
from ultis import check_input_format


if __name__ == '__main__':

    option = int
    try:
        # Get the file from user input
        try:
            file_name = sys.argv[1]
            # Get the graph instance
            input_edges = read_csv('{}/{}'.format(os.getcwd(), file_name))
            graph = Graph(input_edges)
        except WrongEdgesError as e:
            print(e)
            sys.exit()
        except IndexError:
            print('Please enter the csv file as an argument and try again.\n')
            sys.exit()
        except FileNotFoundError:
            print('File not found. Please provide a valid file and try again.\n')
            sys.exit()

        print('Enter the desired route in the format FROM-TO, e.g: GRU-ORL\nYou can also press Ctrl + c to exit.\n')

        while True:
            try:
                [start, end] = input('Please enter the desired route: ').upper().split("-")
                if not check_input_format(start) or not check_input_format(end):
                    print('An airport code has 3 letters!\n')
                    continue
                result_route, value = graph.dijkstra(start, end)
                if value == inf:
                    print('There is no path for the requested route.')
                else:
                    output = ' - '.join(result_route)
                    print('Best route: {} > ${}\n'.format(output, value))
                    continue
            except NodeDoestExist as e:
                print('{}\n'.format(e))
                continue
            except ValueError:
                print('Please enter the input with the format FROM-TO\n')
                continue

    except KeyboardInterrupt:
        print('\nFinished by the user!')
        sys.exit()
