import subprocess
import sys
from packaging.requirements import Requirement
from packaging.version import Version

def get_installed_packages():
    """Mengembalikan dictionary berisi nama paket dan versinya yang terinstal."""
    packages = {}
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if '==' in line:
                name, version = line.split('==')
                packages[name.lower()] = Version(version)
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan pip freeze: {e}")
    return packages

def check_requirements(requirements_file="requirements_versions.txt"):
    """
    Mengecek apakah semua requirement dalam file sudah terinstal dengan versi yang sesuai.
    Mengembalikan True jika semua sesuai, False jika ada yang tidak sesuai atau tidak terinstal.
    """
    installed_packages = get_installed_packages()
    needs_install = False
    try:
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        req = Requirement(line)
                        package_name = req.name.lower()
                        required_specifier = req.specifier

                        if package_name in installed_packages:
                            installed_version = installed_packages[package_name]
                            if not required_specifier.contains(installed_version):
                                print(f"Versi tidak sesuai: {package_name} (terinstal: {installed_version}, dibutuhkan: {required_specifier})")
                                needs_install = True
                        else:
                            print(f"Paket belum terinstal: {package_name} ({required_specifier})")
                            needs_install = True
                    except Exception as e:
                        print(f"Gagal memproses baris '{line}' di {requirements_file}: {e}")
                        needs_install = True
    except FileNotFoundError:
        print(f"File {requirements_file} tidak ditemukan.")
        needs_install = True

    return not needs_install

if __name__ == "__main__":
    if check_requirements():
        return True
    else:
        return False

