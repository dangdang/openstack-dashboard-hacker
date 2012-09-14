#!/bin/bass
cp -Rf ./horizon /usr/share/pyshared/

#floating ips view.py
sed -i 's/for pool in api.floating_ip_pools_list(self.request)]/for pool in api.keystone.tenant_list(self.request)]/g' /usr/share/pyshared/horizon/dashboards/nova/access_and_security/floating_ips/views.py

mkdir -p /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd
ln -s /usr/share/pyshared/horizon/dashboards/settings/passwd/* /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd/
mkdir -p /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd
ln -s /usr/share/pyshared/horizon/dashboards/settings/templates/settings/passwd/*.html /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd/

#Change for passwd  /usr/share/pyshared/horizon/dashboards/settings/dashboard.py
sed -i "s/panels = ('user', 'project'/panels = ('user', 'passwd', 'project'/g" /usr/share/pyshared/horizon/dashboards/settings/dashboard.py