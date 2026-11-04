// Execute real application functions without contacting external services.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const elements = new Map();
const storage = new Map();
const sandbox = {
  window: { supabase: { createClient: () => ({}) } },
  document: {
    getElementById: id => {
      if (id === 'wave-canvas-wrap') return null;
      if (!elements.has(id)) elements.set(id, {
        value: '', innerHTML: '', textContent: '', addEventListener() {},
      });
      return elements.get(id);
    },
    addEventListener() {},
  },
  localStorage: {
    getItem: key => storage.get(key) ?? null,
    setItem: (key, value) => storage.set(key, String(value)),
  },
  console: { error() {} },
};
vm.createContext(sandbox);
const source = fs.readFileSync(path.join(__dirname, '../src/script.js'), 'utf8');
// Suppress only automatic startup; tests call the actual functions explicitly.
if (!/\binit\(\);\s*$/.test(source)) throw new Error('Application startup changed');
vm.runInContext(source.replace(/\binit\(\);\s*$/, ''), sandbox);
const scenario = fs.readFileSync(0, 'utf8');
const result = vm.runInContext(scenario, sandbox, { timeout: 3000 });
process.stdout.write(JSON.stringify(result));
