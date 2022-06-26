from setuptools import find_packages, setup
setup(
    name='fhui',
    packages=find_packages(),
    version='0.1.0',
    description='Mackie HUI control surface emuolation',
    author='Jamie Hardt',
    license='MIT',
    install_requires=['pygame', 'mido'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
