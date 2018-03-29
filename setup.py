"""resourceful."""
from setuptools import find_packages, setup


setup(
    name='resourceful',
    version='0.2',
    url='https://github.com/caxiam/resourceful',
    license='Apache Version 2.0',
    author='Colton Allen',
    author_email='colton.allen@caxiam.com',
    long_description=__doc__,
    packages=find_packages(exclude=("test*", )),
    package_dir={'resourceful': 'resourceful'},
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests'
)
