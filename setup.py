from pathlib import Path

from setuptools import find_packages, setup

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="django-recaptcha3",
    version="0.1.0",
    author="Andrea Briganti",
    author_email="kbytesys@gmail.com",
    maintainer="buswedg",
    maintainer_email="buswedg@djangomango.com",
    url="https://github.com/djangomango/django-recaptcha3",
    license="GNU Lesser General Public License v2 (LGPLv2)",
    description="Django reCAPTCHA v3 form field, widget, and template tags.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
        "requests>=2.28",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.10",
)
