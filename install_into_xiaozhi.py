#!/usr/bin/env python3
"""
把 robot-s3-n16r8 自定义板卡安装到小智官方 xiaozhi-esp32 v2.4.0 源码。

用法：
    python install_into_xiaozhi.py D:\xiaozhi-esp32-2.4.0

Linux/macOS:
    python3 install_into_xiaozhi.py ~/xiaozhi-esp32-2.4.0
"""

from pathlib import Path
import argparse
import shutil
import sys


BOARD_NAME = "robot-s3-n16r8"
KCONFIG_SYMBOL = "BOARD_TYPE_ROBOT_S3_N16R8"


def patch_kconfig(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    if KCONFIG_SYMBOL in text:
        print("Kconfig.projbuild 已包含机器人板卡，跳过。")
        return False

    marker = '    config BOARD_TYPE_BREAD_COMPACT_WIFI\n'
    addition = (
        '    config BOARD_TYPE_ROBOT_S3_N16R8\n'
        '        bool "DIY Robot ESP32-S3-N16R8"\n'
        '        depends on IDF_TARGET_ESP32S3\n'
    )

    if marker not in text:
        raise RuntimeError(
            "无法在Kconfig.projbuild中找到插入位置。"
            "请确认使用的是xiaozhi-esp32 v2.4.0。"
        )

    text = text.replace(marker, addition + marker, 1)
    path.write_text(text, encoding="utf-8")
    print("已修改 main/Kconfig.projbuild")
    return True


def patch_cmake(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")

    if "CONFIG_BOARD_TYPE_ROBOT_S3_N16R8" in text:
        print("CMakeLists.txt 已包含机器人板卡，跳过。")
        return False

    marker = 'if(CONFIG_BOARD_TYPE_BREAD_COMPACT_WIFI)\n'
    replacement = (
        'if(CONFIG_BOARD_TYPE_ROBOT_S3_N16R8)\n'
        '    set(BOARD_TYPE "robot-s3-n16r8")\n'
        '    set(BUILTIN_TEXT_FONT font_noto_sans_basic_14_1)\n'
        '    set(BUILTIN_ICON_FONT font_material_symbols_14_1)\n'
        'elseif(CONFIG_BOARD_TYPE_BREAD_COMPACT_WIFI)\n'
    )

    if marker not in text:
        raise RuntimeError(
            "无法在CMakeLists.txt中找到插入位置。"
            "请确认使用的是xiaozhi-esp32 v2.4.0。"
        )

    text = text.replace(marker, replacement, 1)
    path.write_text(text, encoding="utf-8")
    print("已修改 main/CMakeLists.txt")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "xiaozhi_source",
        help="xiaozhi-esp32 v2.4.0源码目录"
    )
    args = parser.parse_args()

    source_root = Path(args.xiaozhi_source).expanduser().resolve()
    main_dir = source_root / "main"

    if not (source_root / "CMakeLists.txt").exists():
        print("错误：指定目录不像xiaozhi-esp32源码根目录。")
        return 2

    if not (main_dir / "Kconfig.projbuild").exists():
        print("错误：缺少 main/Kconfig.projbuild。")
        return 2

    package_root = Path(__file__).resolve().parent
    source_board = (
        package_root /
        "board_files" /
        "main" /
        "boards" /
        BOARD_NAME
    )
    target_board = main_dir / "boards" / BOARD_NAME

    if not source_board.exists():
        print("错误：安装包中的板卡文件缺失。")
        return 2

    if target_board.exists():
        backup = target_board.with_name(target_board.name + ".backup")
        if backup.exists():
            shutil.rmtree(backup)
        shutil.copytree(target_board, backup)
        shutil.rmtree(target_board)
        print(f"旧板卡已备份到：{backup}")

    shutil.copytree(source_board, target_board)
    print(f"板卡文件已复制到：{target_board}")

    patch_kconfig(main_dir / "Kconfig.projbuild")
    patch_cmake(main_dir / "CMakeLists.txt")

    print()
    print("安装完成。下一步在ESP-IDF 6.0.2终端执行：")
    print(f'  cd "{source_root}"')
    print("  idf.py set-target esp32s3")
    print("  idf.py menuconfig")
    print()
    print("menuconfig中选择：")
    print("  Xiaozhi Assistant")
    print("    Board Type")
    print("      DIY Robot ESP32-S3-N16R8")
    print()
    print("然后执行：")
    print("  idf.py build")
    print("  idf.py -p COM3 flash monitor")
    return 0


if __name__ == "__main__":
    sys.exit(main())
