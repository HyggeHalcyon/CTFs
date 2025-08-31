const KEY_HEX = '6c27f0f1a2f0e4b14b3a5b7c9d1e2f3a6c27f0f1a2f0e4b14b3a5b7c9d1e2f3a';
const IV_HEX  = '1a2b3c4d5e6f708190a0b0c0d0e0f001'; 

const hexToBytes = (h) => new Uint8Array(h.match(/../g).map(b => parseInt(b, 16)));
const KEY_BYTES = hexToBytes(KEY_HEX);
const IV_BYTES  = hexToBytes(IV_HEX);

const cryptoKeyPromise = crypto.subtle.importKey('raw', KEY_BYTES, { name: 'AES-CTR', length: 256 }, false, ['encrypt']);

const utf8enc = (s) => new TextEncoder().encode(s);
const bytesToB64 = (b) => btoa(String.fromCharCode(...b));

const textToBase64 = (s) => bytesToB64(utf8enc(s));

async function encValue(value) {
  const s = (typeof value === 'string') ? value : JSON.stringify(value);
  const b64plain = textToBase64(s);
  const key = await cryptoKeyPromise;
  const ct = await crypto.subtle.encrypt(
    { name: 'AES-CTR', counter: IV_BYTES, length: 64 },
    key,
    utf8enc(b64plain)
  );
  const cta = new Uint8Array(ct);
  const out = new Uint8Array(cta.length + IV_BYTES.length);
  out.set(cta, 0);
  out.set(IV_BYTES, cta.length);
  return bytesToB64(out);
}

async function encObject(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v === '' || v == null) continue;
    out[k] = await encValue(v);
  }
  return out;
}

async function encPost(url, body) {
  const encBody = await encObject(body || {});
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(encBody)
  });
}

window.encPost = encPost;

