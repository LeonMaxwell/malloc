from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from .models import MallocBaseUser


class MallocUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MallocBaseUser
        fields = ('email', 'password')


class MallocChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = MallocBaseUser
        fields = ('email', 'password')