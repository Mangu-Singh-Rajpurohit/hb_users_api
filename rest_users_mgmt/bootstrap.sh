#whereis source
#source /tmp/tmp1/hb_users_api/rest_users_mgmt/docker_venv/bin/activate
#supervisord -c supervisord.conf
supervisord
#supervisorctl reread 
#supervisorctl update
#python manage.py runserver localhost:7777 &
service rabbitmq-server start
#celery -A rest_users_mgmt worker -l info 
