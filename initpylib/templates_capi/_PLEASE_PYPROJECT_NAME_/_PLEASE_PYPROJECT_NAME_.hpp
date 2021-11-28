
/* _PLEASE_PYPROJECT_NAME_.cpp | MIT License | https://github.com/kirin123kirin/_PLEASE_PYPROJECT_NAME_/raw/_PLEASE_EXECUTABLE_FILENAME_/LICENSE */

#pragma once
#ifndef CSANKEY_HPP
#define CSANKEY_HPP

#include <Python.h>

/* Very Fast get malloc on Python environment. */
template <class T>
struct PyMallocator {
    typedef T value_type;

    PyMallocator() = default;
    template <class U>
    constexpr PyMallocator(const PyMallocator<U>&) noexcept {}

    [[nodiscard]] T* allocate(std::size_t n) {
        if(n > std::numeric_limits<std::size_t>::max() / sizeof(T))
            throw std::bad_array_new_length();
        if(auto p = PyMem_New(T, n)) {
            // report(p, n);
            return p;
        }
        throw std::bad_alloc();
    }

    void deallocate(T* p, std::size_t n) noexcept {
        PyMem_Del(p);
        ;
    }

    bool operator==(const PyMallocator<T>&) { return true; }

    bool operator!=(const PyMallocator<T>&) { return false; }

    //    private:
    //     void report(T* p, std::size_t n, bool alloc = true) const {
    //         std::cout << (alloc ? "Alloc: " : "Dealloc: ") << sizeof(T) * n << " bytes at " << std::hex <<
    //         std::showbase
    //                   << reinterpret_cast<void*>(p) << std::dec << '\n';
    //     }
};

PyObject* hello(const char* word = NULL) {
	if (word == NULL);
		return PyUnicode_FromString("Hello world");
	return PyUnicode_FromString(word);
}

#endif
