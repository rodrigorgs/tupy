class Inspector:
    def __init__(self, env) -> None:
        self._env = env or []
    
    def public_variables(self, type=object):
        return [var for var in self._env if not var.startswith('_') and isinstance(self._env[var], type)]
    
    def public_objects(self, type=object):
        return [self._env[var] for var in self.public_variables(type=type)]

    def object_for_variable(self, var):
        return self._env[var]

    def destroy_variable(self, var):
        del self._env[var]
    
    def destroy_object(self, obj):
        for var in self.public_variables():
            if self._env[var] == obj:
                self.destroy_variable(var)

    def get_public_methods(self, obj):
        return [attr for attr in dir(obj) if not attr.startswith('_') and callable(getattr(obj, attr))]
    def get_public_attributes(self, obj):
        return [attr for attr in dir(obj) if not attr.startswith('_') and not callable(getattr(obj, attr))]