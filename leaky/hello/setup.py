from distutils.core import setup, Extension

hello_extension = Extension('hello', sources=['hello.c'])

setup(name='hello', version='0.1.0-SNAPSHOT', description='A Python app that leaks memory...on purpose!',
      ext_modules=[hello_extension])
