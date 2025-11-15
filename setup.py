from setuptools import setup, find_packages

setup(
    name="techguru",
    version="0.1.0",
    description="TechGuru - AI pair-programmer mentor",
    packages=find_packages(exclude=("tests", "notebooks", "demo", "data", ".github")),
    include_package_data=True,
)
