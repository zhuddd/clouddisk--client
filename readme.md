ui库：https://github.com/zhiyiYo/PyQt-Fluent-Widgets



open.py 启动器程序

cloud.py 主程序人口

# 打包指南

--follow-imports 会将所有依赖的库打包进exe(可选)

### 打包命令(完整包) cloud.py

`nuitka --standalone --mingw64 --show-progress --nofollow-imports --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../out/dev cloud.py`

`nuitka --standalone --windows-disable-console --mingw64 --nofollow-imports --show-progress --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../out/r --windows-icon-from-ico=./app/Resource/logo.ico cloud.py`

### 打包命令(完整包) open.py

`nuitka --standalone --mingw64 --show-progress --output-dir=../out/dev open.py`

`nuitka --standalone --windows-disable-console --mingw64 --show-progress --output-dir=../out/r open.py`


### 打包命令(仅exe)

`nuitka --mingw --windows-disable-console --output-dir=../out xxx.py`

`nuitka --windows-disable-console --mingw64 --nofollow-imports --show-progress --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../out/r --windows-icon-from-ico=./app/Resource/logo.ico cloud.py`
