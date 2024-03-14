

# pyinstall 打包指南

pyinstaller -i .\app\Resource\logo.ico .\cloud.py

(不含dos窗口)

pyinstaller -i .\app\Resource\logo.ico -w .\cloud.py


# nuitka打包指南

--follow-imports 会将所有依赖的库打包进exe(可选)

### 打包命令(完整包) cloud.py

dev
`nuitka --standalone --mingw64 --show-progress --nofollow-imports --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../dev cloud.py`

release
`nuitka --windows-disable-console --standalone --mingw64 --show-progress --nofollow-imports --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../release --windows-icon-from-ico=./app/Resource/logo.ico cloud.py`

### 打包命令(仅exe)

dev
`nuitka --mingw64  --show-progress --nofollow-imports --plugin-enable=pyqt5 -follow-import-to=app --output-dir=../dev cloud.py`

release
`nuitka --windows-disable-console --mingw64 --show-progress --nofollow-imports --plugin-enable=pyqt5 --follow-import-to=app --output-dir=../release --windows-icon-from-ico=./app/Resource/logo.ico cloud.py`


