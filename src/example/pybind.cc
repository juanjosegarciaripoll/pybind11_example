#include <pybind11/pybind11.h>

namespace py = pybind11;

struct MyStructure {

  double some_value{0.123};

  double get_some_value() const { return some_value; }
};

PYBIND11_MODULE(pybind, m) {
  py::class_<MyStructure>(m, "MyStructure")
      .def(py::init())
      .def("get_some_value", &MyStructure::get_some_value)
      .def_readwrite("some_value", &MyStructure::some_value);
};
