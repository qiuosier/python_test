from my_package import utils
from my_module import my_function_in_module

print("This is the main script.")
my_function_in_module()
utils.my_function_in_package()

def entry_function(*args, **kwargs):
    print("This is the entry function.")
    print("Arguments:")
    print(args)
    for k, v in kwargs.items():
        print(f"{k}={v}")
    my_function_in_module()
    utils.my_function_in_package()

