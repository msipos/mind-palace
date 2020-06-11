from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView


class MpAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'  # bulma
        self.fields['password'].widget.attrs['class'] = 'input'  # bulma


class MpLoginView(LoginView):
    template_name = 'auth/login.jinja.html'
    redirect_authenticated_user = True
    form_class = MpAuthenticationForm


class MpLogoutView(LogoutView):
    pass
