import re

a = "123.png"

b = re.search(r"\.+\w+", a)

print(b.group())