import random
import datetime
from typing import List, Dict

PositionsList = List[List[int]]
EmployeesNameList = List[Dict[str, str]]
EmployeeGroupsPerWeekList = List[List[List[str]]]


def place(number_of_employees: int) -> PositionsList:
    """
    Returns a minimal series of permutations of 1..N such
    that each number is neighbour at least once with each of
    the others.
    """

    if number_of_employees < 1:
        return [[]]

    # Skip the calculation if calculation already exist
    if number_of_employees % 2:
        """
        N is odd. Solve the problem for (N+1), then remove
        element (N+1) in the result
        """
        arrangements = place(number_of_employees + 1)
        for arr in arrangements:
            arr.remove(number_of_employees + 1)

        return arrangements

    else:
        """
        N is even. Place the elements in that order:
        1, N, 2, N-1, 3, N-2, etc. then roll !
        """
        first_arrangement = []  # construct the first arrangement
        number_of_possible_groupings = number_of_employees // 2
        for i in range(number_of_possible_groupings):
            first_arrangement = first_arrangement + [i + 1, number_of_employees - i]

        # construct the subsequent arrangements using p1
        groupings = []
        for path_number in range(number_of_possible_groupings):
            path = []
            for edge in first_arrangement:
                employee = ((edge + path_number - 1) % number_of_employees) + 1
                path.append(employee)
            groupings.append(path)

        return groupings


def placement_wrapper(number_of_employees: int) -> PositionsList:
    from teamupp.models import Placements  # Causes errors if import is outside of function
    try:
        if cached_placement := Placements.objects.get(pk=number_of_employees):
            return cached_placement.placement
    except:
        pass

    placements = place(number_of_employees)

    placement_model = Placements(id=number_of_employees, placement=placements)
    placement_model.save()

    return placements


def get_new_employee_order(employees: list) -> list:
    new_ordering = employees.copy()
    random.shuffle(new_ordering)
    return new_ordering


def map_placements_to_developer_groups(positions, developers, accessor):
    developers_outer_array = []

    for work_week in positions:
        names_inner_array = []
        work_week.reverse()  # cuts down on repeat group due the removal of a position when the n of employees is odd

        for employee_index in work_week:
            developer = accessor(developers[employee_index - 1])
            names_inner_array.append(developer)

        developers_outer_array.append(names_inner_array)

    return developers_outer_array


def map_groups_to_employee_pairs(groups) -> EmployeeGroupsPerWeekList:
    employee_pairs = []
    for employee_names in groups:
        employee_pairs.append(
            [employee_names[i:i + 2] for i in range(0, len(employee_names), 2)]
        )
    return employee_pairs


def map_list_of_employees_to_work_group_by_week(employees: EmployeesNameList, number_of_weeks: int,
                                                sprint_duration: int = 1) -> EmployeeGroupsPerWeekList:
    if len(employees) < 0:
        raise Exception("employees array is invalid")
    if number_of_weeks < 0:
        raise Exception("Invalid number of weeks")

    number_of_employees = len(employees)
    placements = placement_wrapper(number_of_employees)
    number_to_repeat_placements = number_of_weeks // len(placements)
    groupings = map_placements_to_developer_groups(placements, employees, accessor=lambda dev: dev.get('name'))
    weekly_pairings = map_groups_to_employee_pairs(groupings)

    weeks = []
    for _ in range(number_to_repeat_placements):
        weeks.extend(weekly_pairings)

    return weeks[:number_of_weeks]


def next_weekday(d, weekday: int):  # weekday: 0 = Monday, 1=Tuesday, 2=Wednesday...
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def generate_calender(groupings, project):
    from teamupp.models import Week, Group

    start_of_week = project.start_date
    for developers in groupings:
        end_of_the_week = next_weekday(start_of_week, 4)  # Friday
        week = Week(project=project, start=start_of_week, end=end_of_the_week)
        week.save()

        for i in range(0, len(developers), 2):
            pairing_group = developers[i:i + 2]
            user1 = pairing_group[0]
            user2 = pairing_group[1] if len(pairing_group) > 1 else None

            group = Group.objects.filter(user1=user1, user2=user2)

            if group.exists():
                group = group.first()
            else:
                group = Group(user1=user1, user2=user2)
                group.save()  # TODO: Use this save function for testing using mocks

            week.groups.add(group)

        start_of_week = next_weekday(start_of_week, 0)  # Next Monday


def map_list_of_devs_to_groups_models(developers, number_of_weeks, sprint_duration, project):
    if len(developers) < 0:
        raise Exception("employees array is invalid")
    if number_of_weeks < 0:
        raise Exception("Invalid number of weeks")

    number_of_devs = len(developers)
    placements = placement_wrapper(number_of_devs)
    groupings = map_placements_to_developer_groups(placements, developers, accessor=lambda dev: dev)
    number_to_repeat_placements = number_of_weeks // len(placements)

    for _ in range(number_to_repeat_placements):
        generate_calender(groupings, project)
