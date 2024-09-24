write a writeup on this!!!
we accessed a memory location in order to pull the stored flag, strings would NOT work for this.


// Access the WebAssembly memory
const memory = exports.memory;

// Create a DataView to read from the memory buffer
const memoryView = new DataView(memory.buffer);

// Read the memory at address 1024
let memoryLocation = 1072;
let memoryValue = '';

// Assuming the memory location stores a string, read byte by byte until you hit a null byte (0x00)
for (let i = memoryLocation; i < memory.buffer.byteLength; i++) {
    const byte = memoryView.getUint8(i);
    if (byte === 0) break; // Null-terminated string
    memoryValue += String.fromCharCode(byte);
}

// Print the value stored at memory location 1024
console.log("Memory at location 1072:", memoryValue);
