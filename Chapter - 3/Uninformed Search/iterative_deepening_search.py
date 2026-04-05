def dfs_limited(tree, node, limit, visited):

	# Skip already visited nodes in this iteration
	if node in visited:
		return

	visited.append(node)  # Mark node as visited for this depth run
	# if path is not None:
	# 	path.append(node)

	print(node, end=" ")  # Print traversal in DFS order

	# if goal is not None and node == goal:
	# 	return list(path)

	# Stop expanding when depth limit is reached
	if limit == 0:
		# if path is not None:
		# 	path.pop()
		return

	# DFS expansion
	for neighbor in tree.get(node, []):
		dfs_limited(tree, neighbor, limit - 1, visited)  # Go to next childreln with decreased limit
		# limit - 1 so that not allowed to expand children anymore at limit 0	
		# result = dfs_limited(tree, neighbor, limit - 1, visited, goal, path)
		# if result is not None:
		# 	return result

	# Goal/path mode (commented)
	# if path is not None:
	# 	path.pop()
	# return None


def iterative_deepening(tree, start, max_limit):
	# Run depth-limited DFS from depth 1 up to max_limit
	for i in range(max_limit):
		print(f"Iteration {i + 1}: ", end="")
		dfs_limited(tree, start, i + 1, [])  # Fresh visited list each iteration
		print()

	# Goal/path mode (commented)
	# for i in range(max_limit):
	# 	print(f"Iteration {i + 1}: ", end="")
	# 	path = dfs_limited(tree, start, i + 1, [], goal, [])
	# 	print()
	# 	if path is not None:
	# 		return path
	# return None


if __name__ == "__main__":
	# Example tree/graph
	tree = {
		'A': ['B', 'C', 'D'],
		'B': ['E', 'F'],
		'C': ['G'],
		'D': ['H', 'I'],
		'E': [],
		'F': [],
		'G': [],
		'H': [],
		'I': []
	}

	# Start iterative deepening from A up to depth 4
	iterative_deepening(tree, 'A', 4)

	# Goal/path mode (commented)
	# goal_node = 'I'
	# path = iterative_deepening(tree, 'A', 4, goal_node)
	# print("Path:", path if path else "Goal not found")
