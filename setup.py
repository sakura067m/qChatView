from setuptools import setup

requirements = [
    "PyQt5>=5.8.2",  # TBD
]

setup(
    name="qChatView",  # TBC
    version="1.0.0",
    description="show your messages like a chat",
    url="https://github.com/sakura067m/qChatView",
    author="sakura067m",
    author_email="3IE19001M@s.kyushu-u.ac.jp",
##    license='',  # TBD
    py_modules=["qChatView"],
    install_requires=requirements,
    keywords="chat",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
    ],
)
