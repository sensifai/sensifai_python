from setuptools import setup, find_packages

setup(
    name="sensifai_python",
    version="0.0.1",
    description="Sensifai API Python Client",
    packages=find_packages(exclude=["docs", "tests"]),
    extras_require=dict(reST="Docutils>=0.14")
)
