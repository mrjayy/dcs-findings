#! /usr/bin/env python3
import re

def extract_function(line):
    stripped_line = line
    
    name_pattern = r"^\[[A-Za-z0-9_\-+\* ]+\][ ]+" + r"([0-9]+[ ]+\(0x[a-fA-F0-9]+\)|N\/A)" + r"([ ]+[0-9]+[ ]+\(0x[a-fA-F0-9]+\)[ ]{2})" + \
        r"([\S:~`',*&^%\s]+[\S:~`',*&^%])\s{2,}?"
    match  = re.findall(name_pattern, stripped_line)
    if not match or len(match[0]) < 2:
        return None
        
    return match[0][2]


def process_imports_and_exports(content):
    
    lines = content.split('\n')

    DLL_LIST = ["COCKPITBASE.DLL", "EDCORE.DLL", "EDOBJECTS.DLL", "ED_API.DLL", "ED_SOUND.DLL", "EDWEBVIEWBROWSER.DLL", "EDDEBUGDRAW.DLL"]    
    dll_name_pattern = r"[A-Za-z0-9_-]+\.DLL"
    match = re.findall(dll_name_pattern, lines[0])

    if match:
        dll_name = match[0]
        
    if dll_name in DLL_LIST:
        del lines[0]
        functions = [[], []]
        ieindex = 0
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped or stripped.startswith("---"):
                continue
            
            if stripped.startswith("Import"):
                ieindex = 0
                continue
                
            elif stripped.startswith("Export"):
                ieindex = 1
                continue
            
            function = extract_function(stripped)
            if function:
                functions[ieindex].append(function)

        return functions, dll_name
    
    return None, None
    

def main():
    
    with open("CockpitBase.dll-dump.txt", "r", encoding="latin-1") as file:
        contents = file.read()

    DLL_LIST = ["COCKPITBASE.DLL", "EDCORE.DLL", "EDOBJECTS.DLL", "ED_API.DLL", "ED_SOUND.DLL", "EDWEBVIEWBROWSER.DLL", "EDDEBUGDRAW.DLL"]
    module_pattern = r"\[[a-zA-Z0-9 -_]*\][ ][A-Za-z0-9_-]+\.DLL"
    
    startings = []

    for match in re.finditer(module_pattern, contents):        
        startings.append(match.start())

    dll_d = {}
    for index in range(len(startings) - 1):
        functions, dll = process_imports_and_exports(contents[startings[index]:startings[index + 1]])
        if dll:
            dll_d[dll] = functions
        
    
    for dll_name in dll_d.keys():
        imports, exports = dll_d[dll_name]
        
        # for imp in imports:
        #     s = f"{dll_name}[I]: {imp}"
        #     print(s)
        
        for exp in exports:
            s = f"{dll_name}[E]: {exp}"
            print(s)
        


if __name__ == "__main__":
    main()