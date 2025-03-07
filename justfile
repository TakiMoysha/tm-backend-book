## ====================================== deprecated

py-new-django project_name:
  django-admin startproject --template=django/templates/base {{ project_name }}

py-new-app app_name:
    uv init {{ app_name }} --no-workspace

apache-benchmark:
    ab -n 100000 -c 10 http://127.0.0.1:8000/api/orders
