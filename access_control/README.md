1. Student - read his own records
2. Teacher - create, update, read and delete student records
3. Principal - create, read, update and delete

*User, Group and Permissions*
"django.contrib.auth" - defaul authentication system (identification)

*Student Assessment Record*
```bash
python manage.py startapp record
```

```python
from django.db import models
from django.contrib.auth.models import User

class StudentAssessmentRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.username} - Score:{self.score}"
```
