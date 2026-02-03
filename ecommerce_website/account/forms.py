from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
# 1️⃣ UserCreationForm
# This is a built-in Django form that already knows how to:
# ✔ create a new user
# ✔ hash passwords securely
# ✔ validate:
# password strength
# password confirmation (password1 & password2)
# duplicate usernames

# 2️⃣ AuthenticationForm
# This is used for login, not registration.
# Takes username + password
# Authenticates user
# (You didn’t use it yet here, but you’ll use it in login_view)

# 3️⃣ User
# This is Django’s built-in User model.
# It already has fields like: username,emailpassword (hashed),is_active,is_staff

class Register(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email']

class AdminRegister(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


# 🧠 Why not write our own form?
# If you tried to do this manually, you’d need to:
# hash passwords
# validate password strength
# handle security edge cases
# ❌ Dangerous
# ❌ Error-prone
# ❌ Reinventing the wheel