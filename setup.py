"""The setup script."""

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

install_requirements = [
    "requests",
    "pandas",
    "tqdm",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="João Vitor F. Cavalcante",
    author_email="jvfe@ufrn.edu.br",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python utility to reconcile Pandas DataFrames",
    install_requires=install_requirements,
    license="BSD license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="tabular wikidata opendata linked-data",
    name="reconciler",
    packages=find_packages(include=["reconciler", "reconciler.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jvfe/reconciler",
    project_urls={
        "Bug Tracker": "https://github.com/jvfe/reconciler/issues",
        "Documentation": "https://jvfe.github.io/reconciler/",
        "Source Code": "https://github.com/jvfe/reconciler",
    },
    version="0.2.1",
    zip_safe=False,
)
