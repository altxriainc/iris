from setuptools import setup, find_packages

setup(
    name="iris-templates",
    version="0.1.1",
    description="A powerful template rendering engine with support for directives, includes, and dynamic context evaluation.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Altxria Inc.",
    author_email="company@altxria.com",
    url="https://github.com/altxriainc/iris",
    packages=[
        "altxria.iris"  
    ],
    package_dir={
        "altxria.iris": "src"  
    },
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
        ]
    },
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "iris=iris.cli:main",  
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    license="CC BY-ND 4.0", 
    keywords="template engine rendering includes directives",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/iris/issues",
        "Documentation": "https://github.com/yourusername/iris/wiki",
        "Source Code": "https://github.com/yourusername/iris",
    },
)
