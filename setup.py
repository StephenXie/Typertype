from setuptools import setup, find_packages
import re
import os

# def get_version(package):
#     with open(os.path.join(package, "__init__.py")) as f:
#         return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setup(
    name="typertype",
    version="0.0.1",
    url="https://github.com/StephenXie/Typertype",
    license="GNU_v3",
    author="Stephen Xie",
    author_email="xiepin225@gmail.com",
    description="An offline, customizable, feature-rich, typing app",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['type', 'typing', 'offline', 'customizable'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    requires = [],
    install_requires=[],
    zip_safe=False,
)
