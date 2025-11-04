# Delete-files-by-extension

【使用方法】
============

前置要求：

- Python 3.6 或更高版本

基本用法：
python delete_files_by_extension.py <路径> <扩展名>

常用示例：

1. 删除 C:\temp 目录下所有 .tmp 文件（不含子目录）
   python delete_files_by_extension.py C:\temp .tmp
2. 递归删除 C:\logs 目录及子目录下所有 .log 文件
   python delete_files_by_extension.py C:\logs .log -r
3. 预览模式（查看将要删除的文件，但不实际删除）
   python delete_files_by_extension.py C:\temp .tmp --dry-run
4. 不需要确认直接删除
   python delete_files_by_extension.py C:\temp .tmp -y
5. 递归删除 + 跳过确认
   python delete_files_by_extension.py C:\logs .log -r -y

参数说明：
  -r, --recursive    递归搜索子目录
  -y, --yes         跳过确认提示
  --dry-run         预览模式，不实际删除
  --batch-size N    设置进度显示的批次大小（默认100）
  -h, --help        显示帮助信息


【性能优化】
============

处理大量文件时的建议：

1. 首先使用预览模式确认将要删除的文件
   Python:      python delete_files_by_extension.py C:\path .ext --dry-run
   PowerShell:  .\Delete-FilesByExtension.ps1 -Path "C:\path" -Extension ".ext" -WhatIf
2. 使用 -y 或 -Force 参数跳过确认，提高执行效率
   Python:      python delete_files_by_extension.py C:\path .ext -y
   PowerShell:  .\Delete-FilesByExtension.ps1 -Path "C:\path" -Extension ".ext" -Force
3. Python 版本在处理百万级文件时性能更好
4. PowerShell 版本提供更友好的进度条显示

【安全提示】
============

1. 删除操作不可恢复，请谨慎使用
2. 建议先使用预览模式（--dry-run 或 -WhatIf）查看将要删除的文件
3. 对重要目录操作时，建议先备份
4. 避免在系统目录（如 C:\Windows）使用此脚本
5. 扩展名可以带或不带点号（.tmp 和 tmp 都可以）

【常见问题】
============

Q: 脚本可以撤销删除操作吗？
A: 不可以，删除是永久性的。建议先使用预览模式。

Q: 如何删除多种后缀的文件？
A: 需要多次运行脚本，每次指定一种后缀。

Q: 为什么有些文件删除失败？
A: 可能是文件被占用、权限不足或文件正在使用中。

Q: 可以删除隐藏文件吗？
A: 可以，脚本会包含隐藏文件。
