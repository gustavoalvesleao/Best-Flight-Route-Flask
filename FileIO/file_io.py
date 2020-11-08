import csv


def read_csv(file_path):
    try:
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            input_edges = []
            for row in csv_reader:
                input_edges.append(tuple(row.values()))
            return input_edges
    except FileNotFoundError as e:
        raise FileNotFoundError(e)


def write_in_csv(file_path, new_route):
    try:
        with open(file_path, mode='a') as input_edges:
            employee_writer = csv.writer(input_edges, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([new_route[0], new_route[1], str(new_route[2])])
    except FileNotFoundError:
        raise FileNotFoundError
