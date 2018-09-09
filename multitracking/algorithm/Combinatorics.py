V_DIRECTION = 'v'
U_DIRECTION = 'u'

###########################
# FITTING AND FISHING RPS #
###########################
def rp_with_max_combination(rp_combinations):
    return max(rp_combinations, key=lambda x :rp_combinations[x])


def rp_with_min_combination(rp_combinations):
    return min(rp_combinations, key=lambda x :rp_combinations[x])


def get_fitting_rps(rp_combinations):
    fitting_rps = list(rp_combinations)

    min_combi_rp = rp_with_min_combination(rp_combinations)
    max_combi_rp = rp_with_max_combination(rp_combinations)

    fitting_rps.remove(min_combi_rp)
    fitting_rps.remove(max_combi_rp)

    fitting_rps = [min_combi_rp] + fitting_rps

    return fitting_rps


def get_fishing_fitting_rps(multi_lines_dict):
    rp_combinations = {}
    '''
    EXAMPLE: rp_combinations: {105: 6, 125: 4, 121: 20}
    '''
    for rp_id in multi_lines_dict:
        rp_combinations[rp_id] = len(multi_lines_dict[rp_id][U_DIRECTION]) * len(multi_lines_dict[rp_id][V_DIRECTION])

    fishing_rp = rp_with_max_combination(rp_combinations)
    fitting_rps = get_fitting_rps(rp_combinations)

    return fishing_rp, fitting_rps


###########################
# FITTING AND FISHING RPS #
###########################
def generate_rp_combinations(rp_id, multi_lines_dict):
    combinations = []

    u_lines_numbers = list(multi_lines_dict[rp_id][U_DIRECTION])
    v_lines_numbers = list(multi_lines_dict[rp_id][V_DIRECTION])

    for u_idx in u_lines_numbers:
        for v_idx in v_lines_numbers:
            u_tuple = (rp_id, U_DIRECTION, u_idx)
            v_tuple = (rp_id, V_DIRECTION, v_idx)
            combinations.append([u_tuple, v_tuple])

    return combinations


def merge_combinations(rps_combinations):
    if len(rps_combinations) == 1:
        return rps_combinations[0]

    a_combinations = rps_combinations[0]
    b_combinations = merge_combinations(rps_combinations[1:])

    merged_combinations = []
    for a_combination in a_combinations:
        for b_combination in b_combinations:
            merged_combination = []
            for a_tuple in a_combination:
                merged_combination.append(a_tuple)
            for b_tuple in b_combination:
                merged_combination.append(b_tuple)
            merged_combinations.append(merged_combination)

    return merged_combinations


def get_combinations(fitting_rps, multi_lines_dict):
    '''
    :return:
    Example

        rp_combinations: {105: 4, 125: 4, 121: 16}
        fitting_rps: [125, 105]

        125: 2 x u_lines, 2 x v_lines
        105: 2 x u_lines, 2 x v_lines

        [(105, 'u', 0), (105, 'v', 0), (125, 'u', 0), (125, 'v', 0)]
        [(105, 'u', 0), (105, 'v', 0), (125, 'u', 0), (125, 'v', 1)]
        [(105, 'u', 0), (105, 'v', 0), (125, 'u', 1), (125, 'v', 0)]
        [(105, 'u', 0), (105, 'v', 0), (125, 'u', 1), (125, 'v', 1)]
        [(105, 'u', 0), (105, 'v', 1), (125, 'u', 0), (125, 'v', 0)]
        [(105, 'u', 0), (105, 'v', 1), (125, 'u', 0), (125, 'v', 1)]
        [(105, 'u', 0), (105, 'v', 1), (125, 'u', 1), (125, 'v', 0)]
        [(105, 'u', 0), (105, 'v', 1), (125, 'u', 1), (125, 'v', 1)]
        [(105, 'u', 1), (105, 'v', 0), (125, 'u', 0), (125, 'v', 0)]
        [(105, 'u', 1), (105, 'v', 0), (125, 'u', 0), (125, 'v', 1)]
        [(105, 'u', 1), (105, 'v', 0), (125, 'u', 1), (125, 'v', 0)]
        [(105, 'u', 1), (105, 'v', 0), (125, 'u', 1), (125, 'v', 1)]
        [(105, 'u', 1), (105, 'v', 1), (125, 'u', 0), (125, 'v', 0)]
        [(105, 'u', 1), (105, 'v', 1), (125, 'u', 0), (125, 'v', 1)]
        [(105, 'u', 1), (105, 'v', 1), (125, 'u', 1), (125, 'v', 0)]
        [(105, 'u', 1), (105, 'v', 1), (125, 'u', 1), (125, 'v', 1)]

        Note that 125 with min number of combinations is in first two columns

    '''

    rps_combinations = []
    for fit_rp_id in fitting_rps:
        rp_combinations = generate_rp_combinations(fit_rp_id, multi_lines_dict)
        rps_combinations.append(rp_combinations)

        for rp_combination in rp_combinations:
            print(rp_combination)

    return merge_combinations(rps_combinations)