from setuptools import setup, find_packages

text = """
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.
"""

setup(
    name='yurlungur',
    version='0.9.1',
    package_dir={"" : "yurlungur"},
    packages=find_packages(where="yurlungur", exclude=["*.pyc"]),
    url='https://sho7noka.github.io/Yurlungur/',
    license='MIT',
    author='sho7noka',
    author_email='shosumioka@gmail.com',
    platforms="any",
    description='universal scripting environment with Python which Maya, Houdini and Unreal.',
    long_description=text,
    test_suite='tests',
    keywords=['maya', '3d', 'graphics', 'Game', 'VFX', 'CG', 'houdini', "unreal"],
)