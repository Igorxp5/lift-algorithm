import heapq
from building_lift import BuildingLift, LiftPassager


def go_lift(lift, passagers, passagers_by_floor, current_lift_floor):
	current_floor = current_lift_floor
	arrived_passagers = set()

	destinations = []
	total_destiny_floors = []
	for f in range(lift.total_floors + 1):
		destinations.append(bool(passagers_by_floor[f]))
		total_destiny_floors.append(0)

	for passager in passagers:
		total_destiny_floors[passager.destiny_floor] += 1

	destinations[current_floor] = False
	while len(arrived_passagers) < len(passagers):
		for passager in passagers_by_floor[current_floor]:
			if not passager.is_on_destiny_floor():
				passager.enter_lift(lift)
				passagers_by_floor[current_floor].remove(passager)
				destinations[passager.destiny_floor] = True
				print(f'Passager: {passager} entered the lift.')

		for passager in lift.passagers:
			if passager.is_on_destiny_floor():
				passager.exit_lift()
				arrived_passagers.add(passager)
				passagers_by_floor[current_floor].append(passager)
				print(f'Passager: {passager} has reached his destination.')

		# Remover destinos com passageiros somente à entregar,
		# que não estão com todos os seus passageiros no elevador.
		current_destiny_floors = [0] * (lift.total_floors + 1)
		for passager in lift.passagers:
			current_destiny_floors[passager.destiny_floor] += 1
		for f in range(lift.total_floors + 1):
			total_destiny = current_destiny_floors[f]
			if total_destiny > 0:
				destinations[f] = total_destiny_floors[f] == total_destiny
		
		up_weight = 0
		down_weight = 0
		for f in range(lift.total_floors + 1):
			if destinations[f]:
				dist = abs(current_floor - f)
				if f > current_floor and (not up_weight or dist < up_weight):
					up_weight = dist
				elif (
					f < current_floor
					and (not down_weight or dist < down_weight)
				):
					down_weight = dist

		worst_up_weight = 0
		worst_down_weight = 0
		for p in passagers:
			if p not in arrived_passagers:
				if (
					p.current_floor > current_floor 
					and p.destiny_floor < current_floor
				): 
					weight = abs(current_floor - p.current_floor)
					weight += abs(p.current_floor - p.destiny_floor)
					if weight > worst_down_weight:
						worst_down_weight = weight
				elif (
					p.current_floor < current_floor
					and p.destiny_floor > current_floor
				):
					weight = abs(current_floor - p.current_floor)
					weight += abs(p.current_floor - p.destiny_floor)
					if weight > worst_up_weight:
						worst_up_weight = weight
		up_weight += worst_up_weight
		down_weight += worst_down_weight

		move_lift_direction = None
		distance = 0
		if down_weight == up_weight:
			up_pointer = current_floor + 1
			down_pointer = current_floor - 1
			while (
				distance == 0 
				and (down_pointer >= 0 or up_pointer <= lift.total_floors)
			):
				if down_pointer >= 0 and destinations[down_pointer]:
					move_lift_direction = lift.down
					distance = current_floor - down_pointer
				elif (
					up_pointer <= lift.total_floors 
					and destinations[up_pointer]
				):
					move_lift_direction = lift.up
					distance = up_pointer - current_floor
				down_pointer -= 1
				up_pointer += 1

		elif down_weight == 0 or (up_weight != 0 and down_weight > up_weight):
			move_lift_direction = lift.up
			for f in range(current_floor + 1, lift.total_floors + 1):
				if destinations[f]:
					distance = f - current_floor
					break
		else:
			move_lift_direction = lift.down
			for f in range(current_floor - 1, -1, -1):
				if destinations[f]:
					distance = current_floor - f
					break
		
		# No último laço não há movimentos, 
		# somente deixadas de pessoas no andar atual.
		if distance > 0:
			move_lift_direction(distance)

		current_floor = lift.current_floor
		destinations[current_floor] = False


def lift_algorithm(total_floors, current_lift_floor, passagers):
	# Checar se todos os passageiros possuem ID's diferentes
	raise_if_not_passagers_different_ids(passagers)

	lift = BuildingLift(total_floors, current_floor=current_lift_floor)
	passagers_by_floor = {f: [] for f in range(total_floors + 1)}
	for passager in passagers:
		passagers_by_floor[passager.current_floor].append(passager)

	go_lift(lift, passagers, passagers_by_floor, current_lift_floor)

	# Printar situação dos andares

	print('\n# Building Floors #')

	for floor in range(total_floors + 1):
		print(f'Floor {floor}: {passagers_by_floor[floor]}')


def raise_if_not_passagers_different_ids(passagers):
	ids = set()
	for passager in passagers:
		if passager.id in ids:
			raise RuntimeError('LiftPassager\'s with same id.')
		ids.add(passager.id)
