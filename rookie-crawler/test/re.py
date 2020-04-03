import re
import os

if __name__ == '__main__':
    content = "Xiaoshuaib has 100 bananas"
    res = re.match('^Xi.*(\d+)\s.*s$', content)
    print(res.group(1))
    print(os.getcwd())

