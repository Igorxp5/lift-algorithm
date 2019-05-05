import heapq
from building_lift import BuildingLift, LiftPassager

def get_lift_graph(lift, passagers, passagers_by_floor, source_floor):
	floors = [f for f in range(lift.total_floors + 1) if passagers_by_floor[f]]
	added_floors = set((source_floor,))
	current_floor = source_floor
	path = [source_floor]
	while len(path) < len(floors) + 1:
		weights = {f: 0 for f in floors if f not in added_floors}
		# weights = [0 if f not in added_floors else None for f in floors]
		for f in floors:
			if f in weights and f is not current_floor:
				weights[f] = abs(f - current_floor)
			passagers = passagers_by_floor[f]
			for passager in passagers:
				pos_floors = sorted([f, current_floor, passager.destiny_floor])
				if pos_floors[0] is passager.destiny_floor:
					for g in range(current_floor, min(floors) - 1, -1):
						if g in weights:
							weights[g] += abs(f - passager.destiny_floor)
				elif pos_floors[2] is passager.destiny_floor:
					for g in range(current_floor, max(floors) + 1):
						if g in weights:
							weights[g] += abs(f - passager.destiny_floor)

		min_weight_floor = None
		for f in [g for g in floors if g in weights]:
			if min_weight_floor is None or weights[f] < weights[min_weight_floor]:
				min_weight_floor = f
		path.append(min_weight_floor)
		added_floors.add(min_weight_floor)
		current_floor = min_weight_floor

	print(path)
	exit()


	vertices = tuple(passagers + [lift])
	graph = []

	edge_count = 1
	for p in range(len(passagers)):
		for q in range(p + 1, len(passagers)):
			passager_p_floor = passager_floor(passagers[p])
			passager_q_floor = passager_floor(passagers[q])
			weight = abs(passager_p_floor - passager_q_floor)
			edge = weight, edge_count, (passagers[p], passagers[q])
			graph.append(edge)
			edge_count += 1

	for passager in passagers:
		weight = abs(lift.current_floor - passager_floor(passager))
		edge = weight, edge_count, (lift, passager)
		graph.append(edge)
		edge_count += 1

	return vertices, graph

def get_lowest_cost_graph_path(vertices, graph, source_vertice):
	heap_edges = graph.copy()
	heapq.heapify(heap_edges)
	total_connected_edges = 0

	final_graph = {v: [] for v in vertices}
	while heap_edges and total_connected_edges < len(vertices) - 1:
		weight, edge_count, edge_vertices = heapq.heappop(heap_edges)
		edge = weight, *edge_vertices
		valid_edge = True
		for vertice in  edge_vertices:
			conditions = (
				vertice is source_vertice and len(final_graph[vertice]) == 0,
				vertice is not source_vertice and len(final_graph[vertice]) < 2
			)
			valid_edge = valid_edge and any(conditions)
		if valid_edge:
			for vertice in edge_vertices:
				final_graph[vertice].append(edge)
			total_connected_edges += 1

	path = [source_vertice]
	while len(path) < len(vertices):
		current_vertice = path[-1]
		edge = final_graph[current_vertice][0]
		next_vertice = edge[1] if edge[1] is not current_vertice else edge[2]
		final_graph[next_vertice].remove(edge)
		path.append(next_vertice)
	
	return tuple(path)

def go_lift_by_path(lift, passagers_by_floor, path):
	for floor in path:
		distance_floors = floor - lift.current_floor
		move_lift = lift.up if distance_floors > 0 else lift.down
		distance_floors = abs(distance_floors)

		for _ in range(distance_floors):
			move_lift(1)
			for passager in passagers_by_floor[lift.current_floor]:
				if not passager.is_on_destiny_floor():
					passager.enter_lift(lift)
					print(f'Passager: {passager} entered the lift.')
					passagers_by_floor[lift.current_floor].remove(passager)

			for passager in lift.passagers:
				if passager.is_on_destiny_floor():
					passager.exit_lift()
					print(f'Passager: {passager} has reached his destination.')
					passagers_by_floor[lift.current_floor].append(passager)

def lift_algorithm(total_floors, current_lift_floor, passagers):
	lift = BuildingLift(total_floors, current_floor=current_lift_floor)
	passagers_by_floor = {f: [] for f in range(total_floors + 1)}
	for passager in passagers:
		passagers_by_floor[passager.current_floor].append(passager)

	# Pegar todos os passageiros
	vertices, graph = get_lift_graph(lift, passagers, passagers_by_floor, current_lift_floor)
	path = get_lowest_cost_graph_path(vertices, graph, lift)
	path = path[1:] # o primeiro é o andar em que se encontra o elevador
	path = [o.current_floor for o in path]

	go_lift_by_path(lift, passagers_by_floor, path)

	# Deixar todos os passageiros
	vertices, graph = get_lift_graph(lift, lift.passagers, lambda p: p.destiny_floor)
	path = get_lowest_cost_graph_path(vertices, graph, lift)
	path = path[1:] # o primeiro é o andar em que se encontra o elevador
	path = [o.destiny_floor for o in path]

	go_lift_by_path(lift, passagers_by_floor, path)

	# Fim do Algoritmo

	# Printar situação dos andares

	print('\n# Building Floors #')

	for floor in range(total_floors + 1):
		print(f'Floor {floor}: {passagers_by_floor[floor]}')