import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyembroidery",
    version="1.4.1",
    author="Tatarize",
    author_email="tatarize@gmail.com",
    description="Embroidery IO library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmbroidePy/pyembroidery",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)