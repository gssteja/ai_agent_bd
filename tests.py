from functions.run_python_file import run_python_file
from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py"))

print(run_python_file("calculator", "main.py", ["3 + 5"]))

print(run_python_file("calculator", "tests.py"))

print(run_python_file("calculator", "../main.py"))

print(run_python_file("calculator", "nonexistent.py"))

print(run_python_file("calculator", "lorem.txt"))
