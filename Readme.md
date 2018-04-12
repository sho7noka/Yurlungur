# Yurlungur
universal scripting environment with Python which Maya, Houdini and Unreal.

## summary
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.

Yurlungur is inspired by [PyMEL](https://github.com/LumaPictures/pymel).

## future
* HOM (Houdini Object Model) like command wrapper.
* PySide & PyQt shorten accessor.
* Useful py-snippet for Game&Film technical artist.

### semantics

- Object
    ```lua
    -- MXS
    $.value = 0
    ```
    
    ```mel
    // MEL    
    setAttr "hoge" 0;
    ```
    
    ```python:yurlungur
    # python
    import yurlungur as yr
    yr.YNode("hoge").attr(0)
    ``` 

## TODO
- [x] basic api
- [ ] github.io
- [ ] transparency PNG
- [ ] unreal support

## contribution
WIP


## License
Yurlungur is MIT License.
