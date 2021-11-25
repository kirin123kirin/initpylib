/* csankey.cpp | MIT License | https://github.com/kirin123kirin/csankey/raw/main/LICENSE */
#include "_PLEASE_PYPROJECT_NAME_.hpp"

extern "C" PyObject* _PLEASE_PYPROJECT_NAME__py(PyObject* self, PyObject* args, PyObject* kwargs) {
    PyObject* o;

    const char* kwlist[2] = {"o", NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "O", (char**)kwlist, &o))
        return NULL;

    if(!PyList_Check(o) && !PyTuple_Check(o))
        return PyErr_Format(PyExc_TypeError, "argument is list or tuple object only.");

    return o;
}

#define MODULE_NAME __PLEASE_PYPROJECT_NAME_
#define MODULE_NAME_S "__PLEASE_PYPROJECT_NAME_"

/* {{{ */
// this module description
#define MODULE_DOCS                                            \
    "_PLEASE_PYPROJECT_NAME_ Overview.\n"                      \
    "Description xxxx.\n" \
    ""

#define _PLEASE_PYPROJECT_NAME__py_DESC "\n"

/* }}} */
#define PY_ADD_METHOD(py_func, c_func, desc) \
    { py_func, (PyCFunction)c_func, METH_VARARGS, desc }
#define PY_ADD_METHOD_KWARGS(py_func, c_func, desc) \
    { py_func, (PyCFunction)c_func, METH_VARARGS | METH_KEYWORDS, desc }

/* Please extern method define for python */
/* PyMethodDef Parameter Help
 * https://docs.python.org/ja/3/c-api/structures.html#c.PyMethodDef
 */
static PyMethodDef py_methods[] = {PY_ADD_METHOD_KWARGS("_PLEASE_PYPROJECT_NAME_", _PLEASE_PYPROJECT_NAME__py, _PLEASE_PYPROJECT_NAME__py_DESC),
                                   {NULL, NULL, 0, NULL}};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef py_defmod = {PyModuleDef_HEAD_INIT, MODULE_NAME_S, MODULE_DOCS, 0, py_methods};
#define PARSE_NAME(mn) PyInit_##mn
#define PARSE_FUNC(mn) \
    PyMODINIT_FUNC PARSE_NAME(mn)() { return PyModule_Create(&py_defmod); }

#else
#define PARSE_NAME(mn) \
    init##mn(void) { (void)Py_InitModule3(MODULE_NAME_S, py_methods, MODULE_DOCS); }
#define PARSE_FUNC(mn) PyMODINIT_FUNC PARSE_NAME(mn)
#endif

PARSE_FUNC(MODULE_NAME);
