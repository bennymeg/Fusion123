import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# see: https://packaging.python.org/tutorials/packaging-projects/
#      https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

setuptools.setup(
    name="123-Fusion",
    version="0.0.1",
    author="Benny Megidish",
    author_email="bennymegk@gmail.com",
    description="Converts 123D design CAD files into Fusion 360 CAD files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bennymeg/123-Fusion",
    packages=setuptools.find_packages(),
    scripts=['bin/123fusion'],
    # entry_points = {
    #     'console_scripts': ['123fusion=src.converter:main'],
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)