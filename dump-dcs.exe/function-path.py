#! /usr/bin/env python3


def filter(filename):
    content = None
    
    with open(filename, 'r') as file:
        try:
            content = file.read()
            
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
        
    lines = [line.strip() for line in content.split('\n')]
    lines = [line.strip() for line in lines if line != '']
    lines = [line.strip() for line in lines if not 'Address' in line]
    lines = [line.strip() for line in lines if not '=======' in line]
    lines = [line.strip() for line in lines if not 'Type' in line]
    lines = [line.strip() for line in lines if not 'Ordinal' in line]
    lines = [line.strip() for line in lines if not 'Full Path' in line]
    
    if len(lines) % 2 == 0:
        pairsz = zip(lines[0::2], lines[1::2])
        output = []
        
        for func, dll in pairsz:
            
            funcname = func.split(' : ')[1].strip() if "Function Name" in func else dll.split(" : ")[1].strip()
            dllx = dll.split(" : ")[1].strip() if "Filename" in dll else func.split(' : ')[1].strip()
            output.append(f'{dllx}:  {funcname}')
            output.sort()
        for line in output:
            print(line)
            
    

if __name__ == "__main__":
    filter(filename='functions-dcs-exe.txt')