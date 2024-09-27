from pwn import*


'''
    What's weird is when I free x and then print the value of x it 
    still prints the correct value of bico. The reason for this is because when 
    we free(x) it becomes a dangling pointer, it still points to the memory location,
    but since nothing over-wrote it yet, it's still accessing it.
    We just need to allocate an object and overwrite it with "pico"!

'''