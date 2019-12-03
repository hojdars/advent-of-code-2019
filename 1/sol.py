import math

def op(mass):
    return (math.floor(mass / 3) - 2)

def fuel_iterate(mass):
    result_sum = 0
    to_add = op(mass)
    while to_add > 0:
        result_sum += to_add
        to_add = op(to_add)
    return result_sum

def calc_fuel(mass):
    primary_fuel = op(mass)
    to_add = fuel_iterate(primary_fuel)
    return primary_fuel + to_add

def main():
    with open('input.txt') as f:
        modules = [int(x) for x in f]
        fuel = map(calc_fuel, modules)
        return sum(fuel)


if __name__ == "__main__":
    print(calc_fuel(12))
    print(calc_fuel(14))
    print(calc_fuel(1969))
    print(calc_fuel(100756))
    print("Main:", main())