# BEST FLIGHT ROUTE

The purpose of this program is to enable a user to find the best route for their trip.

## Program Execution

This project was built and tested in a Linux environment. You must have python3 installed.

Initially it will be necessary to install the packages used in this project. It is interesting that these are installed in a "virtual env".

In the folder where the project files are located, run:

    $ python3 -m venv myenv

    $ source myenv/bin/activate

    $ pip install -r requirements.txt

Then the program will be ready to run.

### Unit tests

To run the unit tests, run (with virtual env enabled):

    $ python -m unittest tests/test.py -v

One detail is that the test for adding routes changes the original input-routes.csv file. So it is interesting to restore the backup when using the API.

### Console Interface

In the console run:

    $ python console_interface.py input-routes.csv

Inside the console, just type the route in FROM-TO format to get the best route and Ctrl + c to end the execution.

### WEB Interface

To run the BE, run:

    $ python app.py

The API will run on port 5001, so make sure it's not being used by another application.

To facilitate the interaction with this API, a simple HTML page was built, which allows the consultation and addition of new routes. To use it, just open the index.html file that is inside the webInterface directory.

There is also the option of interacting via Postman. To do so, just import the file Routes.postman_collection.js. It contains the methods mentioned above.

### Structure

    ├── Dijkstra
        ├── Graph.py # Class that implements the search algorithm
    ├── Errors
        ├── errors.py # Custom error classes
    ├── FileIO
        ├── file_io.py # Methods for reading and writing the input file
    ├── webInterface # Web page for API interaction
    ├── app.py # API for querying and registering routes
    ├── Routes.postman.json # Postman collection for API interaction
    ├── console_interface.py # Console interface for API interaction
    ├── utils.py # Method for validating user input
    ├── input-routes.csv # Input data file
    ├── input-routes-bkp.csv # Backup input data file
    ├── requirements.txt # List of packages needed to run the program
    └── README.md

### Project Decisions

Because it is a simple API, the Flask framework was chosen,
for its flexibility and simple development model.

For the search algorithm Dijkstra was chosen, which proposes the
calculation of the least cost path between the vertices of a graph.

### REST API

The API has 2 endpoints:

##### /getRoute

To query the best route, the GET method is used, where the 'FROM' and 'TO' routes are sent by query strings. The departure and destination abbreviations must be in the IATA standard (3-LETTER LOCATION CODE).

The final url structure would be like this:

/getRoute?start=FROM&end=TO

Answers:

The results will be in the result field of the payload.

- 200:

  - The query was performed successfully and the result will be in the payload.
  - The query was successful, but there is no route to the requested destinations. In this case, there will be a message reporting this result.

- 404:

  - One or both parameters sent were not registered in the input file.

- 400:

  - The format of the data sent is not valid, for example empty or non-IATA standard fields.

- 500:
  - There was an error trying to load the data file. Theoretically, this
    it would be a problem on the server side.

##### /addRoute

To add a new route, the POST method is used, following the same formats as the GET method for the departure and destination. For the cost must be sent a whole number.

The payload would be of type JSON:
{
"start": "GRU",
"end": "ORL",
"cost": "40",
}

Headers:
{
"Content-Type": "application/json"
}

Answers:

- 200:
  - The route has been added successfully.
- 400:

  - The format of the data sent is not valid, for example empty or non-IATA standard fields.

- 500:
  - There was an error trying to load the data file. Theoretically, this would be a server-side issue.
