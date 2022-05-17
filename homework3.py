from queue import PriorityQueue

def initialize(file_name):
    with open(file_name, 'r') as f:
        algorithm = f.readline().split('\n')[0]
        dimensions = f.readline().split('\n')[0].split(' ')
        dimensions = list(map(int, dimensions))
        entrance_input = f.readline().split('\n')[0].split(' ')
        entrance_input = list(map(int, entrance_input))
        exit_input = f.readline().split('\n')[0].split(' ')
        exit_input = list(map(int, exit_input))
        num = int(f.readline().split('\n')[0])
        grids = f.readlines()
        # print(algorithm)
        # print(dimensions)
        # print(entrance_input)
        # print(exit_input)
        # print(num)
        # print(grids)

    nodes = []
    nodes2id = {}
    for grid in grids:
        grid = grid.split('\n')[0].split(' ')
        grid = list(map(int, grid))
        nodes.append({'location': grid[0:3], 'actions': grid[3:]})
        nodes2id[','.join([str(x) for x in grid[0:3]])] = len(nodes) - 1
        # print(len(nodes) - 1, nodes[len(nodes) - 1])
        # print(','.join([str(x) for x in grid[0:3]]), nodes2id[','.join([str(x) for x in grid[0:3]])])
    # print(nodes)
    # print(nodes2id)

    if len(nodes) != num:
        return algorithm, dimensions, None, None, num, nodes, nodes2id, False

    if nodes2id.__contains__(','.join([str(x) for x in entrance_input])) and nodes2id.__contains__(','.join([str(x) for x in exit_input])):
        entrance = nodes2id[','.join([str(x) for x in entrance_input])]
        exit = nodes2id[','.join([str(x) for x in exit_input])]
        return algorithm, dimensions, entrance, exit, num, nodes, nodes2id, True
    else:
        return algorithm, dimensions, None, None, num, nodes, nodes2id, False

def decode_action(location, action):
    current_location = [location[0], location[1], location[2]]
    if action == 1:
        current_location[0] += 1
    elif action == 2:
        current_location[0] -= 1
    elif action == 3:
        current_location[1] += 1
    elif action == 4:
        current_location[1] -= 1
    elif action == 5:
        current_location[2] += 1
    elif action == 6:
        current_location[2] -= 1
    elif action == 7:
        current_location[0] += 1
        current_location[1] += 1
    elif action == 8:
        current_location[0] += 1
        current_location[1] -= 1
    elif action == 9:
        current_location[0] -= 1
        current_location[1] += 1
    elif action == 10:
        current_location[0] -= 1
        current_location[1] -= 1
    elif action == 11:
        current_location[0] += 1
        current_location[2] += 1
    elif action == 12:
        current_location[0] += 1
        current_location[2] -= 1
    elif action == 13:
        current_location[0] -= 1
        current_location[2] += 1
    elif action == 14:
        current_location[0] -= 1
        current_location[2] -= 1
    elif action == 15:
        current_location[1] += 1
        current_location[2] += 1
    elif action == 16:
        current_location[1] += 1
        current_location[2] -= 1
    elif action == 17:
        current_location[1] -= 1
        current_location[2] += 1
    elif action == 18:
        current_location[1] -= 1
        current_location[2] -= 1
    return current_location
    

def BFS(dimensions, entrance, exit, num, nodes, nodes2id):
    queue = [entrance]
    parents = [-1] * num
    visited = [False] * num
    while len(queue) > 0:
        node = queue.pop(0)
        visited[node] = True
        if node == exit:
            return parents
        for action in nodes[node]['actions']:
            current_location = decode_action(nodes[node]['location'], action)
            index = nodes2id[','.join([str(x) for x in current_location])]
            if not visited[index] and nodes[index]['location'][0] < dimensions[0] and nodes[index]['location'][1] < dimensions[1] and nodes[index]['location'][2] < dimensions[2]:
                queue.append(index)
                parents[index] = node
    return 'FAIL'

def UCS(dimensions, entrance, exit, num, nodes, nodes2id):
    queue = PriorityQueue()
    queue.put((0, entrance)) # item[0] is the cost from entrance to the current node, item[1] is the index of the current node
    traverse_info = [{'parent': -1, 'cost': 0}] * num # "cost" is the cost from the parent of the current node to it
    visited = [False] * num
    while not queue.empty():
        node = queue.get()
        visited[node[1]] = True
        if node[1] == exit:
            return traverse_info
        for action in nodes[node[1]]['actions']:
            current_location = decode_action(nodes[node[1]]['location'], action)
            index = nodes2id[','.join([str(x) for x in current_location])]
            if not visited[index] and nodes[index]['location'][0] < dimensions[0] and nodes[index]['location'][1] < dimensions[1] and nodes[index]['location'][2] < dimensions[2]:
                if action < 7:
                    cost = 10
                else:
                    cost = 14
                queue.put((node[0] + cost, index))
                traverse_info[index] = {'parent': node[1], 'cost': cost}
    return 'FAIL'

def heuristic(current):
    return pow(pow((nodes[exit]['location'][0] - nodes[current]['location'][0]) * 10, 2) + pow((nodes[exit]['location'][1] - nodes[current]['location'][1]) * 10, 2)+ pow((nodes[exit]['location'][2] - nodes[current]['location'][2]) * 10, 2), 0.5)

def A(dimensions, entrance, exit, num, nodes, nodes2id):
    queue = PriorityQueue()
    queue.put((heuristic(entrance), 0, entrance)) # item[0] is the total cost from entrance to exit through the current node, item[1] is the cost from entrance to the current node, item[2] is the index of the current node
    traverse_info = [{'parent': -1, 'cost': 0}] * num # "cost" is the cost from the parent of the current node to it
    visited = [False] * num
    while not queue.empty():
        node = queue.get()
        visited[node[2]] = True
        if node[2] == exit:
            return traverse_info
        for action in nodes[node[2]]['actions']:
            current_location = decode_action(nodes[node[2]]['location'], action)
            index = nodes2id[','.join([str(x) for x in current_location])]
            if not visited[index] and nodes[index]['location'][0] < dimensions[0] and nodes[index]['location'][1] < dimensions[1] and nodes[index]['location'][2] < dimensions[2]:
                if action < 7:
                    cost = 10
                else:
                    cost = 14
                queue.put((heuristic(index) + node[1] + cost, node[1] + cost, index))
                traverse_info[index] = {'parent': node[2], 'cost': cost}
    return 'FAIL'

if __name__ == "__main__":
    input_file_name = 'Grading Cases/input14.txt'
    output_file_name = 'output.txt'
    algorithm, dimensions, entrance, exit, num, nodes, nodes2id, result = initialize(input_file_name)
    if not result:
        print('Entrance or exit is not in accessible nodes list!')
        with open(output_file_name, 'w') as f:
            f.write('FAIL')
    elif algorithm == 'BFS':
        result = BFS(dimensions, entrance, exit, num, nodes, nodes2id)
        if result == 'FAIL':
            print('No solution was found!')
            with open(output_file_name, 'w') as f:
                f.write('FAIL')
        else:
            current_node = exit
            steps = []
            while current_node != entrance:
                steps.insert(0, current_node)
                current_node = result[current_node]
            with open(output_file_name, 'w') as f:
                f.write(str(len(steps)) + '\n')
                f.write(str(len(steps) + 1) + '\n')
                f.write(str(nodes[entrance]['location'][0]) + ' ' + str(nodes[entrance]['location'][1]) + ' ' + str(nodes[entrance]['location'][2]) + ' 0\n')
                for step in steps:
                    f.write(str(nodes[step]['location'][0]) + ' ' + str(nodes[step]['location'][1]) + ' ' + str(nodes[step]['location'][2]) + ' 1\n')
                print('Solution is printed!')
    elif algorithm == 'UCS':
        result = UCS(dimensions, entrance, exit, num, nodes, nodes2id)
        if result == 'FAIL':
            print('No solution was found!')
            with open(output_file_name, 'w') as f:
                f.write('FAIL')
        else:
            current_node = exit # index of each node
            steps = []
            total_cost = 0
            while current_node != entrance:
                steps.insert(0, (current_node, result[current_node]['cost']))
                total_cost += result[current_node]['cost']
                current_node = result[current_node]['parent']
            with open(output_file_name, 'w') as f:
                f.write(str(total_cost) + '\n')
                f.write(str(len(steps) + 1) + '\n')
                f.write(str(nodes[entrance]['location'][0]) + ' ' + str(nodes[entrance]['location'][1]) + ' ' + str(nodes[entrance]['location'][2]) + ' 0\n')
                for step in steps:
                    f.write(str(nodes[step[0]]['location'][0]) + ' ' + str(nodes[step[0]]['location'][1]) + ' ' + str(nodes[step[0]]['location'][2]) + ' ' + str(step[1]) + '\n')
                print('Solution is printed!')
    elif algorithm == 'A*':
        result = A(dimensions, entrance, exit, num, nodes, nodes2id)
        if result == 'FAIL':
            print('No solution was found!')
            with open(output_file_name, 'w') as f:
                f.write('FAIL')
        else:
            current_node = exit # index of each node
            steps = []
            total_cost = 0
            while current_node != entrance:
                steps.insert(0, (current_node, result[current_node]['cost']))
                total_cost += result[current_node]['cost']
                current_node = result[current_node]['parent']
            with open(output_file_name, 'w') as f:
                f.write(str(total_cost) + '\n')
                f.write(str(len(steps) + 1) + '\n')
                f.write(str(nodes[entrance]['location'][0]) + ' ' + str(nodes[entrance]['location'][1]) + ' ' + str(nodes[entrance]['location'][2]) + ' 0\n')
                for step in steps:
                    f.write(str(nodes[step[0]]['location'][0]) + ' ' + str(nodes[step[0]]['location'][1]) + ' ' + str(nodes[step[0]]['location'][2]) + ' ' + str(step[1]) + '\n')
                print('Solution is printed!')