# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Forms used for Horizon's register mechanisms.
"""


from django.utils.translation import ugettext as _
from horizon import  forms
from horizon.utils import validators
import logging





LOG = logging.getLogger(__name__)



class RegForm(forms.SelfHandlingForm):
    """ Form used for logging in a user.

    Handles authentication with Keystone, choosing a tenant, and fetching
    a scoped token token for that tenant. Redirects to the URL returned
    by :meth:`horizon.get_user_home` if successful.

    Subclass of :class:`~horizon.forms.SelfHandlingForm`.
    """
    
    username = forms.CharField(label=_("User Name"),max_length=30,required=True,error_messages={'required': _('Please enter your username')})
    email = forms.EmailField(label=_("E-mail"))
    password = forms.RegexField(
            label=_("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            error_messages={'invalid': validators.password_validator_msg()})
    confirm_password = forms.CharField(
            label=_("Confirm Password"),
            required=False,
            widget=forms.PasswordInput(render_value=False))
    def __init__(self, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        # FIXME(gabriel): When we switch to region-only settings, we can
        # remove this default region business.

