class LiftPassager:
	def __init__(self, id_, current_floor, destiny_floor):
		self._id = id_
		self._lift = None
		self._current_floor = current_floor
		self._destiny_floor = destiny_floor

	def __repr__(self):
		return (f'{self.__class__.__name__}' + 
				f'({self._id}, {self._current_floor}, {self._destiny_floor})')

	def __eq__(self, other):
		if not isinstance(other, LiftPassager):
			return NotImplemented
		return self._id == other._id

	def __hash__(self):
		return hash((self._id,))

	@property
	def id(self):
		return self._id

	@property
	def destiny_floor(self):
		return self._destiny_floor

	@property
	def current_floor(self):
		if self._lift:
			self._current_floor = self._lift.current_floor
		return self._current_floor

	def enter_lift(self, lift):
		LiftPassager.raise_if_not_lift(lift)
		self._lift = lift
		self._lift.put_passager(self)

	def exit_lift(self):
		LiftPassager.raise_if_not_lift(self._lift)
		self.current_floor # atualizar andar atual
		self._lift.withdraw_passager(self)
		self._lift = None

	def is_on_lift(self):
		return bool(self._lift)

	def is_on_destiny_floor(self):
		return self.current_floor == self._destiny_floor

	@staticmethod
	def raise_if_not_lift(lift):
		if not isinstance(lift, BuildingLift):
			raise TypeError('Argument must be a BuildingLift.')


class BuildingLift:
	_ORDER_SUFFIX = {1: 'st', 2: 'nd', 3: 'rd'}
	_ORDER_DEFAULT_SUFFIX = 'th'

	def __init__(self, total_floors, current_floor=0):
		self._total_floors = total_floors
		self._passagers = []
		self._current_floor = current_floor

	def __repr__(self):
		return (f'{self.__class__.__name__}' + 
				f'({self._total_floors}, {self._current_floor})')

	@property
	def total_floors(self):
		return self._total_floors

	@property
	def current_floor(self):
		return self._current_floor

	@property
	def passagers(self):
		return list(self._passagers)
	
	def up(self, floors):
		if self._current_floor + floors > self._total_floors:
			raise ValueError('Lift can\'t go up more than the last floor.')
		self._current_floor += floors
		# print(f'The lift went up {floors} floor(s).')
		self.__print_current_floor()

	def down(self, floors):
		if self._current_floor - floors < 0:
			raise ValueError('Lift can\'t go down more than ground floor.')
		self._current_floor -= floors
		# print(f'The lift went down {floors} floor(s).')
		self.__print_current_floor()

	def put_passager(self, passager):
		BuildingLift.raise_if_not_passager(passager)
		self._passagers.append(passager)
		print('A passenger entered the lift.')

	def withdraw_passager(self, passager):
		BuildingLift.raise_if_not_passager(passager)
		if passager not in self._passagers:
			raise RuntimeError('Passager is not in the lift.')
		self._passagers.remove(passager)
		print('A passenger left the lift.')

	def __print_current_floor(self): 
		suffix = BuildingLift._ORDER_SUFFIX.get(
			self._current_floor, BuildingLift._ORDER_DEFAULT_SUFFIX
		)
		print(f'The lift is on {self._current_floor}{suffix} floor.')

	@staticmethod
	def raise_if_not_passager(passager):
		if not isinstance(passager, LiftPassager):
			raise TypeError('Argument must be a iterable of LiftPassager\'s.')
