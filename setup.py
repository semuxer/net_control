import sys
from cx_Freeze import setup, Executable

from version import ver

version = ver()
version.incbuild()

build_exe_options = {
    "packages": ["wx"],
    # Перечислите дополнительные файлы, если они есть
    "include_files": ["config.json", "version.json", "net24.ico", "error.mp3"],
}

icon_path = "net24.ico"
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Задаем base как Win32GUI для скрытия консоли на Windows


setup(
    name="Перевірка зв'язку",
    version=f"{version.getver()}",
    description="Контроль зв'язку",
    options={"build_exe": build_exe_options},
    executables=[Executable("net_control.py", base=base, icon=icon_path)]
)
