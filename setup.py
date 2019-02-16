import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="restful_userservice",
    version="0.0.1",
    author="Michael Borko",
    author_email="mborko@tgm.ac.at",
    description="Restful User-Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TGM-HIT/simple-user-database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

