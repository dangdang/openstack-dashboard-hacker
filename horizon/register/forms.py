# vim: tabstop=4 shiftwidth=4 softtabstop=4
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from horizon import forms
from horizon.utils import validators

"""
Forms used for Horizon's register mechanisms.
"""

class RegForm(forms.SelfHandlingForm):
    """ Form used for logging in a user.

    Handles authentication with Keystone, choosing a tenant, and fetching
    a scoped token token for that tenant. Redirects to the URL returned
    by :meth:`horizon.get_user_home` if successful.

    Subclass of :class:`~horizon.forms.SelfHandlingForm`.
    """
    
    username = forms.CharField(label=_("User Name"), min_length=5, max_length=30, required=True)
    email = forms.EmailField(label=_("E-mail"))
    password = forms.RegexField(
            label=_("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            error_messages={'invalid': validators.password_validator_msg()})
    #error_messages={'required': _('Confirm Password must be same with password.')}
    confirm_password = forms.CharField(
            label=_("Confirm Password"),
            required=False,
            widget=forms.PasswordInput(render_value=False))
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
    def clean(self):
        password = self.cleaned_data.get('password', '').strip()
        confirm_password = self.cleaned_data.get('confirm_password', '').strip()
        if len(password)<6 or len(password)>18 or password != confirm_password:
            self._errors["password"] = ErrorList([_('Password must be between 8 and 18 characters.')])
            self._errors["confirm_password"] = ErrorList([_('Confirm Password must be same with password.')])
            del self.cleaned_data["confirm_password"]
        return self.cleaned_data

