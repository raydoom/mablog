

from django.contrib.auth.forms import UserCreationForm
from .models import Users
class RegisterForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		models = Users
		fields = ("username","email")