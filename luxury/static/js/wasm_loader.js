
fetch('/static/wasm/sample.wasm')
.then(response => response.arrayBuffer())
.then(bytes => WebAssembly.instantiate(bytes))
.then(result => {
    result.instance.exports._start(); // Assumes exported _start()
});
