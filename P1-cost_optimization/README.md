# Ice Box Allocation Optimization

This Program addresses the problem of optimally allocating ice boxes of various sizes to meet a required capacity at the minimum cost across different cities. Each city offers different rental rates per box type, and the goal is to compute the lowest cost configuration that exactly satisfies the capacity requirement for a specified number of hours.

## Problem Statement

Given:
- **Capacity**: The total volume that must be achieved.
- **Box Sizes**: A list of available box types with their corresponding volumes.
- **City Costs**: The cost per hour for renting each box type in different cities.
- **Time**: The number of hours the boxes are needed.

The task is to determine the combination of boxes (with boxes allowed to be used multiple times) that exactly achieves the required capacity at the lowest total cost, separately for each city.

## How to Run

### 1. Clone the Repository and Navigate to directory

```bash
git clone https://github.com/bishnoipk01/assignment
cd assignment/P1-cost_optimization
```

### 2. Running the Program with Command-Line Arguments

The program is designed to accept command-line arguments for the `time_input` (number of hours) and `capacity_input` (required volume). If these arguments are not provided, the program will exit.

 **Run the script using:**

```bash
python main.py <time_input> <capacity_input>
```
### 3. Running tests

 To ensure that the program functions correctly and handles various scenarios, a suite of tests has been provided. These tests verify the correct behavior of core functions, and edge cases.

 **Run the tests using:**

```bash
python test_main.py 
```


## Approach

The solution is modeled as an **unbounded knapsack** problem:
- **Knapsack Capacity**: Represents the required volume.
- **Items**: Are the available box types.
- **Item Weight**: Is the volume of each box.
- **Item Value**: Is the cost (per hour multiplied by the given time) for renting a box.

### Dynamic Programming Strategy

1. **Filtering**: For each city, the program first filters out boxes that do not have a valid cost.
2. **DP Table Initialization**:  
   - Create an array `dp` where `dp[j]` holds the minimum cost to achieve exactly a capacity of `j`.  
   - `dp[0]` is initialized to 0 (no cost for zero capacity), while all other entries are initialized to infinity (a representation of an unreachable state).
3. **State Transition**:  
   - For each achievable capacity `j` and for each available box, the program calculates the new capacity `j + volume` if that box is used.  
   - It then updates `dp[j + volume]` if including the box results in a lower cost.
4. **Backtracking**:  
   - An auxiliary array `choice` is maintained to remember which box was added at each step.  
   - After constructing the DP table, the program backtracks from the target capacity to reconstruct the combination of boxes used.
5. **Output Formation**:  
   - The result for each city includes the region name, the total cost (or a "No solution" message if the capacity cannot be met), and a breakdown of the number of each box used.

