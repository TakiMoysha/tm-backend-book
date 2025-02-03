py-new-django project_name:
  django-admin startproject --template=django/templates/base {{ project_name }}

py-new-app app_name:
    uv init {{ app_name }} --no-workspace

# in locust folder
locust:
    locust --host http://localhost:8000

create-docker-locust:
    docker run -it --name locust-inst -p 8089:8089 -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py

docker-locust:
    docker start locust-inst --attach

apache-benchmark:
    ab -n 100000 -c 10 http://127.0.0.1:8000/api/orders
