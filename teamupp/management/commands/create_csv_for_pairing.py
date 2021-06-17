import csv
import os
import json

from django.core.management.base import BaseCommand
from app.grouping_algorthim import map_list_of_employees_to_work_group_by_week, \
    get_new_employee_order


class Command(BaseCommand):
    help = 'generates a csv of work groups for a given project'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        json_file = options['json_file']
        data = None
        with open(os.path.abspath(json_file)) as f:
            data = json.load(f)

        if number_of_weeks := data.get("projectDurationMonths"):
            number_of_weeks *= 4
        elif number_of_weeks := data.get("projectDurationWeeks"):
            pass
        else:
            raise Exception("Duration of project was not set")

        work_groups = map_list_of_employees_to_work_group_by_week(
            employees=get_new_employee_order(data.get('developers')),
            number_of_weeks=number_of_weeks,
            sprint_duration=data.get('sprintDurationWeeks')
        )

        number_of_groups = len(work_groups[0])
        week_number = 1
        print(f"Number of Weeks: {number_of_weeks}\nNumber of Groups: {number_of_groups}")

        first_column = [f"Group #{i + 1}" for i in range(number_of_groups)]
        first_column.insert(0, "")  # offset for the weeks text in the coming code

        csv_output = [first_column]

        for week in work_groups:
            print(f"== Week {week_number} ==")
            grouping = [f"Week {week_number}"]
            for i, group in enumerate(week):
                output = group[0]
                if len(group) > 1:
                    output = " and ".join(group)
                print(f"Group #{i + 1}: {output}")
                grouping.append(output)

            week_number += 1
            csv_output.append(grouping)

        with open('pairing_groups_by_week.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_output)
