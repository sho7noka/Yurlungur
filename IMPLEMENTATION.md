# Native imprimentations

## なぜ
- インハウスツールの拡張性は低い傾向にある
- DCCツールの操作に詳しいエンジニアは希少
- 小さな連携のためにSDKとドキュメントを読むのが面倒

緊密な統合に関してはそれぞれのSDKを読み込む必要があります。

ネイティブからapiコール
pluginパッケージから読み取り

### embeded.h
- (埋込) エディタ(dll)内にCapiを組み込む
- Python インタープリター不要
- 競合他社間のソフトウェア統合

```makefile
cmake_minimum_required(VERSION 3.0)
project(yurlungur)

find_package(pybind11 REQUIRED)  # or add_subdirectory(pybind11)

add_executable(yurlungur main.cpp)
target_link_libraries(yurlungur PRIVATE pybind11::embed)
```

```cpp
#include <pybind11/embed.h>
#include <yurlungur/embeded.h>

namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(cpp_module, m) {
    m.attr("a") = 1;
}

int main() {
    py::scoped_interpreter guard{};

    auto py_module = py::module::import("py_module");

    auto locals = py::dict("fmt"_a="{} + {} = {}", **py_module.attr("__dict__"));
    assert(locals["a"].cast<int>() == 1);
    assert(locals["b"].cast<int>() == 2);

    py::exec(R"(
        c = a + b
        message = fmt.format(a, b, c)
    )", py::globals(), locals);

    assert(locals["c"].cast<int>() == 3);
    assert(locals["message"].cast<std::string>() == "1 + 2 = 3");
}
```

```python
"""py_module.py located in the working directory"""
import cpp_module

a = cpp_module.a
b = a + 1
```


### extension.h
- (拡張) SDKをPython Capiから呼び出す
- 内蔵インタプリタのイニシャライズが必要
- pybind11 のラッパー

```makefile
cmake_minimum_required(VERSION 3.0)
project(example)

add_subdirectory(pybind11)
pybind11_add_module(example example.cpp)
```

```cpp
#include "string"

class Node {
    Node(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
};

struct File {
    void import(const std::string file_name);
    void export(const std::string file_name);

    std::string path;
}

struct Shell {

}

```

```cpp
#include <pybind11/pybind11.h>
#include <yurlungur/extension.h>

namespace py = pybind11;

PYBIND11_MODULE(example, m) {
    py::class_<Node>(m, "Node")
        .def(py::init<const std::string &>())
        .def("setName", &Node::setName)
        .def("getName", &Node::getName);

    py::class_<File>(m, "File")
        .def("import", $File::import);
}
```

#### sample
- [Qt C++]()
- [C# DllImport]()

#### misc
- http://hhsprings.pinoko.jp/site-hhs/2015/03/pythonには縁もゆかりもないccをdistutilsでビルドする/
- https://docs.python.org/ja/3/extending/building.html