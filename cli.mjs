#!/usr/bin/env node
import { hash } from './encrypt.mjs'; // or './encrypt.mjs' if renamed

if (process.argv.length < 3) {
  console.error("Usage: node cli.mjs <input-string>");
  process.exit(1);
}

const input = process.argv[2];

hash(input)
  .then((result) => {
    console.log(result);
  })
  .catch((err) => {
    console.error("Error computing hash:", err);
    process.exit(1);
  });
