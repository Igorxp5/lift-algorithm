__author__ = 'Igor Fernandes'
__version__ = '0.0.0'

from building_lift import BuildingLift, LiftPassager


def get_best_path(lift, passagers, current_lift_floor):
	"""Retorna o melhor caminho a ser seguido por um elevador
	para obter a menor distância entre saltos possíveis. 
	"""
	def get_solution_leaps(solution):
		"""Retorna quantidade de saltos de um caminho."""
		solution_leaps = 0
		for i in range(1, len(solution)):
			solution_leaps += abs(solution[i - 1] - solution[i])
		return solution_leaps

	def compare_solution(solution1, solution2):
		"""Compara dois caminhos e retorna o melhor entre os dois,
		ou seja, o que possuir o menor somatório da distância
		entre os saltos.
		"""
		solution1_leaps = get_solution_leaps(solution1)
		solution2_leaps = get_solution_leaps(solution2)

		if solution2_leaps < solution1_leaps:
			return solution2
		return solution1

	def next_up_destiny(destinations, current_floor):
		"""Retorna o andar do destino mais próximo 
		do andar atual no sentido para cima.
		"""
		for f in range(current_floor + 1, len(destinations)):
			if destinations[f]:
				return f

	def next_down_destiny(destinations, current_floor):
		"""Retorna o andar do destino mais próximo 
		do andar atual no sentido para baixo.
		"""
		for f in range(current_floor - 1, -1, -1):
			if destinations[f]:
				return f

	def best_solution_recursive(passagers, lift_passagers, arrived_passagers, 
								current_floor, total_floors):
		"""
		A retorna a melhor solução dado: os passageiros participantes 
		do problema, os passageiros atuais do elevador, os passageiros 
		que já chegaram ao seu destino e a posição do elevador.
		"""
		if len(arrived_passagers) == len(passagers):
			return []
		else:
			# O vetor 'destinations' determina todos os andares que
			# o elevador deve passar. Seguindo os seguintes critérios:
			# - Andar dos passageiros que ainda estão esperando pelo elevador
			# - Andar dos que os passageiros que estão no elevador querem ir  
			destinations = [False] * (total_floors + 1)
			c_lift_passagers = lift_passagers.copy()
			c_arrived_passagers = arrived_passagers.copy()
			for passager in passagers:
				if passager not in c_arrived_passagers:
					if passager.current_floor is current_floor:
						c_lift_passagers.add(passager)
					if (
						passager in c_lift_passagers 
						and passager.destiny_floor is current_floor
					):
						c_lift_passagers.remove(passager)
						c_arrived_passagers.add(passager)

			for passager in passagers:
				if passager not in c_arrived_passagers:
					if passager not in c_lift_passagers:
						destinations[passager.current_floor] = True
					else:
						destinations[passager.destiny_floor] = True

			# É comparado duas soluções e retornado a melhor entre elas.
			# Uma solução que usa como próximo destino, o próximo
			# andar acima do elevador que foi marcado como destino.
			# A outra solução é considerando como destino um andar 
			# abaixo do elevador que foi marcado como destino. 
			next_up_floor = next_up_destiny(destinations, current_floor)
			next_down_floor = next_down_destiny(destinations, current_floor)

			if next_up_floor is None and next_down_floor is None:
				return []

			solution_up = None
			if next_up_floor is not None:
				solution_up = [next_up_floor]
				solution_up += best_solution_recursive(
					passagers, c_lift_passagers, c_arrived_passagers, 
					next_up_floor, total_floors
				)

			solution_down = None
			if next_down_floor is not None:
				solution_down = [next_down_floor]
				solution_down += best_solution_recursive(
					passagers, c_lift_passagers, c_arrived_passagers, 
					next_down_floor, total_floors
				)

			if not solution_down:
				return solution_up
			if not solution_up:
				return solution_down

			return compare_solution(solution_up, solution_down)

	arrived_passagers = set()
	lift_passagers = set(lift.passagers)
	return [current_lift_floor] + best_solution_recursive(
		passagers, lift_passagers, arrived_passagers,
		current_lift_floor, lift.total_floors
	)


def go_lift_by_path(lift, passagers_by_floor, path):
	"""Desenvolve os movimentos do elevador baseado no caminho passado."""
	for floor in path:
		distance_floors = floor - lift.current_floor
		move_lift = lift.up if distance_floors > 0 else lift.down
		distance_floors = abs(distance_floors)

		move_lift(distance_floors)
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
	"""Executa o algortimo de menor tempo de movimento para 
	o elevador levar ao destino todos os passageiros, e mostra
	como resposta a estado final dos andares do edifício.
	"""

	# Checar se todos os passageiros possuem ID's diferentes
	raise_if_not_passagers_different_ids(passagers)

	lift = BuildingLift(total_floors, current_floor=current_lift_floor)
	passagers_by_floor = {f: [] for f in range(total_floors + 1)}
	for passager in passagers:
		passagers_by_floor[passager.current_floor].append(passager)

	path = get_best_path(lift, passagers, current_lift_floor)
	go_lift_by_path(lift, passagers_by_floor, path)	

	# Printar situação dos andares

	print('\n# Building Floors #')

	for floor in range(total_floors + 1):
		print(f'Floor {floor}: {passagers_by_floor[floor]}')


def raise_if_not_passagers_different_ids(passagers):
	"""Lança exceção caso haja passageiros com ID semelhantes."""
	ids = set()
	for passager in passagers:
		if passager.id in ids:
			raise RuntimeError('LiftPassager\'s with same id.')
		ids.add(passager.id)
