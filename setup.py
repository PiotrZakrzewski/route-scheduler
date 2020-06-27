import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="route-scheduler-pmzakrzewski",
    version="1.0.0",
    author="Piotr Zakrzewski",
    author_email="crvc-no-reply@protonmail.com",
    description="A toy route scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PiotrZakrzewski/route-scheduler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
