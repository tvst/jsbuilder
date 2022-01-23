import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsbuilder",
    version="0.1.1",
    author="Thiago Teixeira",
    author_email="me@thiagot.com",
    description="Convert Python code to JavaScript strings, just by decorating it with @js!",
    license="Apache 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tvst/jsbuilder",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["iteration_utilities"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
