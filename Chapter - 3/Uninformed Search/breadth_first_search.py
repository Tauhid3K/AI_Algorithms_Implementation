from collections import deque   # Import deque for efficient FIFO queue operations

def bfs(graph, start, goal):    #graph as adjacency list, start and goal nodes
    							# Initialize data structures
    queue = deque([start])      
    visited = set()             
    traversal_order = []   # Track nodes in visited order
    parent = {start: None}      # Store parent of each node for path reconstruction 
								#(start has no parent)
    
    while queue:                
        
        node = queue.popleft()  # remove first node from queue
        if node not in visited: # Check if node has not been visited
            visited.add(node)   # Mark as visited
            traversal_order.append(node)  # Record in traversal order
            
            for neighbor in graph[node]:   	 # Check all neighbors
                if neighbor not in visited and neighbor not in parent:
                    parent[neighbor] = node  # Link neighbor to current node to reconstruct path later
                    queue.append(neighbor)   # Add to queue for later processing
    
    # Reconstruct path from start to goal
    shortest_path = []
    if goal in parent:          # Check if goal was found
        current = goal          # Start from goal node
        while current is not None:  	#  Start node has no parent (None) (Backtrack to start)
            shortest_path.append(current)    	# Add node to path
            current = parent[current]   # move currents parent to the current node
        shortest_path.reverse()          # Reverse to get start→goal order
        print("Goal Found!")
    else:
        print("Goal Not Found")  # Goal unreachable from start
    
    return traversal_order, shortest_path


if __name__ == "__main__": 
    # Define example graph as adjacency list
    graph = {
        'A': ['B', 'C', 'D'],
        'B': [],
        'C': ['E', 'F'],
        'D': [],
        'E': [],
        'F': ['G', 'H'],
        'G': [],
        'H': []
    }
    
    # Define start and goal nodes
    start_node = 'A'
    goal_node = 'G'
    
    # Execute BFS
    traversal_order, shortest_path = bfs(graph, start_node, goal_node)
    
    print("Traversal Order:", traversal_order)
    print("Shortest Path:", shortest_path)