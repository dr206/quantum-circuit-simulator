from setuptools import find_packages, setup
setup(
    name='quantumcircuitsimulator',
    packages=find_packages(include=['quantumcircuitsimulator']),
    version='0.1.0',
    description='A circuit based quantum simulator.',
    author='Daniel Reilly',
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
