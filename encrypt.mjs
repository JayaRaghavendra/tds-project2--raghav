import crypto from 'node:crypto';
/*
PEM from public_key.pem generated on 22 Sep 2024 via:

openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out -
*/

const pem =
  "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuYcxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMIDEkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXcWyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfWed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfISI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIXdQIDAQAB";
const binary = atob(pem);
const keyData = new ArrayBuffer(binary.length);
const view = new Uint8Array(keyData);
for (let i = 0; i < binary.length; i++) view[i] = binary.charCodeAt(i);
const publicKey = await crypto.subtle.importKey("spki", keyData, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["encrypt"]);

// Encrypt using the public key
export async function encrypt(data) {
  const encodedData = new TextEncoder().encode(data);
  const encryptedBuffer = await crypto.subtle.encrypt({ name: "RSA-OAEP" }, publicKey, encodedData);
  const encryptedArray = new Uint8Array(encryptedBuffer);
  return btoa(String.fromCharCode(...encryptedArray));
}

// Hash using SHA-256
export async function hash(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  return hashHex;
}
