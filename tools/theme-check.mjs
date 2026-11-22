import { check } from '@shopify/theme-check-node';
const root = process.argv[2];
const offenses = await check(root);
const sev = ['ERROR','WARN','INFO'];
for (const o of offenses) console.log(`${sev[o.severity]}\t${o.check}\t${o.uri.replace(/.*posy[^/]*\//,'')}:${o.start?.line+1}\t${o.message}`);
console.log('TOTAL', offenses.length, 'errors', offenses.filter(o=>o.severity===0).length);
