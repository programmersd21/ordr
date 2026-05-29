import glob
import os
import subprocess
import sys


def build_and_install():
    print("Building ordr in release mode...")
    env = os.environ.copy()
    env["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"

    output_dir = "build"
    cmd = ["maturin", "build", "--release", "-o", output_dir]

    try:
        subprocess.run(cmd, env=env, check=True)
        print(f"\nBuild successful. Wheels are in the '{output_dir}' directory.")
        wheels = glob.glob(os.path.join(output_dir, "*.whl"))
        if not wheels:
            print("Error: No wheel file found after build.")
            sys.exit(1)

        # Sort by modification time to get the latest one if multiple exist
        latest_wheel = max(wheels, key=os.path.getmtime)

        print(f"Installing {latest_wheel}...")
        pip_cmd = [sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps"]
        subprocess.run([*pip_cmd, latest_wheel], check=True)
        print("\nInstallation successful.")

    except subprocess.CalledProcessError as e:
        print(f"\nOperation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_and_install()
