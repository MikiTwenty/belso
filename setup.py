import os
from setuptools import setup, find_packages

def read_version() -> str:
    """
    Reads the __version__ from belso/version.py\n
    ---
    ### Returns
    - `str`: The version string.
    """
    version_path = os.path.join("belso", "version.py")
    with open(version_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().replace('"', '').replace("'", "")
    raise RuntimeError("Version not found")

VERSION = read_version()

with open("requirements.txt") as requirements:
    requirements = requirements.read().splitlines()

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name = "belso",
    version = VERSION,
    description = "Better LLMs Structured Outputs",
    author = "Michele Ventimiglia",
    author_email = "michele.ventimiglia01@gmail.com",
    license = "MIT",
    url="https://github.com/MikiTwenty/belso",
    packages = find_packages(exclude=["tests", "tests.*"]),
    include_package_data = True,
    python_requires=">=3.10",
    install_requires = requirements,
    zip_safe = False,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
)
