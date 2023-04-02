import inspect
import tupy

class Inspector:
    def __init__(self, env) -> None:
        self.env = env or []
    
    def public_variables(self, type=object):
        if isinstance(type, str):
            type = eval(type)
        return [var for var in self.env if not var.startswith('_') and isinstance(self.env[var], type)]

    def object_has_type(self, obj, type):
        if isinstance(type, str):
            type = eval(type)
        return isinstance(obj, type)

    def public_objects(self, type=object):
        if isinstance(type, str):
            type = eval(type)
        return [self.env[var] for var in self.public_variables(type=type)]

    def eval(self, str):
        # print('eval', str)
        return eval(str, self.env)
    
    def object_for_variable(self, var):
        return self.eval(var)
        # return self.env[var]

    def destroy_variable(self, var):
        del self.env[var]
    
    def destroy_object(self, obj):
        for var in self.public_variables():
            if self.env[var] == obj:
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
        exec(f'{variable} = {classname}({args})', self.env)

inspector = Inspector([])