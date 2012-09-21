'''
Created on 2012-9-17

@author: Lion
'''

from django import shortcuts
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from horizon.register.forms import RegForm
from openstack_dashboard.views import user_home
import ConfigParser
import commands

def register(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(user_home(request.user))
    regform = RegForm()
    request.session.clear()
    try:
        re=settings.REGISTER_ENABLED
        re_declare=settings.REGISTER_DISABLE_DECLARE
    except:
        re=True
        re_declare=""
        
    if(re):
        return shortcuts.render(request, 'horizon/register/index.html', {'form': regform})
    else:
        return shortcuts.render(request, 'horizon/register/register_disable.html', {'declare': re_declare})


def register_do(request):
    rf=RegForm(request.POST)
    er=""
    if rf.is_valid():
        #assert False
        d=rf.cleaned_data 
        username = d['username']
        password=d['password']
        tenantname=username
        email = d['email']
            #assert False
        #return shortcuts.render(request, 'horizon/register/index.html', {'username':username,'email':email})
        cfg=ConfigParser.ConfigParser()
        cfg.read('/etc/nova/api-paste.ini')
        keystone_cfg=dict(cfg.items('filter:authtoken'))
        tenant_cmd="/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s tenant-create --name %s |grep id |awk '{print $4}'" % (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,tenantname)
        tenant_cmd_op=commands.getstatusoutput(tenant_cmd)
        if(len(tenant_cmd_op[1])==32):
            user_cmd="/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s user-create --name %s --tenant_id %s --pass %s --email %s |sed -n '6p' | awk '{print $4}'" % (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,username,tenant_cmd_op[1],password,email)
            user_cmd_op=commands.getstatusoutput(user_cmd)
            if(len(user_cmd_op[1])==32):
                return shortcuts.render(request, 'horizon/register/index.html', {'username':username,'email':email})
            else:
                er=_('Create User fail, User name perhaps exist')
        else:
            er=_('Create Tenant fail, Tenant name perhaps exist.')
        
    return shortcuts.render(request, 'horizon/register/index.html', {'form': rf,'error':er})
    

