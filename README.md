# Backend Book

The main goal is to learn backend practices. Typing rules (mypy, python rules), nosql, function-based & class-based & ViewSet. Overriding apps defined in django (sessions, middleware and etc.)

How to build an application, handle errors, write logs (for service employees).

The backend can be divided into components:

- interface (cli, admin, api, ...)
- business (logic for which the server is responsible)
- store (cache, database, fs, ...)

Backend theory and methodologys: deadline propagation;

[About FastAPI deployment, useful for python deployment / github.com](https://github.com/zhanymkanov/fastapi-best-practices)

# Projects

- **webauth** -
- **rbac_hierarchy** -
- **real_time_analyze** - analytics and reports
- **registry** - <!-- working with django ContentType -->

```python
class BaseRegistry(models.Model):
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  registry = GenericForeignKey('object_id')

    class Meta:
      abstract = True
      indexes = [
        models.Index(fields=['content_type', 'object_id']),
      ]
```

- **plans** - user subscription level, similar to user groups
- **multiplexing websockets** - combining several data channels into one

- **advanced_sessions** -

# Awesome

## Roadmap

### Skills

- Database Design

## Working with Django

- [djangoviz - visualize your models and their relationships using](https://github.com/ariga/djangoviz)
- [django-storages - provide a variety of storage backends in a single library](https://github.com/jschneier/django-storages)
- [django-health-check - checks for various conditions and provides reports when anomalous behavior is detected](https://django-health-check.readthedocs.io/en/latest/)
- [django-templated-mail - simple email system](https://djangopackages.org/packages/p/django-templated-mail/)
- [django-allauth - ](https://github.com/pennersr/django-allauth)

## Open-Source

1. [Taiga - project management / github.com](https://github.com/taigaio/taiga):
2. [Django Plans / github.com](https://github.com/django-getpaid/django-plans)

## Access and Permissions

1. [django-rules / github.com](https://github.com/dfunckt/django-rules) -
   version conflict
2. [django-prbac / github.com](https://github.com/dimagi/django-prbac)
   ([docs](https://django-prbac.readthedocs.io/en/latest/)) - version conflict
3. [django-auhority / django-authority.readthedocs.io](https://django-authority.readthedocs.io/en/latest/) -
   used deprecated function

# Resources

1. [Classy Class-Based Views / ccbbv.co.uk](https://ccbv.co.uk/)
2. [Django Vanilla Views / django-vanilla-views.org](http://django-vanilla-views.org/)
3. [Pinax project / pinaxproject.com](https://pinaxproject.com/pinax/)
4. https://django-best-practices.readthedocs.io/en/latest/index.html

# References

1. [Программирование: ФП подходы на продакшене / SOER / youtube.com](https://www.youtube.com/watch?v=9ajlmRJwF5M)
2. [PostgreSQL - Chapter 21. Database Roles / www.postgresql.org](https://www.postgresql.org/docs/devel/user-manag.html)
