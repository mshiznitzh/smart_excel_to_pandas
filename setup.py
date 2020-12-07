import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smart_excel_to_pandas", # Replace with your own username
    version="0.0.1",
    author="Mike Howard",
    author_email="mshiznitzh@gmail.com",
    description="Takes a list of excel sheet then converts then to a dataframe saving them as a feather format to be used later",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)