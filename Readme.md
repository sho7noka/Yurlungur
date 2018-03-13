# Yurlungur
Meta programming wrapper for Maya, Houdini and 3dsMax and more.

## summary
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tools, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.

## future
* HOM (Houdini object Model) like command wrapper.
* PySide & PyQt shorten accessor.
* Useful py-snippet for technical artist.

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
    
    ```python
    # python
    import yurlungur as yr
    yr.YNode("hoge").attr(0)
    ``` 

## License
Yurlungur is MIT License.
