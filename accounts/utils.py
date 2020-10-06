from django.forms.utils import ErrorList
from django.shortcuts import HttpResponse


class LoginErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return '<div class="error_msg_login">%s</div>' % "".join(
            ['<p class="error_msg error_msg_dj">%s</p>' % e.strip() for e in self]
        )


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            type = request.user.usertype.type

            if type in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")

        return wrapper_func

    return decorator

