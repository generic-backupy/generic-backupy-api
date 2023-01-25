import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gb_module",                     # This is the name of the package
    version="0.0.2",                        # The initial release version
    author="Martin Rader",                     # Full name of the author
    description="Generic Backupy Module Library",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',    # Directory of the source code of the package
    install_requires=["selenium>=4.7.2,<5.0"]                     # Install other dependencies if any
)
