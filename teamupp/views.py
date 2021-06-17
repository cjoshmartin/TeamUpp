from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .Forms.RegisterForm import RegisterForm
from .models import TeamUppUser, Project, Week, Group, Company
from app.grouping_algorthim import map_list_of_devs_to_groups_models


# Creation views
# ------------------------------------------------
class InviteUserView(LoginRequiredMixin, CreateView):
    model = TeamUppUser
    template_name = 'teamupp/invite_user/index.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('teamupp:invite-success')
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        new_user: TeamUppUser = form.save(commit=False)
        new_user.company = self.request.user.company
        new_user.save()
        return super().form_valid(form)


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'teamupp/create_project/index.html'
    # TODO: Fix participants to be only in user's company
    fields = ['name', 'duration', 'participants']
    success_url = reverse_lazy('teamupp:project-success')
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        project: Project = form.save()
        map_list_of_devs_to_groups_models(
            developers=list(project.participants.all()),
            number_of_weeks=project.duration,
            sprint_duration=1,
            project=project
        )
        return super().form_valid(form)


class RegisterUserView(CreateView):
    model = TeamUppUser
    form_class = RegisterForm
    template_name = 'registration/register/index.html'
    success_url = reverse_lazy("teamupp:register-success")

    def get_form(self, form_class=None):
        form = super(RegisterUserView, self).get_form(form_class)
        form.fields['email'].required = True
        return form


# ------------------------------------------------

# List Views
# ------------------------------------------------
class HomeView(LoginRequiredMixin, ListView):
    template_name = "teamupp/index.html"
    context_object_name = 'projects'
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Project.objects \
            .filter(participants__id=self.request.user.id) \
            .order_by('-start_date', '-id')


class SearchResultsView(LoginRequiredMixin, ListView):
    template_name = 'teamupp/search.html'
    context_object_name = 'project_search_results'
    model = Project
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data()
        query = self.request.GET.get('search')
        if query:
            group_lookup = Q(name__icontains=query) \
                           | Q(user1__username__icontains=query) \
                           | Q(user2__username__icontains=query)
            context['group_search_results'] = Group.objects.filter(group_lookup).distinct()

            user_lookup = Q(username__icontains=query) \
                          | Q(email__icontains=query) \
                          | Q(first_name__icontains=query) \
                          | Q(last_name__icontains=query)
            context['user_search_results'] = TeamUppUser.objects.filter(user_lookup).distinct()

            company_lookup = Q(name__icontains=query)
            context['company_search_results'] = Company.objects.filter(company_lookup).distinct()

        return context

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            lookup = Q(name__icontains=query) | Q(participants__username__icontains=query)
            results = Project.objects.filter(lookup).distinct()
            return results


# ------------------------------------------------

# Detail Views
# ------------------------------------------------
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        weeks = Week.objects.filter(project=self.object).order_by('id')
        context['weeks'] = enumerate(weeks)
        first_week = weeks.first()
        number_of_groups_in_first_week = len(first_week.groups.all())
        context['groups_headers'] = range(number_of_groups_in_first_week)
        context['company'] = self.object.participants.first().company
        return context


class GroupsDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'teamupp/group_detail.html'
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        weeks = Week.objects.filter(groups=self.object)
        first_week_together = weeks.order_by('start').first()
        context['first_week'] = first_week_together.start

        projects = []
        for week in weeks:
            projects.append(week.project)

        context['projects'] = list(set(projects))

        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = TeamUppUser
    template_name = 'teamupp/user_details.html'
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(participants=self.object)
        groups_lookup = Q(user1=self.object) |Q(user2=self.object)
        context['groups'] = Group.objects.filter(groups_lookup).distinct()

        solo_group =Group.objects.filter(user1=self.object, user2=None).first()
        if solo_group:
            context['aka_name'] = solo_group.name
        else:
            context['aka_name'] = None


        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'teamupp/company_details.html'
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        users = TeamUppUser.objects.filter(company=self.object)
        context['users'] = users
        groups_lookup = Q(user1=users[0]) | Q(user2=users[0])

        for user in users[1:]:
            groups_lookup |= Q(user1=user) | Q(user2=user)

        context['groups'] = Group.objects.filter(groups_lookup).distinct()
        context['projects'] = Project.objects.filter(participants__in=users).distinct()

        return context

# ------------------------------------------------
