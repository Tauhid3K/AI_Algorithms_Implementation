from collections import deque


def bidirectional_search(graph, start, goal):
	# Check start and goal
	if start not in graph or goal not in graph:
		return []
	if start == goal:
		return [start]
	# for checking if start and goal are the same,

	# BFS data from start side
	queue_start = deque([start])
	visited_start = {start}
	parent_start = {start: None}
	# traversal_start = [] 

	# BFS data from goal side
	queue_goal = deque([goal])
	visited_goal = {goal}
	parent_goal = {goal: None}
	# traversal_goal = []  

	# Keep searching until one frontier becomes empty
	while queue_start and queue_goal:
		# Expand from start side
		node_start = queue_start.popleft()
		# traversal_start.append(node_start)  # Uncomment to record traversal
		for neighbor in graph.get(node_start, []):
			if neighbor not in visited_start:
				visited_start.add(neighbor)  		 # Mark discovered from start side
				parent_start[neighbor] = node_start  # Save parent for path rebuild

				# Meeting point found
				if neighbor in visited_goal:
					# Build path: start -> meet
					left = []
					current = neighbor
					while current is not None:
						left.append(current)
						current = parent_start[current]
					left.reverse()

					# Build path: meet -> goal
					right = []
					current = parent_goal[neighbor]
					while current is not None:
						right.append(current)
						current = parent_goal[current]

					return left + right

				queue_start.append(neighbor)  # Continue BFS from start side

		# Expand from goal side
		node_goal = queue_goal.popleft()
		# traversal_goal.append(node_goal) 
		for neighbor in graph.get(node_goal, []):
			if neighbor not in visited_goal:
				visited_goal.add(neighbor)  # Mark discovered from goal side
				parent_goal[neighbor] = node_goal  # Save parent for path rebuild

				# Meeting point found
				if neighbor in visited_start:
					# Reconstruct full path using parent maps from both sides
					# Build path: start -> meet
					left = []
					current = neighbor
					while current is not None:
						left.append(current)
						current = parent_start[current]
					left.reverse()

					# Build path: meet -> goal
					right = []
					current = parent_goal[neighbor]
					while current is not None:
						right.append(current)
						current = parent_goal[current]

					return left + right

				queue_goal.append(neighbor)  # Continue BFS from goal side

	# No meeting point found, so no path exists
	return []


if __name__ == "__main__":
	# Example graph
	graph = {
		'A': ['B', 'C'],
		'B': ['A', 'D', 'E'],
		'C': ['A', 'F', 'G'],
		'D': ['B', 'H'],
		'E': ['B', 'I'],
		'F': ['C', 'J'],
		'G': ['C', 'K'],
		'H': ['D', 'L'],
		'I': ['E', 'L'],
		'J': ['F', 'M'],
		'K': ['G', 'M'],
		'L': ['H', 'I', 'N'],
		'M': ['J', 'K', 'N'],
		'N': ['L', 'M']
	}

	start_node = 'A'
	goal_node = 'L'

	# Run search and print result path
	path = bidirectional_search(graph, start_node, goal_node)
	print("Path:", path if path else "No path found")

	# print("Start Traversal:", traversal_start)
	# print("Goal Traversal:", traversal_goal)