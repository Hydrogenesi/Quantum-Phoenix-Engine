"""Setup configuration for Quantum Phoenix Engine package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantum-phoenix-engine",
    version="1.0.0",
    author="James Stanley",
    description="Two Operators, Two Laws Per Step — Quantum Phoenix Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hydrogenesi/Quantum-Phoenix-Engine",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "phoenix=quantum_phoenix.cli:main",
        ],
    },
)
