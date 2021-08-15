import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dandelion-tools",
    version="0.0.1",
    author="Riccardo Persello",
    author_email="riccardo.persello@icloud.com",
    description="Tools for programming Dandelion Core boards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dandelion-embedded/dandelion-tools",
    project_urls={
        "Bug Tracker": "https://github.com/dandelion-embedded/dandelion-tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["click", "rich", "pyserial", "timeout-decorator"],
    entry_points={
        "console_scripts": [
            "dandelion-tools = dandeliontools.main:cli",
        ],
    },
)
