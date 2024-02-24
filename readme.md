open.py 启动器程序

cloud.py 主程序人口

# 打包指南

--follow-imports 会将所有依赖的库打包进exe(可选)

### 打包命令(完整包)

`nuitka --mingw --standalone --show-progress --windows-disable-console --output-dir=../out xxx.py`

### 打包命令(仅exe)

`nuitka --mingw --windows-disable-console --output-dir=../out xxx.py`