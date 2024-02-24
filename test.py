import re

# 定义待匹配的字符串
text = "cloud://code=u6i88qc1nja7g7eh&pwd=/"

# 定义正则表达式模式
pattern = r"code=([^&]+)&pwd=([^/]*[^&]*)"

# 使用re模块的findall方法进行匹配
matches = re.findall(pattern, text)

# 输出匹配结果
if matches:
    print(matches)
    code, pwd = matches[0]
    print("Code:", code)
    print("Password:", pwd)
else:
    print("No matches found.")