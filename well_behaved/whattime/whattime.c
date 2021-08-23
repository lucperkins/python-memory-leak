#include <Python.h>
#include <time.h>

#include "whattime.h"

#define BUFFERSIZE 100

static PyObject *current_timestamp_formatted() {
	time_t now;
	struct tm *time_info;
	char formatted_time_string_buffer[BUFFERSIZE];

	time(&now);

	time_info = localtime(&now);

	strftime(formatted_time_string_buffer, BUFFERSIZE, "%x - %I:%M%p", time_info);

  return Py_BuildValue("s", formatted_time_string_buffer);
}

static PyObject *current_timestamp_raw() {
	time_t now;
	PyObject *value;

	now = time(NULL);

  return Py_BuildValue("i", now);
}

static char whattime_mod_documentation[] = "This module performs tasks related to the current time";
static char current_raw_func_documentation[] = "This function tells you the current time";
static char current_formatted_func_documentation[] = "This function tells you the current time";

static PyMethodDef functions[] = {
  {"current_timestamp_raw", current_timestamp_raw, METH_NOARGS, current_raw_func_documentation},
	{"current_timestamp_formatted", current_timestamp_formatted, METH_NOARGS, current_formatted_func_documentation},
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