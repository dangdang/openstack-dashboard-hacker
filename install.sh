#!/bin/bash

#复制安装文件，替换
cp -Rf ./horizon /usr/share/pyshared/


#修改floating_ip使之按项目分组
sed -i 's/for pool in api.floating_ip_pools_list(self.request)]/for pool in api.keystone.tenant_list(self.request)]/g' /usr/share/pyshared/horizon/dashboards/nova/access_and_security/floating_ips/views.py

#创建 软链接
mkdir /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd
ln -s /usr/share/pyshared/horizon/dashboards/settings/passwd/* /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd/
mkdir /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd
ln -s /usr/share/pyshared/horizon/dashboards/settings/templates/settings/passwd/*.html /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd/

#修改 /usr/share/pyshared/horizon/dashboards/settings/dashboard.py
sed -i "s/panels = ('user', 'project'/panels = ('user', 'passwd', 'project'/g" /usr/share/pyshared/horizon/dashboards/settings/dashboard.py