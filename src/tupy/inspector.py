import inspect
import tupy

class Inspector:
    def __init__(self, env) -> None:
        self._env = env or []
    
    def public_variables(self, type=object):
        if isinstance(type, str):
            type = eval(type)
        return [var for var in self._env if not var.startswith('_') and isinstance(self._env[var], type)]

    def object_has_type(self, obj, type):
        if isinstance(type, str):
            type = eval(type)
        return isinstance(obj, type)

    def public_objects(self, type=object):
        if isinstance(type, str):
            type = eval(type)
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
    
    def get_method(self, obj, method_name):
        return getattr(obj, method_name)

    def method_parameters(self, method):
        # return inspect.signature(method).parameters
        return inspect.getargspec(method).args[1:]

    def method_info(self, method):
        s = f'{method.__name__}{inspect.signature(method)}'
        if method.__doc__ is not None:
            s += method.__doc__
        return s
    
    def create_object(self, variable, classname, args=''):
        exec(f'{variable} = {classname}({args})', self._env)