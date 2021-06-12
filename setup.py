
#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
gas - 2021 - por jero98772
gas - 2021 - by jero98772
"""
from core.tools.webutils import genTokenFile
from setuptools import setup, find_packages
setup(
	name='B→FeelLog',
	version='1.0.0 beta',
	license='GPLv3',
	author_email='jero98772@protonmail.com',
	author='jero98772',
	description='web page to record expenses on a computer or on a cell phone through the web page, platform allows to register it immediately or in any time.records data in encrypted form, the database can be accessed and the encrypted data can be viewed.',
	url='https://jero98772.pythonanywhere.com/proyects/gas.html',
	packages=find_packages(),
    install_requires=['Flask','pycrypto'],
    include_package_data=True,
	)
genTokenFile("data/token.txt")