#!/usr/bin/env python3
import subprocess
import sys
import os
import time

LOCAL_DIR = "/Users/ronakpai/Desktop/laundering"
REMOTE_DIR = "/storage/emulated/0/DCIM/Camera"

# 👇 Adjust ONLY if the profile icon tap misses
PROFILE_TAP_X1 = 1005
PROFILE_TAP_Y1 = 133

PROFILE_TAP_X2 = 277
PROFILE_TAP_Y2 = 1190


def run(cmd):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Command failed. Exiting.")
        sys.exit(1)


def main():
    # 1. Ensure adb works
    run("adb version")

    # 2. Collect filenames dynamically
    try:
        files = [
            f for f in os.listdir(LOCAL_DIR)
            if os.path.isfile(os.path.join(LOCAL_DIR, f))
        ]
    except FileNotFoundError:
        print("Local laundering folder not found.")
        sys.exit(1)

    if not files:
        print("No files found in laundering folder. Nothing to do.")
        sys.exit(0)

    # 3. Calculate total size
    total_bytes = sum(
        os.path.getsize(os.path.join(LOCAL_DIR, f)) for f in files
    )
    total_mb = total_bytes / (1024 * 1024)

    if total_mb >= 1024:
        print(f"\nFound {len(files)} files (~{total_mb/1024:.2f} GB)")
    else:
        print(f"\nFound {len(files)} files (~{total_mb:.2f} MB)")

    #aaa

    # 4. Push files to phone
    run(f'adb push "{LOCAL_DIR}/." "{REMOTE_DIR}"')

    # 5. Reboot device (forces media rescan)
    run("adb reboot")

    # 6. Wait for device
    print("\nWaiting for device...")
    run("adb wait-for-device")
    time.sleep(7.5)
    print("the program is working dw")


   #aaa


    time.sleep(7.5)
    #run("adb shell input keyevent 26")

    time.sleep(2)

    #3. 
    run("adb shell input swipe 500 1500 500 500")

    # pee pee
    time.sleep(2.5)

    # 8. Open Google Photos
    run(
        "adb shell am start "
        "-n com.google.android.apps.photos/.home.HomeActivity"
    )

    time.sleep(4)

    # 9. Tap profile icon
    run(f"adb shell input tap {PROFILE_TAP_X1} {PROFILE_TAP_Y1}")
    time.sleep(2)
    run(f"adb shell input tap {PROFILE_TAP_X2} {PROFILE_TAP_Y2}")

    print("\nGoogle Photos opened.")
    print("WAIT for Google Photos to finish backing up.")
    print("When you are 100% sure, type DELETE to proceed.")

    confirm = input("> ").strip()
    if confirm != "DELETE":
        print("Aborted. Nothing deleted.")
        sys.exit(0)

    # 10. Delete files from phone
    # 10. Delete files from phone (SPACE-SAFE)
    for filename in files:
        run(
        f'adb shell \'rm -f -- "{REMOTE_DIR}/{filename}"\''
    )


    # 11. Delete files from Mac
    for filename in files:
        local_path = os.path.join(LOCAL_DIR, filename)
        if os.path.exists(local_path):
            os.remove(local_path)
            print(f"> rm {local_path}")

    # 12. Final summary
    if total_mb >= 1024:
        print(f"\n✅ Freed ~{total_mb/1024:.2f} GB")
    else:
        print(f"\n✅ Freed ~{total_mb:.2f} MB")

    # end reboot so its not funny (media rescan)
    run("adb reboot")


if __name__ == "__main__":
    main()
