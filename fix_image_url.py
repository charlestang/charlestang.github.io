#!/usr/bin/python3

import os
import sys
import re

# 图片可能是这样的：![image](https://sexywp.com/wp-content/uploads/2019/12/1-1.jpg)
# 图片也可能是这样的：[![](https://sexywp.com/wp-content/uploads/2019/12/1-1.jpg)](https://sexywp.com/wp-content/uploads/2019/12/1-1.jpg)
# 也即外面套了一层链接
image_pattern = re.compile(r"\[(?:(\!\[(?:.*)\))|(.*?))\]\((.*?)\)|!\[(.*?)\]\((.*?)\)")
base_url = "https://sexywp.com/wp-content/uploads"

def process_image_repl(filename):
    def image_repl(match):
        # 匹配到了图片的链接
        if match.group(0).startswith("!"):
            # print('图片链接：', match.group(0))
            if match.group(5).startswith(base_url):
                #print('替换：', match.group(5).replace(base_url, '../images'))
                print('处理文件：', filename)
                return f"![{match.group(4)}]({match.group(5).replace(base_url, '../images')})"
            else:
                #print('不用替换：', match.group(0))
                return f"![{match.group(4)}]({match.group(5)})"
        else:
            if match.group(1):
                #print('图片外面套链接，递归处理:', match.group(0))
                img = image_pattern.sub(image_repl, match.group(1))
                #print('替换：', img)
                if match.group(3).startswith(base_url):
                    return f"{img}"
                else:
                    return f"[{img}]({match.group(3)})"
            else:
                #print('普通链接')
                #print('不用替换：', match.group(0))
                return f"[{match.group(2)}]({match.group(3)})"
    return image_repl

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_image_url.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    
    for filename in os.listdir(path):
        if filename.endswith(".md"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r+") as f:
                content = f.read()
                content = re.sub(image_pattern, process_image_repl(filename), content)
                f.seek(0)
                f.write(content)
                f.truncate()
