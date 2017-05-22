from distutils.core import setup

setup(
    name='PyDCC',
    version='0.9',
    packages=['PyDCC.src', 'tests', 'pybinary', 'cameraFrustumTools.v1', 'cameraFrustumTools.v1.OBB',
              'cameraFrustumTools.v1.OBB.shelf'],
    url='',
    license='MIT',
    author='sumioka-sho',
    author_email='shosumioka@gmail.com',
    description='MEL and MaxScript Python wrapper andmore.'
)
