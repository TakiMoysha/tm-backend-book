py-new-django project_name:
  django-admin startproject --template=django/templates/base {{ project_name }}

py-new-app app_name:
    uv init {{ app_name }} --no-workspace

# in locust folder
locust:
    locust --host http://localhost:8000
