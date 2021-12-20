import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="bookstore",
    version="0.0.1",
    description="Buy Books Online",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.shuishan.net.cn/Contemporary_DMS.ZHOU_Xuan.2021Fall.DaSE/CDMS_PJ2_10195501437",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
)
