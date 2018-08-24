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
    yurlungur.log(width.value)



__getitem__ によるアクセスもサポートしているため、
ユーザー側が今操作しているオブジェクトの状態を気にすることなく
はじめからそのプロパティを持っていたかのように振る舞います。

.. code-block:: python

    width = obj.width
    yr.log(width.value)

    width.set(700)


gui
--------------------------------
Qt.py

.. code-block:: python

    yurlungur.YFile.load()

    yurlungur.YFile.save()



Alembic や FBX など汎用ファイルフォーマットのサポートは
アプリケーションに依存します。(例えばゲームエンジンでは、一般的なファイルエクスポート機能はサポートされません)
staticベースによる実装がyurlungur.command モジュールにまとめられています。


基本となるAPIはここで終わりです。