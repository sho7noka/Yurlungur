===================================
API
===================================
yurlungur foundations.


instance
--------------------------------

.. code-block:: python

    # 標準ではPython
    import yurlungur as yr

    obj = yr.YObject("defaultResolution")

    # or

    node = yr.YNode("defaultResolution")


YNode is eble to initialize that is subclass for YObject.
You have to str object.

.. code-block:: python

    node = yr.YNode(obj.name)



attribute
--------------------------------
Object based container.

.. code-block:: python

    width = obj.attr("width") # object YAttr

    # or

    width = obj.width


    yr.log(width.value)

    width.set(700)


gui
--------------------------------
Qt.py

.. code-block:: python

    widget = QWidget()
    yr.qt.show(widget)

