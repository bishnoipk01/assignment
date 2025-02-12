import json
import sys
from typing import List, Tuple, Dict, Any, Union


################################
# Define available box sizes in descending order (largest to smallest).
box_sizes = [("XXL", 320), ("XL", 160), ("L", 80), ("M", 40), ("S", 20), ("XS", 10)]

# Define the cost per hour for each box type in different cities.
city_costs = {
    "Delhi": {"XS": 12, "S": 23, "M": 45, "L": 77.4, "XL": 140, "XXL": 282},
    "Mumbai": {"XS": 14, "S": None, "M": 41.3, "L": 89, "XL": 130, "XXL": 297},
    "Kolkata": {"XS": 11, "S": 20, "M": None, "L": 67, "XL": 118, "XXL": None},
}

################################


def minimize_cost(time: int, 
                  capacity: int, 
                  box_sizes: List[Tuple[str, int]], 
                  city_costs: Dict[str, Dict[str, Union[float, None]]]
                 ) -> Dict[str, List[Dict[str, Any]]]:
    """
    Determine the minimum cost for fulfilling a given capacity using available boxes,
    considering different cost rates per city.

    This function implements a dynamic programming approach. 
    For each city, it calculates the minimum cost to exactly fill the 
    required capacity, if possible, and backtracks to identify the specific count of 
    each box used.

    Parameters:
        time (int): The number of hours for which the boxes are needed.
        capacity (int): The total volume capacity that must be achieved.
        box_sizes (list of tuples): A list where each tuple consists of (box_name, box_volume).
        city_costs (dict): A dictionary mapping each city name to another dictionary,
                           which in turn maps a box type to its cost per hour.
                           
    Returns:
        dict: A dictionary with a key "Output" that contains a list of results. Each result 
              is a dictionary containing:
                - "region": The name of the city.
                - "total_cost": The computed minimum cost (or "No solution" if capacity cannot be reached).
                - "boxes": A dictionary with the count of each box type used.
    """

    # Validate inputs
    if time < 0 or capacity < 0:
        raise ValueError("Time and capacity must be non-negative integers.")
    
    results = []  # List to hold the results for each city

    # Process each city separately
    for city, cost_table in city_costs.items():
        # Prepare lists for boxes that have valid costs in this city.
        available_boxes = []
        available_volumes = []
        available_costs = []
        
        # Filter box_sizes based on availability in the current city's cost table.
        for box, size in box_sizes:
            # Check if the cost exists and is not None
            if box in cost_table and cost_table[box] is not None:
                available_boxes.append(box)
                available_volumes.append(size)
                # Multiply the cost per hour by the total time to get the total cost for that box.
                available_costs.append(cost_table[box] * time)

        n = len(available_boxes)
        # dp[j] will store the minimum cost to exactly achieve capacity j.
        dp = [float('inf')] * (capacity + 1)
        dp[0] = 0  # Base case: zero cost to achieve zero capacity.

        # choice[j] records a tuple (i, prev_j) to help trace back which box was added
        # to achieve capacity j from a previous capacity prev_j.
        choice = [None] * (capacity + 1)

        # For each intermediate capacity j, try adding each box.
        for j in range(capacity + 1):
            if dp[j] != float('inf'):
                for i in range(n):
                    new_volume = j + available_volumes[i]
                    if new_volume <= capacity:
                        new_cost = dp[j] + available_costs[i]
                        if new_cost < dp[new_volume]:
                            dp[new_volume] = new_cost
                            choice[new_volume] = (i, j)  # Store the index of the box and previous capacity.

        # Backtrack from dp[capacity] to determine the count of each box used.
        selected_boxes = {}
        if dp[capacity] == float('inf'):
            total_cost: Union[float, str] = "No solution"
        else:
            total_cost = dp[capacity]
            c = capacity
            while c > 0 and choice[c] is not None:
                i, prev_c = choice[c]
                box_name = available_boxes[i]
                selected_boxes[box_name] = selected_boxes.get(box_name, 0) + 1
                c = prev_c  # Move to the previous capacity state.

        # Append the result for the current city.
        results.append({
            "region": city,
            "total_cost": total_cost,
            "boxes": selected_boxes 
        })

    return {"Output": results}


def process_cmd_args() -> Tuple[int, int]:
    """
    Parse command line arguments for time and capacity.
    """
    try:
        time_input = int(sys.argv[1])
        capacity_input = int(sys.argv[2])
    except ValueError:
        print("Invalid input. Please provide integers for time and capacity.")
        sys.exit(1)

    return time_input, capacity_input

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <time_input> <capacity_input>")
        sys.exit(1)

    # Number of hours the boxes are needed, Total capacity required.
    time_input,capacity_input = process_cmd_args()

    # Calculate the minimum cost and the box allocation for each city.
    result = minimize_cost(time_input, capacity_input, box_sizes, city_costs)

    # Format and print the result in JSON format for readability.
    print(json.dumps(result, indent=2))
