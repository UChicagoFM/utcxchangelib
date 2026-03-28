from setuptools import setup, find_packages

setup(
    name='utcxchangelib',
    version='0.2.0',
    author='UTC',
    author_email='',
    description='Client library for 2026 UTC Xchange',
    packages=['utcxchangelib'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'protobuf>=6.31.1',
        'grpcio>=1.78.0',
        'grpcio-tools>=1.78.0',
    ]
)
