#! /usr/bin/env python3

def filterfl(filename):
    SEPARATOR = "==================================================\n"
    SAVE = False
    SKIP = False
    START = False

    with open(filename, 'r') as f:
        for line in f:
            if line == "\n":
                continue

            if line == SEPARATOR:
                if not START:
                    START = True
                    chunk = ''
                else:
                    START = False
                    if not SKIP:
                        print(chunk)

            if SKIP:
                continue

            if "Function Name" in line:
                x = line.split(":")
                if not x[1][0:3].replace(' ','a').replace('_', 'a').isalnum():
                    SKIP = True
                else:
                    SKIP = False

            if "DCS" in line and not SKIP:
                SAVE = True

            if START:
                chunk += line



if __name__ == "__main__":
    filterfl(filename='functions-dcs-exe.utf-8')