from setuptools import setup

setup(
    name="moja_tools",
    version="0.0.01",
    author="shogo314",
    description="tools for MojaCoder",
    package_dir={"moja_tools": "moja_tools"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mjtools = src.main:main"
        ]
    }
)
