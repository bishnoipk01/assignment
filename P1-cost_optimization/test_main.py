"""
Unit tests for the minimize_cost function.

This module validates the behavior of the minimize_cost function

Test cases include:
- Standard expected output for a sample input.
- Edge cases such as capacity zero or capacity that cannot be met.
- The impact of a time multiplier on the overall cost.
- Scenarios with only one box type available.
- Scenarios where no boxes are available.
- Scenarios where the capacity exactly matches the volume of a specific box.
- Negative input values for capacity and time, which should raise a ValueError.
"""

import unittest
from main import minimize_cost

class TestMinimizeCostCalculation(unittest.TestCase):

    def setUp(self):
        # Define available box sizes in the required order.
        self.box_sizes = [("XXL", 320), ("XL", 160), ("L", 80), ("M", 40), ("S", 20), ("XS", 10)]
        
        # Define cost of each box per hour in different cities.
        self.city_costs = {
            "Delhi": {"XS": 12, "S": 23, "M": 45, "L": 77.4, "XL": 140, "XXL": 282},
            "Mumbai": {"XS": 14, "S": None, "M": 41.3, "L": 89, "XL": 130, "XXL": 297},
            "Kolkata": {"XS": 11, "S": 20, "M": None, "L": 67, "XL": 118, "XXL": None},
        }
        self.time_input = 1
        self.capacity_input = 1150

    def test_expected_output(self):
        """
        Validate that minimize_cost produces the expected result for the sample input.
        """
        expected = {
            "Output": [
                {"region": "Delhi", "total_cost": 1015, "boxes": {"XL": 7, "S": 1, "XS": 1}},
                {"region": "Mumbai", "total_cost": 952, "boxes": {"XL": 7, "XS": 3}},
                {"region": "Kolkata", "total_cost": 857, "boxes": {"XL": 7, "S": 1, "XS": 1}}
            ]
        }
        result = minimize_cost(self.time_input, self.capacity_input, self.box_sizes, self.city_costs)
        self.assertEqual(result, expected)

    def test_capacity_zero(self):
        """
        For capacity 0, expect a total cost of 0 and no boxes selected.
        """
        expected = {
            "Output": [
                {"region": "Delhi", "total_cost": 0, "boxes": {}},
                {"region": "Mumbai", "total_cost": 0, "boxes": {}},
                {"region": "Kolkata", "total_cost": 0, "boxes": {}}
            ]
        }
        result = minimize_cost(self.time_input, 0, self.box_sizes, self.city_costs)
        self.assertEqual(result, expected)

    def test_no_solution(self):
        """
        For a capacity that cannot be reached (e.g. capacity 5), expect "No solution" and no boxes.
        """
        expected = {
            "Output": [
                {"region": "Delhi", "total_cost": "No solution", "boxes": {}},
                {"region": "Mumbai", "total_cost": "No solution", "boxes": {}},
                {"region": "Kolkata", "total_cost": "No solution", "boxes": {}}
            ]
        }
        result = minimize_cost(self.time_input, 5, self.box_sizes, self.city_costs)
        self.assertEqual(result, expected)

    def test_time_multiplier(self):
        """
        Test the case when the time parameter is greater than 1.
        The total cost should scale linearly with time.
        """
        time_input = 2  # Double the time
        expected = {
            "Output": [
                {"region": "Delhi", "total_cost": 2030, "boxes": {"XL": 7, "S": 1, "XS": 1}},
                {"region": "Mumbai", "total_cost": 1904, "boxes": {"XL": 7, "XS": 3}},
                {"region": "Kolkata", "total_cost": 1714, "boxes": {"XL": 7, "S": 1, "XS": 1}}
            ]
        }
        result = minimize_cost(time_input, self.capacity_input, self.box_sizes, self.city_costs)
        self.assertEqual(result, expected)

    def test_single_box_type(self):
        """
        Test a scenario where only one box type is available.
        For example, with only 'L' boxes available in the city, capacity 160 should require 2 boxes.
        """
        city_costs = {
            "TestCity": {"XXL": None, "XL": None, "L": 50, "M": None, "S": None, "XS": None}
        }
        capacity_input = 160  # Requires exactly 2 boxes of type 'L' (each of volume 80)
        expected = {
            "Output": [
                {"region": "TestCity", "total_cost": 100, "boxes": {"L": 2}}
            ]
        }
        result = minimize_cost(self.time_input, capacity_input, self.box_sizes, city_costs)
        self.assertEqual(result, expected)
    
    def test_no_available_boxes(self):
        """
        Test the scenario where no boxes are available (i.e., all cost values are None).
        For any positive capacity, the solution should be "No solution".
        """
        city_costs = {
            "EmptyCity": {"XXL": None, "XL": None, "L": None, "M": None, "S": None, "XS": None}
        }
        capacity_input = 100
        expected = {
            "Output": [
                {"region": "EmptyCity", "total_cost": "No solution", "boxes": {}}
            ]
        }
        result = minimize_cost(self.time_input, capacity_input, self.box_sizes, city_costs)
        self.assertEqual(result, expected)

    def test_exact_box_match(self):
        """
        When the capacity exactly matches the volume of a single box type,
        the optimal solution should be to select that box.
        For instance, if capacity equals 160, the best solution should be one 'XL' box.
        """
        capacity_input = 160
        expected = {
            "Output": [
                {"region": "Delhi", "total_cost": 140, "boxes": {"XL": 1}},
                {"region": "Mumbai", "total_cost": 130, "boxes": {"XL": 1}},
                {"region": "Kolkata", "total_cost": 118, "boxes": {"XL": 1}}
            ]
        }
        result = minimize_cost(self.time_input, capacity_input, self.box_sizes, self.city_costs)
        self.assertEqual(result, expected)

    def test_negative_capacity(self):
        """
        Negative capacity values are invalid.
        The function should raise a ValueError when provided a negative capacity.
        """
        with self.assertRaises(ValueError):
            minimize_cost(self.time_input, -10, self.box_sizes, self.city_costs)

  

if __name__ == '__main__':
    unittest.main()
