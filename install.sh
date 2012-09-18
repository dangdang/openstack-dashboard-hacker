#!/bin/bash
echo "Running Openstack Dashboard hacker..."
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

#Change for passwd  /usr/share/pyshared/horizon/dashboards/settings/dashboard.py
sed -i "s/panels = ('user', 'project'/panels = ('user', 'passwd', 'project'/g" /usr/share/pyshared/horizon/dashboards/settings/dashboard.py

#add register function
mkdir -p /usr/lib/python2.7/dist-packages/horizon/register
ln -sf /usr/share/pyshared/horizon/register/* /usr/lib/python2.7/dist-packages/horizon/register
mkdir -p /usr/lib/python2.7/dist-packages/horizon/templates/horizon/register
ln -sf /usr/share/pyshared/horizon/templates/horizon/register/* /usr/lib/python2.7/dist-packages/horizon/templates/horizon/register/

echo "urlpatterns += patterns('horizon.register.views',url(r'^register$', 'register', name='register'),url(r'register/do/$','register_do', name='register_do'))" >> /usr/share/pyshared/horizon/site_urls.py
sed -i 's/<button type="submit" class="btn btn-primary pull-right">{% trans "Sign In" %}<\/button>/<a href="\/register" class="btn  pull-left">{% trans "Register a new user" %}<\/a><button type="submit" class="btn btn-primary pull-right changed">{% trans "Sign In" %}<\/button>/g' /usr/share/pyshared/horizon/templates/horizon/auth/_login.html

#restart apache
service apache2 restart

echo "All processes has been finished. "