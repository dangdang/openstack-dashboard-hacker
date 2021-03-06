#!/bin/bash
echo "Running Openstack Dashboard hacker..."

#change vnc iframe windows size
sed -i 's/width="720" height="430"/width="100%" height="800"/g' /usr/share/pyshared/horizon/dashboards/nova/templates/nova/instances_and_volumes/instances/_detail_vnc.html

#Change api-paste.ini permission for django reading
chmod 755 /etc/nova
chmod 644 /etc/nova/api-paste.ini
#copy files
cp -Rf ./horizon /usr/share/pyshared/
cp -Rf ./openstack_dashboard /usr/share/openstack-dashboard/
#floating ips view.py
sed -i 's/for pool in api.floating_ip_pools_list(self.request)]/for pool in api.keystone.tenant_list(self.request)]/g' /usr/share/pyshared/horizon/dashboards/nova/access_and_security/floating_ips/views.py

#Create pythton package
mkdir -p /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd
ln -sf /usr/share/pyshared/horizon/dashboards/settings/passwd/* /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/passwd/
mkdir -p /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd
ln -sf /usr/share/pyshared/horizon/dashboards/settings/templates/settings/passwd/* /usr/lib/python2.7/dist-packages/horizon/dashboards/settings/templates/settings/passwd/
ln -sf /usr/share/pyshared/horizon/locale/zh_CN/LC_MESSAGES/django.mo /usr/lib/python2.7/dist-packages/horizon/locale/zh_CN/LC_MESSAGES/django.mo
#Change for passwd  /usr/share/pyshared/horizon/dashboards/settings/dashboard.py
sed -i "s/panels = ('user', 'project'/panels = ('user', 'passwd', 'project'/g" /usr/share/pyshared/horizon/dashboards/settings/dashboard.py

#add register function
mkdir -p /usr/lib/python2.7/dist-packages/horizon/register
ln -sf /usr/share/pyshared/horizon/register/* /usr/lib/python2.7/dist-packages/horizon/register
mkdir -p /usr/lib/python2.7/dist-packages/horizon/templates/horizon/register
ln -sf /usr/share/pyshared/horizon/templates/horizon/register/* /usr/lib/python2.7/dist-packages/horizon/templates/horizon/register/
sed -i "s/urlpatterns += patterns('horizon.register.views',url(r'^register$', 'register', name='register'),url(r'register\/do\/$','register_do', name='register_do'))//g" /usr/share/pyshared/horizon/site_urls.py
echo "urlpatterns += patterns('horizon.register.views',url(r'^register$', 'register', name='register'),url(r'register/do/$','register_do', name='register_do'))" >> /usr/share/pyshared/horizon/site_urls.py
sed -i 's/<button type="submit" class="btn btn-primary pull-right">{% trans "Sign In" %}<\/button>/<a href="\/register" class="btn  pull-left">{% trans "Register a new user" %}<\/a><button type="submit" class="btn btn-primary pull-right changed">{% trans "Sign In" %}<\/button>/g' /usr/share/pyshared/horizon/templates/horizon/auth/_login.html
#disable register
sed -i "s/REGISTER_ENABLED=True//g"  /etc/openstack-dashboard/local_settings.py
sed -i 's/REGISTER_DISABLE_DECLARE="Register is disabled"//g' /etc/openstack-dashboard/local_settings.py
echo "REGISTER_ENABLED=True" >> /etc/openstack-dashboard/local_settings.py
echo 'REGISTER_DISABLE_DECLARE="Register is disabled"' >> /etc/openstack-dashboard/local_settings.py
#restart apache
service apache2 restart

echo "All processes has been finished. "