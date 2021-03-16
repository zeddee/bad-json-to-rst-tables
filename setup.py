from setuptools import setup, find_namespace_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="json2rst", # Replace with your own username
    version="0.0.1-dev",
    author="zed tan",
    author_email="zed@shootbird.work",
    description="Inelegant tool for converting JSON to rST list-tables",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/zeddee/bad-json-to-rst-tables",
    project_urls={
        "Bug Tracker": "https://github.com/zeddee/bad-json-to-rst-tables/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=find_namespace_packages(),
    python_requires=">=3.6",
)
