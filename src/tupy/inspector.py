import inspect
import tupy
from typing import Any, Callable, Union

class Inspector:
    def __init__(self, env: dict[str, object]) -> None:
        self.env = env
    
    def public_variables(self, type: type = object) -> list[str]:
        if isinstance(type, str):
            type = eval(type)
        
        return [var for var in self.env if not var.startswith('_') and isinstance(self.env[var], type)]

    def object_has_type(self, obj: object, type: type) -> bool:
        if isinstance(type, str):
            type = eval(type)
        return isinstance(obj, type)

    def public_objects(self, type: type = object) -> list[object]:
        if isinstance(type, str):
            type = eval(type)
        return [self.env[var] for var in self.public_variables(type=type)]

    def eval(self, str: str) -> Any:
        # print('eval', str)
        return eval(str, self.env)
    
    def object_for_variable(self, var: str) -> Any:
        return self.eval(var)
        # return self.env[var]

    def destroy_variable(self, var: str) -> None:
        del self.env[var]
    
    def destroy_object(self, obj: object) -> None:
        for var in self.public_variables():
            if self.env[var] == obj:
                self.destroy_variable(var)

    def get_public_methods(self, obj: object) -> list[str]:
        return [attr for attr in dir(obj) if not attr.startswith('_') and callable(getattr(obj, attr))]
    def get_public_attributes(self, obj: object) -> list[str]:
        return [attr for attr in dir(obj) if not attr.startswith('_') and not callable(getattr(obj, attr))]
    
    def get_method(self, obj: object, method_name: str) -> Any:
        return getattr(obj, method_name)

    def method_parameters(self, method: Callable[..., Any]) -> Any:
        return inspect.signature(method).parameters


    def method_info(self, method: Callable[..., Any]) -> str:
        s = f'{method.__name__}{inspect.signature(method)}'
        if method.__doc__ is not None:
            s += method.__doc__
        return s
    
    def create_object(self, variable: str, classname: str, args: str = '') -> None:
        exec(f'{variable} = {classname}({args})', self.env)

inspector = Inspector({})