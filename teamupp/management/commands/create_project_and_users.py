import os
import json

from faker import Faker

from django.core.management.base import BaseCommand
from app.grouping_algorthim import map_list_of_devs_to_groups_models, \
    get_new_employee_order

from teamupp.models import Company, Project, TeamUppUser


class Command(BaseCommand):
    help = 'imports a project and collection of users into the app'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        print('Starting...')
        json_file = options['json_file']
        data = None
        with open(os.path.abspath(json_file)) as f:
            data = json.load(f)

        if number_of_weeks := data.get("projectDurationMonths"):
            print('Duration denoted in months')
            number_of_weeks *= 4
        elif number_of_weeks := data.get("projectDurationWeeks"):
            pass
        else:
            raise Exception("Duration of project was not set")

        print(f'Duration of project will be {number_of_weeks} weeks')

        print('creating project...')
        current_project = Project(
            name=data.get('projectName', None),
            duration=number_of_weeks
        )
        current_project.save()
        print(f'Done creating project! Project name: "{current_project.name}"')

        company_name = data.get('projectCompany', '[Default Company]')

        print('Loading company...')

        if (company := Company.objects.filter(name=company_name)).exists():
            print(f'Company with the name "{company_name}", already exists! Will use the one found in the records')
            company = company.first()
        else:
            print(f'Company with the name "{company_name}", does not exists! Creating now...')
            company = Company(name=company_name)
            company.save()
            print(f'finished creating "{company_name}"')

        print('Finished Loading company')

        print('Loading Developers...')
        developers = []
        faker = Faker()
        for developer in data.get('developers'):
            developer_name = developer.get('name')
            developer_email = developer.get('email', faker.ascii_free_email())
            developer_password = developer.get('password', F"{company_name}{developer_name}")

            if (team_mate := TeamUppUser.objects.filter(username=developer_name)).exists():
                print(f'Found Developer {developer_name} in records')
                team_mate = team_mate.first()
            else:
                print(f'Creating records for Developer {developer_name}')
                team_mate = TeamUppUser(username=developer_name, company=company, email=developer_email,
                                        password=developer_password)
                team_mate.save()

            current_project.participants.add(team_mate)
            developers.append(team_mate)
        print('Finished Loading Developers')

        print('Creating Calender...')
        map_list_of_devs_to_groups_models(
            developers=get_new_employee_order(developers),
            number_of_weeks=number_of_weeks,
            sprint_duration=data.get('sprintDurationWeeks'),
            project=current_project
        )
        print('Finished Creating Calender!!')
        print('All done! Goodbye!')
