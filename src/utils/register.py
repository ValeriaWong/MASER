

class Registry:
    def __init__(self):
        self._registry = {}

    def register(self, alias, class_reference):
        self._registry[alias] = class_reference

    def get_class(self, alias):
        return self._registry.get(alias)

# 使用装饰器来注册类，并且可以指定别名 
registry = Registry()
def register_class(alias=None):
    def decorator(cls):
        nonlocal alias # nonlocal alias 声明 alias 为非局部变量，允许 decorator 函数修改 register_class 函数作用域中的 alias 变量。
        if alias is None:
            alias = cls.__name__
        registry.register(alias, cls)
        return cls
    return decorator


