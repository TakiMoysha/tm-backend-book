class ObjectPolicyImplMixin:
    def validate(self):
        raise NotImplementedError

class Policy:
    def create(self, user, *args, **kwargs):
        raise NotImplementedError

    def read_any(self, user, *args, **kwargs):
        raise NotImplementedError

    def read(self, user, obj: ObjectPolicyImplMixin, *args, **kwargs):
        raise NotImplementedError

    def update(self, user, obj: ObjectPolicyImplMixin, *args, **kwargs):
        raise NotImplementedError

    def delete(self, user, obj: ObjectPolicyImplMixin, *args, **kwargs):
        raise NotImplementedError

    def force_delete(self, user, obj: ObjectPolicyImplMixin, *args, **kwargs):
        raise NotImplementedError

    def resotre(self, user, obj: ObjectPolicyImplMixin, *args, **kwargs):
        raise NotImplementedError


