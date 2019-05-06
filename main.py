from building_lift import LiftPassager
from lift_algorithm import lift_algorithm

# 1ª Questão
print('##### 1ª Questão #####')

total_floors, current_lift_floor = 10, 5
# LiftPassager(id, current_floor, destiny_floor)
passagers = [LiftPassager(1, 8, 0), LiftPassager(2, 0, 10)]

print(f'\nTotal Floors: {total_floors}\n')
lift_algorithm(total_floors, current_lift_floor, passagers)


# 2ª Questão
print('\n##### 2ª Questão #####')

total_floors, current_lift_floor = 20, 3
# LiftPassager(id, current_floor, destiny_floor)
passagers = [LiftPassager(1, 8, 0), LiftPassager(2, 0, 7), LiftPassager(3, 3, 15)]

print(f'\nTotal Floors: {total_floors}\n')
lift_algorithm(total_floors, current_lift_floor, passagers)