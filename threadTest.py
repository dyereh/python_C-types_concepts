import ctypes
import ctypes.util
from numpy.ctypeslib import ndpointer
import threading
import time

import ctypes
lib = ctypes.cdll.LoadLibrary('./threadTest.so')
class Foo(object):
    def __init__(self, val):
        lib.Foo_new.argtypes = [ctypes.c_int]
        lib.Foo_new.restype = ctypes.c_void_p

        lib.Foo_bar.argtypes = [ctypes.c_void_p]
        lib.Foo_bar.restype = ctypes.c_void_p

        lib.Foo_foobar.argtypes = [ctypes.c_void_p, ctypes.c_int]
        lib.Foo_foobar.restype = ctypes.c_int

        ## Thread 1 ##
        lib.Foo_thread1.argtypes = [ctypes.c_void_p]
        lib.Foo_thread1.restype = ctypes.c_void_p

        ## Thread 2 ##
        lib.Foo_thread2.argtypes = [ctypes.c_void_p]
        lib.Foo_thread2.restype = ctypes.c_void_p

        ## setArr ##
        lib.Foo_setArr.argtypes = [ctypes.c_int, ctypes.c_char]
        lib.Foo_setArr.restype  = ctypes.c_void_p

        ## getArr ##
        lib.Foo_getArr.argtypes = [ctypes.c_void_p]
        lib.Foo_getArr.restype  = ndpointer(dtype=ctypes.c_char, shape=(10,))

        self.obj = lib.Foo_new(val)

    def bar(self):
        lib.Foo_bar(self.obj)

    def foobar(self, val):
        return lib.Foo_foobar(self.obj, val)

    def thread1(self):
        while(True):
            lib.Foo_thread1(self.obj)

    def thread2(self):
        while(True):
            lib.Foo_thread2(self.obj)

    def setArr(self, idx, value):
        lib.Foo_setArr(self.obj, idx, value)

    def getArr(self):
        return lib.Foo_getArr(self.obj)

# the fillprototype is a user-defined function, see my previous post...
# fillprototype(mylib.add_vector, ctypes.POINTER(ctypes.c_double), [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int])

if __name__ == '__main__':
    # We'll create a Foo object with a value of 5...
    f=Foo(5)
    # Calling f.bar() will print a message including the value...
    # f.bar()
    # # Now we'll use foobar to add a value to that stored in our Foo object, f
    # print (f.foobar(7))
    # # Now we'll do the same thing - but this time demonstrate that it's a normal
    # # Python integer...
    # x = f.foobar(2)
    # print (type(x))

    ########################################################
    ## Demonstrate access of raw char * from the cpp side ##
    ########################################################
    for idx, i in enumerate(range(10)):
        f.setArr(idx, i)

    s = f.getArr()
    print("s:", s)

    for idx, i in enumerate(range(10,20)):
        f.setArr(idx, i)

    t = f.getArr()

    print("s:", s)
    print("t:", t)

    ###########################
    ## Demonstrate threading ##
    ###########################
    t1 = threading.Thread(target=f.thread1)
    t2 = threading.Thread(target=f.thread2)

    t1.start()
    t2.start()

"""
testname = ctypes.util.find_library('test')
testlib = ctypes.cdll.LoadLibrary(testname)

test = testlib.test
test.argtypes = [ctypes.c_int, ctypes.c_int]

def t():
  test(0, 1000000000)

if __name__ == '__main__':
  start_time = time.time()
  t()
  t()
  print "Sequential run time: %.2f seconds" % (time.time() - start_time)

  start_time = time.time()
  t1 = threading.Thread(target=t)
  t2 = threading.Thread(target=t)
  t1.start()
  t2.start()
  t1.join()
  t2.join()
  print "Parallel run time: %.2f seconds" % (time.time() - start_time)
  """