from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aibug",
    version="0.1.0",
    author="Tony Cai",
    author_email="tonytasks@gmail.com",
    description="Intelligent Bug Tracking CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonycai/AIBugReport",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Bug Tracking",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "mysql-connector-python>=8.0.0",
        "pinatapy-unofficial>=0.1.0",
        "click>=8.0.0",
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "aibug=aibug.cli:main",
        ],
    },
)