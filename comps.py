from enum import IntEnum, auto, unique
from itertools import combinations, chain
import csv
from os import execlpe

NUM_TANKS = 4
NUM_HEALERS = 4
NUM_MELEES = 5
NUM_PHYSICAL_RANGE = 3
NUM_MAGICAL_RANGE = 4
FIELDS = ["T1", "T2", "H1", "H2", "M1", "M2", "R1", "R2", ]
FILENAME = "savage_comps"

@unique
class Class(IntEnum):
    TANK = 0
    HEALER = 1
    MELEE = 2
    PHYSICAL_RANGE = 3
    MAGICAL_RANGE = 4

@unique
class Job(IntEnum):
    PLD = 0
    WAR = auto()
    DRK = auto()
    GNB = auto()

    WHM = auto()
    SCH = auto()
    AST = auto()
    SGE = auto()

    MNK = auto()
    DRG = auto()
    NIN = auto()
    SAM = auto()
    RPR = auto()

    BRD = auto()
    MCH = auto()
    DNC = auto()

    BLM = auto()
    SMN = auto()
    RDM = auto()
    BLU = auto()

    @classmethod
    def job_groups_by_class(cls, class_int):
        assert 0 <= class_int <= 4

        groupings = [
            [cls.PLD, cls.WAR, cls.DRK, cls.GNB],
            [cls.WHM, cls.SCH, cls.AST, cls.SGE],
            [cls.MNK, cls.DRG, cls.NIN, cls.SAM, cls.RPR],
            [cls.BRD, cls.MCH, cls.DNC],
            [cls.BLM, cls.SMN, cls.RDM, cls.BLU],
            ]
        return groupings[class_int]

    @staticmethod
    def from_name(label):
        label = label.upper().strip()
        if label in ("PLD",):
            return Job.PLD
        elif label in ("WAR",):
            return Job.WAR
        elif label in ("DRK",):
            return Job.DRK
        elif label in ("GNB",):
            return Job.GNB

        elif label in ("WHM",):
            return Job.WHM
        elif label in ("SCH",):
            return Job.SCH
        elif label in ("AST",):
            return Job.AST
        elif label in ("SGE",):
            return Job.SGE

        elif label in ("MNK",):
            return Job.MNK
        elif label in ("DRG",):
            return Job.DRG
        elif label in ("NIN",):
            return Job.NIN
        elif label in ("SAM",):
            return Job.SAM
        elif label in ("RPR",):
            return Job.RPR

        elif label in ("BRD",):
            return Job.BRD
        elif label in ("MCH",):
            return Job.MCH
        elif label in ("DNC",):
            return Job.DNC

        elif label in ("BLM",):
            return Job.BLM
        elif label in ("SMN",):
            return Job.SMN
        elif label in ("RDM",):
            return Job.RDM
        elif label in ("BLU",):
            return Job.BLU
        else:
            raise NotImplementedError

POACHED = {
    "Celaena": {
        "primary": [
            Job.AST
            ],
        "secondary": [
            Job.WHM,
            Job.PLD
            ],
        "tertiary": [

            ]
        },
    "Leone": {
        "primary": [
            Job.GNB
            ],
        "secondary": [
            Job.DRG,
            ],
        "tertiary": [
            Job.RDM,
            Job.MNK,
            Job.NIN
            ]
        },
    "Prims": {
        "primary": [
            Job.SAM
            ],
        "secondary": [
            Job.PLD,
            Job.DRK
            ],
        "tertiary": [

            ]
        },
    "Arg": {
        "primary": [
            Job.DRK
            ],
        "secondary": [
            Job.SMN,
            Job.DRG,
            Job.DRK
            ],
        "tertiary": [

            ]
        },
    "Kat": {
        "primary": [
            Job.DNC
            ],
        "secondary": [
            Job.BRD,
            Job.WHM,
            Job.AST,
            Job.RDM
            ],
        "tertiary": [

            ]
        },
    "Lloyd": {
        "primary": [
            Job.DRG,
            # Job.RPR
            ],
        "secondary": [

            ],
        "tertiary": [

            ]
        },
    "Livia": {
        "primary": [
            Job.PLD,
            Job.DRK
            ],
        "secondary": [
            Job.DRG,
            Job.NIN,
            Job.DNC,
            Job.AST
            ],
        "tertiary": [

            ]
        },
    "Sonja": {
        "primary": [
            Job.PLD,
            Job.WAR,
            Job.DRK,
            Job.GNB,

            Job.MNK,
            Job.DRG,
            Job.NIN,
            Job.SAM,
            # Job.RPR,

            Job.BRD,
            Job.MCH,
            Job.DNC,

            Job.BLM,
            Job.SMN,
            Job.RDM,
            ],
        "secondary": [

            ],
        "tertiary": [

            ]
        },
    "Blyze": {
        "primary": [
            Job.PLD,

            Job.WHM,
            Job.SCH,
            Job.AST,

            Job.MNK,
            Job.NIN,
            Job.DRG,
            Job.SAM
            ],
        "secondary": [

            ],
        "tertiary": [

            ],
        }
    }

def primary_only():
    poached_aux = {}
    for name, roles in POACHED.items():
        poached_aux[name] = roles["primary"]

    return poached_aux

def no_pref():
    poached_aux = {}
    for name, roles in POACHED.items():
        roles_aux = []
        for roles_list in roles.values():
            roles_aux.extend(roles_list)
        poached_aux[name] = roles_aux

    return poached_aux

def bucket_method(pref_matters=False):
    by_class = [set(), set(), set(), set()]

    poached_aux = primary_only() if pref_matters else no_pref()

    # print(poached_aux)

    # creating class buckets and associating names to jobs
    for name, roles in poached_aux.items():
        for role in roles:
            # print(role.value)
            val = (name, role)
            if role.value in Job.job_groups_by_class(Class.TANK):
                by_class[Class.TANK].add(val)
            elif role.value in Job.job_groups_by_class(Class.HEALER):
                by_class[Class.HEALER].add(val)
            elif role.value in Job.job_groups_by_class(Class.MELEE):
                by_class[Class.MELEE].add(val)
            elif role.value in Job.job_groups_by_class(Class.PHYSICAL_RANGE) or role.value in Job.job_groups_by_class(
                    Class.MAGICAL_RANGE):
                by_class[3].add(val)

    four_to_two = [set(), set()]
    # t h m r -> t/h m/r
    for i, grouping in enumerate(by_class):
        combs = set(list(combinations(grouping, 2)))
        for comb in combs:
            names = {
                comb[0][0], comb[1][0],
                }
            jobs = {
                comb[0][1], comb[1][1],
                }
            # filter out combinations with duplicate names or duplicate jobs
            if len(names) == 2 and len(jobs) == 2:
                if i == 0 or i == 1:
                    four_to_two[0].add(comb)
                else:
                    four_to_two[1].add(comb)

    two_to_one = set()
    # t/h m/r -> t/h/m/r
    for grouping in four_to_two:
        combs = set(list(combinations(grouping, 2)))
        for comb in combs:
            names = {
                comb[0][0][0], comb[0][1][0],
                comb[1][0][0], comb[1][1][0]
                }
            jobs = {
                comb[0][0][1], comb[0][1][1],
                comb[1][0][1], comb[1][1][1]
                }
            # filter out combinations with duplicate names or duplicate jobs
            if len(names) == 4 and len(jobs) == 4:
                two_to_one.add(comb)

    csv_format = []
    # final combinations
    combs = set(list(combinations(two_to_one, 2)))
    for comb in combs:
        names = {
            comb[0][0][0][0], comb[0][0][1][0], comb[0][1][0][0], comb[0][1][1][0],
            comb[1][0][0][0], comb[1][0][1][0], comb[1][1][0][0], comb[1][1][1][0],
            }
        jobs = [
            comb[0][0][0][1], comb[0][0][1][1], comb[0][1][0][1], comb[0][1][1][1],
            comb[1][0][0][1], comb[1][0][1][1], comb[1][1][0][1], comb[1][1][1][1],
            ]
        # filter out combinations with duplicate names or duplicate jobs
        if len(names) == 8 and len(set(jobs)) == 8:
            jobs.sort()
            # Making sure the job complies with a 2-2-2-2
            if all(job in Job.job_groups_by_class(Class.TANK) for job in (jobs[0], jobs[1])) and \
                    all(job in Job.job_groups_by_class(Class.HEALER) for job in (jobs[2], jobs[3])) and \
                    all(job in Job.job_groups_by_class(Class.MELEE) for job in (jobs[4], jobs[5])) and \
                    all(job in Job.job_groups_by_class(Class.PHYSICAL_RANGE) + Job.job_groups_by_class(
                            Class.MAGICAL_RANGE) for job in (jobs[6], jobs[7])):

                # CSV formatting
                comp = list(chain.from_iterable((chain.from_iterable(comb))))
                comp.sort(key=lambda x: x[1])
                comp_abvr = [f"{name} {job.name}" for name, job in comp]
                csv_format.append(comp_abvr)

    filename = f"{FILENAME}_bucket_method_combined_prefs.csv"
    file_writer(filename, csv_format)

def file_writer(filename, csv_formatted_data):
    with open(filename, "w", newline="") as csvfile:
        print("Starting file write...")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(FIELDS)
        csvwriter.writerows(csv_formatted_data)

        print("File writing finished...")

CELL_PAD_AT_LEAST = 2
NUM_COLS = 8

def get_table_delims(data):
    longest = 0
    for cell in data:
        if len(cell) > longest:
            longest = len(cell)

    cell_max_width = longest + CELL_PAD_AT_LEAST * 2

    row_delim = f"|{('_' * cell_max_width + '|') * NUM_COLS}"

    row_zero_upper = f" {('_' * cell_max_width + '_') * NUM_COLS}"[:-1]

    return row_delim, cell_max_width, row_zero_upper

def left_right_padding(cell_max_width, cell):
    space_left = cell_max_width - len(cell)
    left = right = space_left // 2
    if space_left % 2 == 1:
        left += 1
    return left, right

def tablify(csv_reader, length=""):
    table_str = ""
    data_aux = csv_reader
    if len(data_aux) > 8 and length != "d":
        data_aux = data_aux[:4] + [["..."] * NUM_COLS] + data_aux[-3:]
    flat_data = set(chain.from_iterable(data_aux))
    row_delim, cell_max_width, row_zero_upper = get_table_delims(flat_data)

    for i, row in enumerate(data_aux):
        if i == 0:
            new_row_upper = f" {('_' * cell_max_width) * NUM_COLS + '_' * (NUM_COLS - 1)} "
        else:
            new_row_upper = f"{'|' + (' ' * cell_max_width + '|') * NUM_COLS}"

        new_row_mid = "|"

        for j, val in enumerate(row):

            cell = str(val).strip()
            left, right = left_right_padding(cell_max_width, cell)
            cell_content = f"{' ' * left + cell + ' ' * right}|"
            new_row_mid += cell_content

        new_row = new_row_upper + '\n' + new_row_mid + '\n' + row_delim
        if i != len(data_aux) - 1:
            new_row += '\n'
        table_str += new_row

    print(table_str)

def viewing_size_menu(data):
    keep_going = True
    while keep_going:
        print("Compact and Detailed Table? (C)/d")
        print(">>>", end=" ")
        length = input()

        if length.lower().strip() not in ["", "c", "d"]:
            print("That is not a valid option. Please try again.")
            continue

        tablify(data, length)
        break

def filter_data_menu(data):
    players_filter_params = set()
    jobs_filter_params = set()
    keep_going = True
    while keep_going:
        # filter_parameters = {
        #     "Players": players_filter_params,
        #     "Jobs": jobs_filter_params
        #     }
        # print("Current Filter Parameters")
        # for filter_type, parameters in filter_parameters.items():
        #     print(filter_type)
        #     for i, param in enumerate(parameters):
        #         print(f"{'Blacklist' if i == BLACKLIST else 'Whitelist'}:", end=" ")
        #         print(f"{param if param else 'None'}")

        print("""How would you like to filter this table? 
\t1) Player(s)
\t2) Job(s)
\t3) Exit""")
        print(">>>", end=" ")
        try:
            choice = int(input().strip())
            if choice not in range(1, 4):
                print("That is not a valid option. Please try again.")
                continue
            keep_going = choice != 3
            if keep_going:
                if keep_going == 1:
                    blacklist = player_filter_menu()
                else:
                    ...
            else:
                print("Exiting App")
        except ValueError as _:
            print("That is not an integer!. Please try again.")

def player_filter_menu():
    players_filter_params = (set(), set())
    print("Players you can filter by:")
    for i, name in enumerate(POACHED, 1):
        print(f"\t{i}) {name}")
        if i == len(POACHED):
            print(f"\t{i + 1}) Exit")
    keep_going = True
    while keep_going:

        print("Pressing enter will also exit.")
        # print(">>>", end=" ")
        # filter_me = input()
        # filter_me_aux = filter_me.split()
        # print(filter_me)
        # print(filter_me_aux)
        # try:
        #     filter_name = int(filter_me_aux[0].strip())
        #     if not filter_name in range(1, len(POACHED) + 1):
        #         print("That number isn't in a valid range.")
        #         continue
        #     if len(filter_me_aux) == 1:
        #         if filter_name == len(POACHED) + 1 or filter_me_aux[0].strip() == "":
        #             return players_filter_params
        #         else:
        #             filter_type = int(filter_me_aux[1].strip())
        #             if filter_type != 0 or filter_type != 1:
        #                 print("There is something wrong with the query for black or white listing.")
        #                 continue
        #             players_filter_params[BLACKLIST].add(list(POACHED.keys())[filter_name - 1])
        #
        # except ValueError as _:
        #     print("That is not an integer!. Please try again.")
        # print(players_filter_params)
        # print(filter_name)

        # if filter_name not in list(POACHED.keys()):
        #     print("That name isn't in the group of available people to filter.")
        #     continue 
        # filter_type = filter_me_aux[-1].strip()
        # try:
        #     filter_type = int(filter_type)
        #     if filter_type != 0 or filter_type != 1:
        #         print(
        #             "There is something wrong with the query for black or white listing.")
        #         continue
        # except ValueError as _:
        #     print("That is not an integer!. Please try again.")

        # print(filter_name, filter_type)
        # players_filter_params[filter_type].add(filter_name)
    return players_filter_params

def job_filter_menu(data, jobs_filter_params):
    print("Jobs  you can filter by:")

BLACKLIST = 0
WHITELIST = 1

def run_filter(data, filter_parameters):
    keep = []
    player_filter_type = filter_parameters["Players"][0]
    player_filters = filter_parameters["Players"][1]
    job_filter_type = filter_parameters["Jobs"][0]
    job_filters = filter_parameters["Jobs"][1]
    for comp in data[1:]:
        # print(comp)

        score = 0
        names = []
        jobs = []
        for val in comp:
            name = val[:-3].strip()
            names.append(name)
            job = val[-3:].strip()
            jobs.append(job)
            # print(name, job)
            if name in player_filters:
                if player_filter_type == BLACKLIST:
                    score -= 1
                else:
                    score += 1
            if job in job_filters:
                if job_filter_type == BLACKLIST:
                    score -= 1
                else:
                    score += 1

        if player_filter_type == WHITELIST:
            is_subset = player_filters.issubset(set(names))
            if not is_subset:
                score -= len(player_filters)
        if job_filter_type == WHITELIST:
            is_subset = job_filters.issubset(set(jobs))
            if not is_subset:
                score -= len(job_filters)

        # print(score)
        if score >= 0:
            keep.append(comp)

        # print(keep)
        # input()
    keep = data[:1] + keep
    # print(keep)
    tablify(keep, length="d")
    print(len(keep) - 1)

MENU = [viewing_size_menu, filter_data_menu]

def main_menu(comps):
    keep_going = True
    while keep_going:
        print("""\nOptions:
\t1) Change Viewing Size
\t2) Filter
\t3) Exit""")
        print(">>>", end=" ")
        try:
            choice = int(input().strip())
            if choice not in range(1, 4):
                print("That is not a valid option. Please try again.")
                continue
            keep_going = choice != 3
            if keep_going:
                MENU[choice - 1](comps)
            else:
                print("Exiting App")
        except ValueError as _:
            print("That is not an integer!. Please try again.")

if __name__ == "__main__":
    print("Updating CSV...")
    bucket_method()
    print("Updating Complete...")
    filename = f"{FILENAME}_bucket_method_combined_prefs.csv"
    with open(filename, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        comps = list(csv_reader)
        viewing_size_menu(comps)
    # # main_menu(comps)
    # filter_parameters = {
    #     "Players": [None, {}],
    #     "Jobs": [None, {}],
    #     # "Favouritism" : T/F # T will choose Jobs over Players and vice versa
    #     }
    # run_filter(comps, filter_parameters)
