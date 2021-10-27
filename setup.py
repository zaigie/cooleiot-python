import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="cooleiot",                  # 包名称
    version="0.0.5",                                   # 包版本
    author="CoolE IoT",                           # 作者
    license='MIT',                                     # 协议简写
    author_email="jokerwho@yeah.net",                 # 作者邮箱
    description="CoolEIoT Python Library",             # 工具包简单描述
    long_description=long_description,                 # readme 部分
    long_description_content_type="text/markdown",     # readme 文件类型
    install_requires=[
    'requests>=2.22.0',
    'urllib3>=1.25.3',
    'paho-mqtt>=1.6.1'
    ],
    url="https://github.com/jokerwho/cooleiot-python",       # 包的开源链接
    packages=setuptools.find_packages(),               # 不用动，会自动发现
    classifiers=[                                      # 给出了指数和点子你的包一些额外的元数据
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)