import platform
import subprocess
import sys, psutil
from core.sys_utils import get_docker_cmd, get_subprocess_no_window_args

class ExternalToolsManager:

    @staticmethod
    def is_distrib_running():
        try:
            output = subprocess.check_output(
                ["wsl", "-l", "--running", "-q"],
                universal_newlines=True,
                **get_subprocess_no_window_args()
            )
            lines = [line.strip().replace('\x00', '').replace('\ufeff', '') for line in output.splitlines()]
            # Debug print (à virer en prod)
            # for i, line in enumerate(lines): print(f"[{i}] '{line}'")
            return any(line.lower() == "vpn-manager" for line in lines)
        except Exception as e:
            print(f"❌ WSL distribution check failed: {e}")
            return False

        
    @staticmethod
    def is_wsl_installed():
        if platform.system() != "Windows":
            return True  # Not relevant outside Windows
        try:
            subprocess.check_output(["wsl", "--version"], stderr=subprocess.DEVNULL, **get_subprocess_no_window_args())
            return True
        except Exception:
            return False

    @staticmethod
    def is_wsl_running():
        if platform.system() != "Windows":
            return True  # Always true outside Windows

        if not ExternalToolsManager.is_wsl_installed():
            print("❌ WSL is not installed. Exiting.")
            sys.exit(1)

        try:
            print(ExternalToolsManager.is_distrib_running())
            if ExternalToolsManager.is_distrib_running():
                return True
            else:
                print("⚠️ WSL 'vpn-manager' is not running. Attempting to start it...")
                subprocess.run(
                    ["wsl", "-d", "vpn-manager", "dbus-launch", "true"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    **get_subprocess_no_window_args()
                )
                # Re-check if it's now running
                if ExternalToolsManager.is_distrib_running():
                    return True
                else:
                    print("❌ Failed to start WSL 'vpn-manager'. Exiting.")
                    sys.exit(1)
        except Exception:
            print("❌ WSL check failed. Exiting.")
            sys.exit(1)

    @staticmethod
    def is_docker_running():
        if platform.system() == "Windows":
            ExternalToolsManager.is_wsl_running()  # Makes sure it's up

        cmd = get_docker_cmd() + ["info"]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, **get_subprocess_no_window_args())
            return b"Server Version" in output
        except Exception:
            print("❌ Docker is not running or not installed. Exiting.")
            sys.exit(1)

    @staticmethod
    def is_vcxsrv_running():
        if platform.system() != "Windows":
            return True  # Not relevant outside Windows

        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and 'vcxsrv.exe' in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        print("❌ VcXsrv is not running. Exiting.")
        sys.exit(1)
