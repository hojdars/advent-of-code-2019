# instruction : number of params
INSTRUCTIONS = {1 : 3, 2 : 3, 3 : 1, 4 : 1, 99 : 0}

def get_opcode(intcode):
    """ Convert intcode in memory into opcode.
    >>> get_opcode(1002)
    (2, [0, 1, 0])
    >>> get_opcode(99)
    (99, [])
    >>> get_opcode(103)
    (3, [1])
    >>> get_opcode(104)
    (4, [1])
    >>> get_opcode(4)
    (4, [0])
    """
    
    digits = [x for x in str(intcode)]
    assert digits # we have a valid intcode
    
    # The last two digits are the opcode, if they exist
    opcode = None
    if len(digits) == 1:
        opcode = int(digits[0])
    else:
        opcode = 10*int(digits[-2]) + int(digits[-1])
    assert opcode # opcode exists
    assert opcode in INSTRUCTIONS # opcode is known

    modes = [int(x) for x in digits[:-2]] # modes are all digits before last two
    prefix_missing = INSTRUCTIONS[opcode] - len(modes)
    modes = [0] * prefix_missing + modes
    assert len(modes) == INSTRUCTIONS[opcode] # modes are for all parameters

    return opcode, modes


# Params: opcode is int, modes is [int], params is [int]
# Return: number to increase IP by.
def execute_instruction(opcode, modes, params, program):
    # input checks
    assert opcode in INSTRUCTIONS
    assert len(modes) == INSTRUCTIONS[opcode]
    assert len(params) == INSTRUCTIONS[opcode]
    assert program
    
    def eval_param(i):
        assert i < len(params) and i < len(modes)
        return program[params[i]] if modes[len(modes) - 1 - i] == 0 else params[i] 

    if opcode == 99: # HALT
        return -1
    elif opcode == 1: # ADD
        op1 = eval_param(0)
        op2 = eval_param(1)
        dest = params[2]
        program[dest] = op1 + op2
    elif opcode == 2: # MUL
        op1 = eval_param(0)
        op2 = eval_param(1)
        dest = params[2]
        program[dest] = op1 * op2
    elif opcode == 3: # READ
        assert params[0] < len(program)
        program[params[0]] = int(input())
    elif opcode == 4: # WRITE
        assert params[0] < len(program)
        assert len(modes) == 1
        if modes[0] == 0:
            print(program[params[0]])
        elif modes[0] == 1:
            print(params[0])
        else:
            assert False
    else:
        assert False
        return -1

    return INSTRUCTIONS[opcode] + 1

def next_instruction(ip, program):
    opcode, modes = get_opcode(program[ip])
    params = program[ip+1:ip+INSTRUCTIONS[opcode]+1]
    assert len(params) == INSTRUCTIONS[opcode]
    ip_shift = execute_instruction(opcode, modes, params, program)
    if ip_shift == -1:
        return -1
    else:
        return ip + ip_shift


def run_prg(prg):
    """
    >>> run_prg("1,9,10,3,2,3,11,0,99,30,40,50")
    3500
    >>> run_prg("1,0,0,0,99")
    2
    >>> run_prg("1,1,1,4,99,5,6,0,99")
    30
    """
    assert prg
    prg = prg.split(',')
    prg = [int(x) for x in prg]

    ip = 0
    while True:
        # print("Execute at:", ip)
        ip = next_instruction(ip, prg)
        if ip == -1:
            return prg[0]

def main():
    with open('input') as f:
        prg = f.readline()
        run_prg(prg)

if __name__ == "__main__":
    run_prg("1002,4,3,4,33")
    # run_prg("3,0,4,0,99") # manual test for INPUT and OUTPUT

    # import doctest
    # doctest.testmod()
    print("--------------")
    main()

