fname = "hijack.c"
data = open(fname, 'r').read().replace('\n', '\\n')
i = 0
first = True
for element in data:
    if first == True:
        print("'''", end='')
        first = False
    if i == 24-1: # bcs of null terminator
        i = 0
        print("'''", end='')
        print(f"\n[ NEW SEGMENT ]: \n")
        print("'''", end='')
        
    print(element, end='')
    i += 1
print("'''")