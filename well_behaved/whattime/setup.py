from distutils.core import setup, Extension

whattime_extension = Extension('whattime', sources=['whattime.c'])

setup(name='hello', version='0.1.0-SNAPSHOT',
      description='A Python web service that tells you the current time', ext_modules=[whattime_extension])
