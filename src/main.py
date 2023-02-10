import datetime
import os
import sys

from my_package import utils
from my_module import my_function_in_module


def write_output(filename=None):
    if not filename:
        output_dir = os.environ.get("OUTPUT_DIR", "./outputs")
        output_dir = os.path.abspath(os.path.expanduser(output_dir))
        filename = os.path.join(
            output_dir,
            datetime.datetime.now().strftime("%Y%m%d_%H%M%s.txt")
        )
    else:
        output_dir = os.path.dirname(os.path.abspath(os.path.expanduser(filename)))
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Writing {filename}...")
    with open(filename, "w") as f:
        f.write(filename)


def entry_function(*args, **kwargs):
    print("This is the entry function.")
    print("Arguments:")
    for arg in args:
        print(f"{str(arg)} ({type(arg)})")
    for k, v in kwargs.items():
        print(f"{k}={str(v)} ({type(v)})")
    my_function_in_module()
    utils.my_function_in_package()
    write_output()

if __name__ == "__main__":
    print("This is the main script.")
    if len(sys.argv) > 1:
        print(sys.argv[1:])
    my_function_in_module()
    utils.my_function_in_package()
    write_output(os.environ.get("OUTPUT_FILENAME"))
