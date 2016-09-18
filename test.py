#coding=utf-8

import pdb

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

class A(Singleton):
    a = 1

@singleton
class B(object):
    b = 1

if __name__ == "__main__":
    print id(A())
    print id(A())
    print id(A())
    print id(A())
    print id(A())
    print id(A())

    print id(B())
    print id(B())
    print id(B())
    print id(B())
    print id(B())
    print B().b
