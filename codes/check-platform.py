# 檢查是否在 macOS 平台
import platform

if platform.system() == 'Darwin':  # Darwin 是 macOS 的系統名稱
    print("This is macOS")
else:
    print("This is not macOS")

if platform.system() == 'Windows':
    print("This is Windows")
else:
    print("This is not Windows")

if platform.system() == 'Linux':
    print("This is Linux")
else:
    print("This is not Linux")


