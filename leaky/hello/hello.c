#include <Python.h>
#include "hello.h"

static PyObject *hello(PyObject *self, PyObject *args){
  static char hello[] = "And this time inside a Docker container";

  return Py_BuildValue("s", hello);
}

static char hello_mod_documentation[] = "This module does some stuff";
static char hello_func_documentation[] = "This is a function that simply says hello";

static PyMethodDef functions[] = {
  {"hello", hello, METH_NOARGS, hello_func_documentation},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

PyModuleDef hello_mod = {
	PyModuleDef_HEAD_INIT,
	"hello",
	hello_mod_documentation,
	-1,
	functions,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_hello(void) {
	return PyModule_Create(&hello_mod);
}

#else

void inithello(void) {
	Py_InitModule3("hello", functions, hello_mod_documentation);
}

#endif