# instruction : number of params
INSTRUCTIONS = {1 : 3, 2 : 3, 3 : 1, 4 : 1, 5 : 2, 6 : 2, 7 : 3, 8 : 3, 99 : 0}

STD_OUT = []

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
def execute_instruction(opcode, modes, params, program, prg_input, save_stdout=False):
    # input checks
    assert opcode in INSTRUCTIONS
    assert len(modes) == INSTRUCTIONS[opcode]
    assert len(params) == INSTRUCTIONS[opcode]
    assert program
    
    def eval_param(i):
        assert i < len(params) and i < len(modes)
        return program[params[i]] if modes[len(modes) - 1 - i] == 0 else params[i] 

    if opcode == 99: # HALT
        return -1, None
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
        if prg_input is None:
            program[params[0]] = int(input())
        else:
            program[params[0]] = prg_input.pop(0)
    elif opcode == 4: # WRITE
        assert len(modes) == 1
        if modes[0] == 0:
            assert params[0] < len(program)
            if save_stdout:
                STD_OUT.append(program[params[0]])
            else:
                print(program[params[0]])
        elif modes[0] == 1:
            if save_stdout:
                STD_OUT.append(params[0])
            else:
                print(params[0])
        else:
            assert False
    elif opcode == 5: # JMP if TRUE
        check = eval_param(0)
        ipset = eval_param(1)
        if check != 0:
            return -2, ipset
    elif opcode == 6: # JMP if FALSE
        check = eval_param(0)
        ipset = eval_param(1)
        if check == 0:
            return -2, ipset
    elif opcode == 7: # LESS THAN
        op1 = eval_param(0)
        op2 = eval_param(1)
        dest = params[2]
        program[dest] = 1 if op1 < op2 else 0
    elif opcode == 8: # EQUALS
        op1 = eval_param(0)
        op2 = eval_param(1)
        dest = params[2]
        program[dest] = 1 if op1 == op2 else 0
    else:
        assert False
        return -1, None

    return INSTRUCTIONS[opcode] + 1, None

def next_instruction(ip, program, prg_input, save_stdout):
    opcode, modes = get_opcode(program[ip])
    params = program[ip+1:ip+INSTRUCTIONS[opcode]+1]
    assert len(params) == INSTRUCTIONS[opcode]
    ip_shift, ip_jmp = execute_instruction(opcode, modes, params, program, prg_input, save_stdout=save_stdout)
    if ip_shift == -1:
        return -1
    elif ip_shift == -2:
        return ip_jmp
    else:
        return ip + ip_shift


def run_prg(prg, prg_input=None, save_stdout=False):
    """
    >>> run_prg("1,9,10,3,2,3,11,0,99,30,40,50")
    3500
    >>> run_prg("1,0,0,0,99")
    2
    >>> run_prg("1,1,1,4,99,5,6,0,99")
    30
    >>> run_prg("3,0,4,0,99", [123])
    123
    123
    """
    assert prg
    prg = prg.split(',')
    prg = [int(x) for x in prg]

    ip = 0
    while True:
        # print("Execute at:", ip)
        ip = next_instruction(ip, prg, prg_input, save_stdout)
        if ip == -1:
            return prg[0]

def main():
    with open('input') as f:
        prg_bck = f.readline()
        prg = prg_bck

        import itertools
        sequences = list(itertools.permutations([0,1,2,3,4]))

        result_max = -1
        result_code = []

        for seq in sequences:
            retval = 0

            for device in range(0,5):
                prg = prg_bck
                run_prg(prg, [seq[device], retval], save_stdout=True)
                assert len(STD_OUT) == 1
                retval = STD_OUT.pop(0)

            if retval > result_max:
                result_code = seq
            result_max = max(retval, result_max)

        print("Final:", result_max, "codes:", result_code)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()

