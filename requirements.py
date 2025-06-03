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
    except subprocess.CalledProcessError:
        return {}  # Mengembalikan dictionary kosong jika ada error

def check_requirements(requirements_file="requirements_versions.txt"):
    """
    Mengecek apakah semua requirement dalam file sudah terinstal dengan versi yang sesuai.
    Mengembalikan True jika semua sesuai, False jika ada yang tidak sesuai atau tidak terinstal.
    """
    installed_packages = get_installed_packages()
    try:
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        req = Requirement(line)
                        package_name = req.name.lower()
                        required_specifier = req.specifier

                        if package_name not in installed_packages or not required_specifier.contains(installed_packages[package_name]):
                            return False  # Ada yang tidak sesuai
                    except:
                        return False  # Gagal memproses baris
    except FileNotFoundError:
        return False  # File tidak ditemukan

    return True  # Semua sesuai

if __name__ == "__main__":
    all_met = check_requirements()
    print(all_met) # Untuk keperluan pengujian, Anda bisa mencetak hasilnya di sini

