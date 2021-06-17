from django.contrib.auth.forms import UserCreationForm
from teamupp.models import TeamUppUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = TeamUppUser
        fields = ["email", "username", 'company', "password1", "password2" ]