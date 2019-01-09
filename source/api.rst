===================================
API Foundation
===================================
Yurlungur foundations.

基本となるコンセプトは、Pythonインターフェースによるシュガーシンタックスです。
Object(Node) クラス、Attribute クラス、File クラスの基本を知れば、
汎用的な操作ができる設計になっています。


それぞれのオブジェクトのスコープは以下の通りです。

#. Where = Object
#. What = Node
#. How = Attribute

modules:

.. toctree::
    :maxdepth: 2

    modules



Object & Node
--------------------------------
数多くの3Dアプリケーションも、APIのレベルではノードベースとスタックベースに分けることができます。

UnityはComponent、BlenderはModifierでオブジェクトの振る舞いを制御しますが、
Maya や Houdini といったノードベースのアプリケーションでは、接続する同士の相互作用によって
全体の振る舞いを制御します。

前者のスタックベースのアプリケーションを使う際には YObject、
後者のノードベースのアプリケーションを使う際には YNode　がインターフェースの
デザインとして違和感なく使うことが出来ます。

アプリケーションが持つ性質を意識して、
Node と Object をそれぞれ使いわけてプログラミングすると良いでしょう。


.. code-block:: python

    # 標準ではPython
    import yurlungur as yr

    obj = yr.YObject("defaultResolution")

    # or

    node = yr.YNode("defaultResolution")


YNode is eble to initialize that is subclass for YObject.
You have to str object.
Node オブジェクトのみ connection 関係のメソッドを複数持つ

.. code-block:: python

    node = yr.YNode(obj.name)



Attribute
--------------------------------
Object based container.
これはPyMELをベースにした柔軟なAttributeクラスです。
すべてオブジェクトで扱えるようにアプリケーション間の戻値をラップしています。
これは、getter / setter のインターフェースは、アプリケーション間で異なるためです・

attr("str") は文字列ベースのアクセスになるので、予め文字列要素で構成した
リストを準備すれば短く書くことができるでしょう。

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



Attribute クラスをわざわざ別設計したように、戻り値はすべてオブジェクトです。
引数に渡したり set するためには、value プロパティを使って、基本データ型に変更する
必要があります。


File
--------------------------------
現在のスタンダードはアプリケーション間のデータストリームですが、
ファイルIOを一つのインターフェースでまとめておくことは、
今後どのアプリケーションを使う上でも役に立つものでしょう。

.. code-block:: python

    yurlungur.YFile.load()

    yurlungur.YFile.save()



Alembic や FBX など汎用ファイルフォーマットのサポートは
アプリケーションに依存します。(例えばゲームエンジンでは、一般的なファイルエクスポート機能はサポートされません)
staticベースによる実装がyurlungur.command モジュールにまとめられています。


GEOM オブジェクト
-------------------------------
Mesh オブジェクトとそれに連なるシェーダのコンテナオブジェクトです。
共通のデータ構造と各アプリケーション固有のプロシージャで構成されています。
YObject.geometry プロパティはイミュータブルです。
YObject.create()にGEOオブジェクトを渡すことでシーン内に生成できます。

meta オブジェクト経由で呼ぶことができるプロシージャを GEOM オブジェクト経由で
呼ぶメリットは、それがオブジェクトを継承するということです。
YObject 共通のインターフェースとGEOMオブジェクトによるデータアクセスをアプリケーション間の実装の
違いを意識せずに使うことが出来ます。

速度に不安がありますか？ネイティブのAPIをビルドしたモジュールをインポートすることが出来ます。
ext/setup.py を参照して下さい。

基本となるAPIはここで終わりです。