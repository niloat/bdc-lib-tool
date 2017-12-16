class _const:
    class ConstError(TypeError):
        pass
    def __setattr__(self, name, value):
#if name in self.__dict__:
        if self.__dict__.__contains__(name):
            raise self.ConstError("Cannot rebind const(%s)" % name)
        self.__dict__[name] = value
import sys
sys.modules[__name__] = _const()
