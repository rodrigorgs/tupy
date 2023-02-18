class Inspector:
    def __init__(self, env) -> None:
        self._env = env or []
    
    def public_variables(self, type=object):
        return [var for var in self._env if not var.startswith('_') and isinstance(self._env[var], type)]
    
    def public_objects(self, type=object):
        return [self._env[var] for var in self.public_variables(type=type)]

    def object_for_variable(self, var):
        return self._env[var]
