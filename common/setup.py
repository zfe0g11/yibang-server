from setuptools import setup, find_packages

setup(
    name="sky-common",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyjwt>=2.8.0",
        "requests>=2.31.0",
        "oss2>=2.18.0"
    ],
    description="苍穹外卖通用工具模块",
    author="Sky Take Out Team",
    author_email="support@skytakeout.com"
)