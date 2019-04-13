from setuptools import setup

text = """
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.
"""

setup(
    name='yurlungur',
    version="0.9.5",
    url='https://sho7noka.github.io/Yurlungur/',
    license='MIT',
    author='sho7noka',
    author_email='shosumioka@gmail.com',
    platforms="any",
    description='universal scripting environment with Python which Maya, Houdini and Blender.',
    long_description=text,
    keywords=['maya', '3d', 'graphics', 'Game', 'VFX', 'CG', 'houdini', "unreal"],

    packages=["yurlungur"],
    include_package_data=True,
    test_suite='test'
)
