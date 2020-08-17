import os
import pathlib
import subprocess
import glob
from pick import pick


title = 'Welcome to MakeAMake, please fill up the required fields: '
a_title = 'This software was developed by Elia Sulimanov.\nCheck GitHub repository ' + \
    '@ https://github.com/EliaSulimanov/MakeAMake for further information.\n' + \
    'This software uses a open-source library named \'pick\', select it for copyright notice:'
basic_options = ['Compiler path: ', 'Executable name: ', 'Additional flags: ', 'Run', 'About', 'Quit']
options = ['Compiler path: ', 'Executable name: ', 'Additional flags: ', 'Run', 'About', 'Quit']
a_options = ['pick ', 'Back']
options_dict = {}
objects = []
dependencies = []
dir_path = os.path.dirname(os.path.realpath(__file__))


def press_enter_to_continue():
    try:
        input("Press Enter key to continue\n")
        os.system('cls' if os.name == 'nt' else 'clear')
    except SyntaxError:
        os.system('cls' if os.name == 'nt' else 'clear')
        pass


def pick_copyright_notice():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("pick library copyright notice:\n\n" +
          "The MIT License (MIT) \n\n" +

          "Copyright (c) 2016 Wang Dàpéng \n\n" +

          "Permission is hereby granted, free of charge, to any person obtaining a copy\n" +
          "of this software and associated documentation files (the \"Software\"), to deal\n" +
          "in the Software without restriction, including without limitation the rights\n" +
          "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n" +
          "copies of the Software, and to permit persons to whom the Software is\n" +
          "furnished to do so, subject to the following conditions:\n\n" +

          "The above copyright notice and this permission notice shall be included in all\n" +
          "copies or substantial portions of the Software.\n\n" +

          "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n" +
          "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n" +
          "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n" +
          "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n" +
          "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n" +
          "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n" +
          "SOFTWARE.\n\n")
    press_enter_to_continue()


def write_make_file():
    try:
        f = open("Makefile", "w")
        f.write("CC = " + options_dict[0] + "\n")
        if len(objects) > 0:
            f.write("OBJS =")
            for obj in objects:
                f.write(" " + obj)
            f.write("\n")
        f.write("EXEC = " + options_dict[1] + "\n")
        if len(options_dict[2]) > 0:
            f.write("COMP_FLAG = " + options_dict[2] + "\n")
        f.write("\n")
        f.write("$(EXEC): $(OBJS)\n\t$(CC) $(COMP_FLAG) $(OBJS) -o $@\n")
        f.write("\n")
        for dependency in dependencies:
            f.write(dependency + "\n\t$(CC) -c $(COMP_FLAG) $*.cpp\n")
            f.write("\n")
        f.write("clean:\n\trm -f $(OBJS) $(EXEC)\n")
        f.close()
        print("Makefile created and located in: " + str(pathlib.Path().absolute()))
        press_enter_to_continue()
    except Exception as e:
        print("Error: " + str(e))
        press_enter_to_continue()


def make_a_make():
    files = [f for f in glob.glob(dir_path + "**/*.cpp", recursive=True)]
    for file in files:
        objects.append(os.path.splitext(os.path.basename(file))[0] + '.o')
        dependencies.append(subprocess.run([options_dict[0], '-MM ' + os.path.basename(file)], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    write_make_file()


def check_options():
    if len(options_dict[0]) <= 0:
        print("Please provide a compiler path\n")
        press_enter_to_continue()
        return False

    if subprocess.run([options_dict[0], '-v'], stdout=subprocess.PIPE).stdout.decode('utf-8').find("version") == -1:
        print("Please check if gcc installed and if the path is correct\n")
        press_enter_to_continue()
        return False

    if len(options_dict[1]) <= 0:
        print("Please provide a executable name\n")
        press_enter_to_continue()
        return False

    return True


if __name__ == '__main__':
    while True:
        option, index = pick(options, title)
        if option == 'About':
            a_option, a_index = pick(a_options, a_title)
            if a_option == 'Back':
                continue
            else:
                pick_copyright_notice()
        else:
            if option == 'Run':
                if not check_options():
                    continue
                else:
                    make_a_make()
            else:
                if option == 'Quit':
                    break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Please insert ' + basic_options[index].lower() + '\n')
                    options_dict[index] = str(input())
                    options[index] = basic_options[index] + options_dict[index]
                    os.system('cls' if os.name == 'nt' else 'clear')
