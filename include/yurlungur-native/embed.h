//
// Created by sho sumioka on 西暦 2019/10/29.
//

#ifndef YURLUNGUR_EMBED_H
#define YURLUNGUR_EMBED_H

//https://pybind11.readthedocs.io/en/stable/classes.html
//$ c++ -O3 -Wall -shared -std=c++11 -fPIC python3 -m pybind11 --includes yurlungur.cpp -o yurlungurpython3-config --extension-suffix
# include <pybind11/pybind11.h>

struct Pet {
    enum Kind {
        Dog = 0,
        Cat
    };

    Pet(const std::string &name, Kind type) : name(name), type(type) {}

    std::string name;
    Kind type;
};

namespace py = pybind11;

PYBIND11_MODULE(yurlungur, m
) {
py::class_ <Pet> pet(m, "Pet");

pet.

def (py::init<const std::string &, Pet::Kind>())

.def_readwrite("name", &Pet::name)
.def_readwrite("type", &Pet::type);

py::enum_<Pet::Kind>(pet,
"Kind")
.value("Dog", Pet::Kind::Dog)
.value("Cat", Pet::Kind::Cat)
.

export_values();

}

#endif //YURLUNGUR_EMBED_H
