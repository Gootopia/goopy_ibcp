import setuptools
setuptools.setup(name='goopy_ibcp',
version='1.0',
description='Goo configuration module based on configObj library',
url='#',
author='goo',
install_requires=['loguru', 
                  'overrides', 
                  'websockets', 
                  'requests'
                  'urllib3'],
author_email='',
packages=setuptools.find_packages(),
zip_safe=False)