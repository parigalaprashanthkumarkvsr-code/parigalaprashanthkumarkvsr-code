/** Dependency-free Node entry point. The XML transformation lives in build.py. */
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const runners = process.platform === 'win32' ? ['py', 'python', 'python3'] : ['python3','python'];
let result;
for (const binary of runners) {
  result = spawnSync(binary, [resolve(root, 'scripts/build.py')], { cwd: root, stdio: 'inherit' });
  if (!result.error || result.error.code !== 'ENOENT') break;
}
if (!result || result.error) {
  console.error('Python 3 and lxml are needed: pip install -r requirements.txt');
  process.exit(1);
}
process.exit(result.status ?? 1);
