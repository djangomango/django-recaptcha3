from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='django-recaptcha3',
    version='0.1',
    author='Andrea Briganti',
    author_email='kbytesys@gmail.com',
    url='https://github.com/djangomango/django-recaptcha3',
    install_requires=[
        'requests'
    ],
    tests_require=[
        'django-setuptest'
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    license='GNU Lesser General Public License v3 (LGPLv3)',
    description='Django reCaptcha v3 field/widget',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3',
    packages=['django_recaptcha3'],
    include_package_data=True
)
