#!/usr/bin/env python3
"""
批量删除指定路径下特定后缀的文件
支持大量文件的高效处理

Author:  Wei Bai
Last Modified: 2025-11-03
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List


def find_files_by_extension(directory: str, extension: str, recursive: bool = False) -> List[Path]:
    """查找指定后缀的文件"""
    path = Path(directory)
    
    if not path.exists():
        raise ValueError(f"路径不存在: {directory}")
    
    if not path.is_dir():
        raise ValueError(f"不是有效的目录: {directory}")
    
    # 确保扩展名格式正确
    if not extension.startswith('.'):
        extension = '.' + extension
    
    files = []
    pattern = f"**/*{extension}" if recursive else f"*{extension}"
    
    print(f"正在扫描文件...")
    for file_path in path.glob(pattern):
        if file_path.is_file():
            files.append(file_path)
            # 每1000个文件显示一次进度
            if len(files) % 1000 == 0:
                print(f"已找到 {len(files)} 个文件...")
    
    return files


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def delete_files(files: List[Path], batch_size: int = 100, dry_run: bool = False) -> tuple:
    """删除文件列表"""
    total_size = 0
    deleted_count = 0
    failed_files = []
    
    for i, file_path in enumerate(files, 1):
        try:
            file_size = file_path.stat().st_size
            
            if not dry_run:
                file_path.unlink()
            
            total_size += file_size
            deleted_count += 1
            
            # 每100个文件显示一次进度
            if i % batch_size == 0:
                action = "将删除" if dry_run else "已删除"
                print(f"{action} {i}/{len(files)} 个文件...")
                
        except Exception as e:
            failed_files.append((str(file_path), str(e)))
            print(f"删除失败: {file_path} - {e}")
    
    return deleted_count, total_size, failed_files


def main():
    parser = argparse.ArgumentParser(
        description='批量删除指定路径下特定后缀的文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  # 删除 C:\\temp 目录下所有 .tmp 文件（不含子目录）
  python %(prog)s C:\\temp .tmp
  
  # 递归删除 C:\\logs 目录及子目录下所有 .log 文件
  python %(prog)s C:\\logs .log -r
  
  # 预览模式（不实际删除）
  python %(prog)s C:\\temp .tmp --dry-run
  
  # 不需要确认直接删除
  python %(prog)s C:\\temp .tmp -y
        '''
    )
    
    parser.add_argument('path', help='要搜索的目录路径')
    parser.add_argument('extension', help='文件扩展名（如 .tmp 或 tmp）')
    parser.add_argument('-r', '--recursive', action='store_true',
                        help='递归搜索子目录')
    parser.add_argument('-y', '--yes', action='store_true',
                        help='跳过确认，直接删除')
    parser.add_argument('--dry-run', action='store_true',
                        help='预览模式，不实际删除文件')
    parser.add_argument('--batch-size', type=int, default=100,
                        help='进度显示的批次大小（默认: 100）')
    
    args = parser.parse_args()
    
    try:
        # 查找文件
        print(f"搜索路径: {args.path}")
        print(f"文件后缀: {args.extension}")
        print(f"递归搜索: {'是' if args.recursive else '否'}")
        print("-" * 60)
        
        files = find_files_by_extension(args.path, args.extension, args.recursive)
        
        if not files:
            print("未找到匹配的文件。")
            return 0
        
        # 计算总大小
        total_size = sum(f.stat().st_size for f in files)
        
        print(f"\n找到 {len(files)} 个文件，总大小: {format_size(total_size)}")
        
        # 显示前10个文件作为示例
        if len(files) <= 10:
            print("\n文件列表:")
            for f in files:
                print(f"  - {f}")
        else:
            print(f"\n前10个文件示例:")
            for f in files[:10]:
                print(f"  - {f}")
            print(f"  ... 还有 {len(files) - 10} 个文件")
        
        # 确认删除
        if args.dry_run:
            print("\n[预览模式] 将执行删除操作（实际不会删除）")
        elif not args.yes:
            print("\n" + "=" * 60)
            response = input("确认要删除这些文件吗？(yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("操作已取消。")
                return 0
        
        # 删除文件
        print("\n开始删除...")
        deleted_count, deleted_size, failed_files = delete_files(
            files, args.batch_size, args.dry_run
        )
        
        # 显示结果
        print("\n" + "=" * 60)
        action = "将删除" if args.dry_run else "已删除"
        print(f"{action} {deleted_count} 个文件，释放空间: {format_size(deleted_size)}")
        
        if failed_files:
            print(f"\n失败的文件数: {len(failed_files)}")
            print("失败详情:")
            for file_path, error in failed_files[:10]:
                print(f"  - {file_path}: {error}")
            if len(failed_files) > 10:
                print(f"  ... 还有 {len(failed_files) - 10} 个失败")
        
        if args.dry_run:
            print("\n[预览模式] 未实际删除任何文件")
        else:
            print("\n删除完成！")
        
        return 0 if not failed_files else 1
        
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
