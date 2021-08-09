import datetime
import os

from my_package import utils
from my_module import my_function_in_module


def write_output():
    if "OUTPUT_DIR" in os.environ:
        output_dir = os.path.abspath(os.path.expanduser(os.environ.get("OUTPUT_DIR")))
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(
            output_dir,
            datetime.datetime.now().strftime("%Y%m%d_%H%M%s.txt")
        )
        print(f"Writing {filename}...")
        with open(filename, "w") as f:
            f.write(filename)


def entry_function(*args, **kwargs):
    print("This is the entry function.")
    print("Arguments:")
    print(args)
    for k, v in kwargs.items():
        print(f"{k}={v}")
    my_function_in_module()
    utils.my_function_in_package()
    write_output()

if __name__ == "__main__":
    print("This is the main script.")
    my_function_in_module()
    utils.my_function_in_package()
    write_output()
