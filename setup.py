from setuptools import setup, find_packages

setup(
    # metadata
    name='chembo', 
    version='1.0', 
    description="Chembo testing",
    author="Stefan Pricopie",
    author_email="stefan.pricopie@postgrad.manchester.ac.uk",

    # options
    packages=find_packages(),
    package_dir="src"
)