# if (/usr/bin/python2.7 /usr/src/app/manage.py migrate); then
#     if (/usr/bin/python2.7 /usr/src/app/manage.py makemigrations); then
#         if (/usr/bin/python2.7 /usr/src/app/manage.py migrate); then
#             echo "succeed to migrate database"
#             break
#         fi
#     fi
# fi
/usr/local/bin/supervisord -n
