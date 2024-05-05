cdef class MyCythonStructure:
    cdef double value

    def __init__(self):
        self.value = 0.123

    def get_some_value(self):
        return self.value
