'''
Created on 2012-9-17

@author: Lion
'''
from django import shortcuts
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template.context import Context
from horizon.api import keystone
from horizon.register import forms as _regform
from openstack_dashboard.views import user_home
import ConfigParser
import commands
import os

def register(request):
    if request.user.is_authenticated():
        return shortcuts.redirect(user_home(request.user))
    regform = _regform.RegForm()
    request.session.clear()
    
    return shortcuts.render(request, 'horizon/register/index.html', {'form': regform})


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
        #cfg.read('/etc/nova/api-paste.ini')
        cfg.read('D:\\Java\\workspace\\horizon\\api-paste.ini')
        keystone_cfg=dict(cfg.items('filter:authtoken'))
        tenant_cmd='/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s tenant-create --name %s |grep id |awk "{print $4}"'% (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,tenantname)
        tenant_cmd_op=commands.getstatusoutput(tenant_cmd)
        if(tenant_cmd_op[0]==0):
            user_cmd='/usr/bin/keystone --os_tenant_name=%s --os_username=%s --os_password=%s --os_auth_url=%s tenant-create --name %s |grep id |awk "{print $4}"'% (keystone_cfg['admin_tenant_name'],keystone_cfg['admin_user'],keystone_cfg['admin_password'],settings.OPENSTACK_KEYSTONE_URL,username,tenant_cmd_op[1],password,email)
            user_cmd_op=commands.getstatusoutput(user_cmd)
            if(user_cmd_op[0]==0):
                return shortcuts.render(request, 'horizon/register/register_do.html', {'username':username,'email':email})
            else:
                er='Create User fail'
        else:
            er='Create Tenant fail.'
    else:   
        er='Username must contain 3 charactors and password must contain 6 characors'
        
    return shortcuts.render(request, 'horizon/register/index.html', {'form': regform,'error':er})
    #else:
    
    

