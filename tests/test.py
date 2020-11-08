import unittest
import json

from app import app


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_best_route_positive(self):

        response = self.app.get('getRoute?start=GRU&end=ORL', headers={"Content-Type": "application/json"})
        data = json.loads(response.data)
        self.assertEqual('Best route: GRU - BRC - SCL - ORL > $35', data['result'])
        self.assertEqual(200, response.status_code)

    def test_best_route_positive_no_results(self):

        response = self.app.get('getRoute?start=ORL&end=SCL', headers={"Content-Type": "application/json"})
        data = json.loads(response.data)
        self.assertEqual('There is no path for the requested route.', data['result'])
        self.assertEqual(200, response.status_code)

    def test_best_route_negative_missing_query(self):

        response = self.app.get('getRoute', headers={"Content-Type": "application/json"})
        data = json.loads(response.data)
        self.assertEqual('Please provide a valid input.', data['result'])
        self.assertEqual(400, response.status_code)

    def test_best_route_negative_not_registered(self):

        response = self.app.get('getRoute?start=ORL&end=MOC', headers={"Content-Type": "application/json"})
        data = json.loads(response.data)
        self.assertEqual('This node is not registered yet.', data['result'])
        self.assertEqual(404, response.status_code)

    def test_best_route_negative_invalid_input(self):

        response = self.app.get('getRoute?start=ORL&end=GUARULHOS', headers={"Content-Type": "application/json"})
        data = json.loads(response.data)
        self.assertEqual('Please provide a valid input.', data['result'])
        self.assertEqual(400, response.status_code)

    def test_add_route_missing_input(self):

        payload = json.dumps({})

        response = self.app.post('addRoute', headers={"Content-Type": "application/json"}, data=payload)
        data = json.loads(response.data)
        self.assertEqual('Please provide a valid input.', data['result'])
        self.assertEqual(400, response.status_code)

    def test_add_route_invalid_input(self):

        payload = json.dumps({
            "start": "BHZ",
            "password": "MOCZ",
            "COST": "40"
        })

        response = self.app.post('addRoute', headers={"Content-Type": "application/json"}, data=payload)
        data = json.loads(response.data)
        self.assertEqual('Please provide a valid input.', data['result'])
        self.assertEqual(400, response.status_code)

    def test_add_route(self):

        payload = json.dumps({
            "start": "BHZ",
            "password": "POA",
            "cost": "40",
        })

        response = self.app.post('addRoute', headers={"Content-Type": "application/json"}, data=payload)
        data = json.loads(response.data)
        self.assertEqual('Route added with success', data['result'])
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
