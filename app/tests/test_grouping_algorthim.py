import pytest
import datetime
from unittest.mock import patch

from ..grouping_algorthim import place, map_list_of_employees_to_work_group_by_week, \
     get_new_employee_order, next_weekday, map_placements_to_developer_groups


@pytest.mark.parametrize("number_of_employees, expected_grouping", [
    (-1, '[[]]'),
    (0, '[[]]'),
    (1, '[[1]]'),
    (2, '[[1, 2]]'),
    (3, '[[1, 2, 3], [2, 1, 3]]'),
    (4, '[[1, 4, 2, 3], [2, 1, 3, 4]]'),
    (5, '[[1, 2, 5, 3, 4], [2, 1, 3, 4, 5], [3, 2, 4, 1, 5]]'),
])
def test_get_groups_in_correct_order(number_of_employees, expected_grouping):
    actual = place(number_of_employees)
    assert str(actual) == expected_grouping


@pytest.mark.parametrize("positions, names, expected", [
    (
            [[1, 2]],
            [{"name": "Julia"}, {"name": "Xing"}],
            "[['Xing', 'Julia']]"
    ),
    (
            [[1, 4, 2, 3], [2, 1, 3, 4]],
            [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}, {"name": "John"}],
            "[['Katie', 'Xing', 'John', 'Julia'], ['John', 'Katie', 'Julia', 'Xing']]"
    ),
    (
            [[1, 2, 5, 3, 4], [2, 1, 3, 4, 5], [3, 2, 4, 1, 5]],
            [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}, {"name": "John"}, {"name": "Sarah"}],
            "[['John', 'Katie', 'Sarah', 'Xing', 'Julia'], ['Sarah', 'John', 'Katie', "
            "'Julia', 'Xing'], ['Sarah', 'Julia', 'John', 'Xing', 'Katie']]"
    )
])
def test_mapping_placements_to_employee_pairs(positions, names, expected):
    actual = map_placements_to_developer_groups(positions=positions, developers=names, accessor=lambda d: d.get('name'))

    assert str(actual) == expected


@patch('app.grouping_algorthim.placement_wrapper')
def test_get_correct_number_weeks_and_correct_shape_after_3_weeks(placement_wrapper_mock):
    employees = [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}, {"name": "John"}, {"name": "Sarah"}]
    number_of_weeks = 3
    placement_wrapper_mock.return_value = place(len(employees))

    actual = map_list_of_employees_to_work_group_by_week(employees, number_of_weeks)

    assert len(actual) == number_of_weeks


@patch('app.grouping_algorthim.placement_wrapper')
def test_get_correct_number_weeks_and_correct_shape_after_12_weeks(placement_wrapper_mock):
    employees = [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}, {"name": "John"}, {"name": "Sarah"}]
    number_of_weeks = 12
    placement_wrapper_mock.return_value = place(len(employees))

    actual = map_list_of_employees_to_work_group_by_week(employees, number_of_weeks)

    assert len(actual) == number_of_weeks


def test_that_shuffling_algorithm_does_not_mutate():
    expected = [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}]

    # Should not change and should be equal to expected
    should_not_change = [{"name": "Julia"}, {"name": "Xing"}, {"name": "Katie"}]
    actual = get_new_employee_order(should_not_change)

    assert str(expected) == str(should_not_change)
    assert str(expected) != str(actual)


def test_gets_next_weekday():
    current_monday = datetime.date(2021, 6, 21)
    assert (next_weekday(current_monday, 1).day - current_monday.day) == 1
    assert (next_weekday(current_monday, 2).day - current_monday.day) == 2
    assert (next_weekday(current_monday, 3).day - current_monday.day) == 3
    assert (next_weekday(current_monday, 4).day - current_monday.day) == 4
    assert (next_weekday(current_monday, 5).day - current_monday.day) == 5
    assert (next_weekday(current_monday, 6).day - current_monday.day) == 6
    assert (next_weekday(current_monday, 0).day - current_monday.day) == 7

