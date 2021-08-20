#include <Python.h>
#include "whattime.h"

static PyObject *current(PyObject *self, PyObject *args) {
  static char hello[] = "And this time inside a Docker container";

  return Py_BuildValue("s", hello);
}

static char whattime_mod_documentation[] = "This module performs tasks related to the current time";
static char current_func_documentation[] = "This function tells you the current time";

static PyMethodDef functions[] = {
  {"current", current, METH_NOARGS, current_func_documentation},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

PyModuleDef whattime_mod = {
	PyModuleDef_HEAD_INIT,
	"whattime",
	whattime_mod_documentation,
	-1,
	functions,
	NULL,
	NULL,
	NULL,
	NULL
};

PyMODINIT_FUNC PyInit_whattime(void) {
	return PyModule_Create(&whattime_mod);
}

#else

void initwhattime(void) {
	Py_InitModule3("whattime", functions, whattime_mod_documentation);
}

#endif