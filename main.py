from building_lift import LiftPassager
from lift_algorithm import lift_algorithm

# print('\n##### 2ª Questão #####')

# total_floors, current_lift_floor = 5, 2
# # LiftPassager(id, current_floor, destiny_floor)
# passagers = [LiftPassager(1, 5, 1), LiftPassager(2, 4, 2), LiftPassager(3, 1, 0), LiftPassager(4, 0, 3)]

# print(f'\nTotal Floors: {total_floors}')
# print(f'Current Lift Floor: {current_lift_floor}\n')
# lift_algorithm(total_floors, current_lift_floor, passagers)


# print('\n##### 2ª Questão #####')


# total_floors, current_lift_floor = 10, 4
# # LiftPassager(id, current_floor, destiny_floor)
# passagers = [
# 	LiftPassager(1, 9, 7), LiftPassager(2, 8, 10), LiftPassager(3, 6, 5),
# 	LiftPassager(4, 3, 7), LiftPassager(5, 2, 0)
# ]
 
# print(f'\nTotal Floors: {total_floors}')
# print(f'Current Lift Floor: {current_lift_floor}\n')
# lift_algorithm(total_floors, current_lift_floor, passagers)


# 1ª Questão
print('##### 1ª Questão #####')

total_floors, current_lift_floor = 10, 5
# LiftPassager(id, current_floor, destiny_floor)
passagers = [LiftPassager(1, 8, 0), LiftPassager(2, 0, 10)]

print(f'\nTotal Floors: {total_floors}')
print(f'Current Lift Floor: {current_lift_floor}\n')
lift_algorithm(total_floors, current_lift_floor, passagers)


# 2ª Questão
# print('\n##### 2ª Questão #####')

# total_floors, current_lift_floor = 20, 3
# # LiftPassager(id, current_floor, destiny_floor)
# passagers = [LiftPassager(1, 8, 0), LiftPassager(2, 0, 7), LiftPassager(3, 3, 15)]

# print(f'\nTotal Floors: {total_floors}')
# print(f'Current Lift Floor: {current_lift_floor}\n')
# lift_algorithm(total_floors, current_lift_floor, passagers)