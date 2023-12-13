from django.contrib.auth.models import User

def create_user(kwargs):
    print(kwargs)
    user = User.objects.create(
        username=kwargs.get("username"),
        first_name=kwargs.get("full_name"),
    )
    user.set_password( kwargs.get("password"))
    user.save()
    return user