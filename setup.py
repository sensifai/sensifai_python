from setuptools import setup, find_packages

setup(
    name="sensifai",
    version="0.2.1",
    license='apache-2.0',
    description="Sensifai API Python Client",
    packages=find_packages(exclude=["docs", "tests"]),
    extras_require=dict(reST="Docutils>=0.14"),
    
    maintainer='Rahman yousefzadeh',
    maintainer_email='r.y.zadeh@Sensifai.com',
    url='https://github.com/sensifai/sensifai_python',
    author_email='api@sensifai.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: Apache Software License'
    ],
    keywords='Sensofai; Video Recognition; ',
    python_requires='>=3',
    
)
