'''
Created on 2012-9-17

@author: Lion
'''
from django import shortcuts
from django.conf import settings
from horizon.register import forms as _regform
from openstack_dashboard.views import user_home
from django.utils.translation import ugettext_lazy as _
import ConfigParser
import commands

def register(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(user_home(request.user))
    regform = _regform.RegForm()
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
    regform = _regform.RegForm()
    #try:
    username = request.POST['username']
    password=request.POST['password']
    comfirm_password=request.POST['confirm_password']
    tenantname=username
    email = request.POST['email']
    #except:
    if(len(username)>3 and len(password)>5 and password==comfirm_password):
        cfg=ConfigParser.ConfigParser()
        cfg.read('/etc/nova/api-paste.ini')
        keystone_cfg=dict(cfg.items('filter:authtoken'))
        tenant_cmd="/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s tenant-create --name %s |grep id |awk '{print $4}'" % (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,tenantname)
        tenant_cmd_op=commands.getstatusoutput(tenant_cmd)
        if(len(tenant_cmd_op[1])==32):
            user_cmd="/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s user-create --name %s --tenant_id %s --pass %s --email %s |grep id |awk '{print $4}'" % (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,username,tenant_cmd_op[1],password,email)
            user_cmd_op=commands.getstatusoutput(user_cmd)
            if(len(user_cmd_op[1])==32):
                return shortcuts.render(request, 'horizon/register/register_do.html', {'username':username,'email':email})
            else:
                er=_('Create User fail.')
        else:
            er=_('Create Tenant fail.')
    else:   
        er=_('Error : Username length must be greater than 3, Password length must be greater than 6, Confirm password must be same with Password.')
        
    return shortcuts.render(request, 'horizon/register/index.html', {'form': regform,'error':er})
    #else:
    
    

