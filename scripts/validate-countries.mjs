import fs from 'node:fs';import assert from 'node:assert/strict';
const data=JSON.parse(fs.readFileSync(new URL('../countries.json',import.meta.url),'utf8'));
assert.equal(data.schema,1);assert.equal(data.authority,'skunkworks-africa/theme');
const owners=new Set(),codes=new Set();
for(const c of data.countries){
 assert.ok(c.owner.startsWith('skunkworks-'),'Expected country org');
 assert.equal(c.repository,c.owner+'/www');
 assert.ok(/^https:\/\//.test(c.canonical));
 assert.ok(/^[a-z]{2}(?:-[A-Z]{2})?$/.test(c.locale));
 assert.ok(['corporate','tokens-only'].includes(c.themeMode));
 assert.ok(!owners.has(c.owner),'Duplicate country org '+c.owner);
 assert.ok(!codes.has(c.code),'Duplicate country '+c.code);
 owners.add(c.owner);codes.add(c.code);
}
assert.ok(data.countries.length>=8,'Missing country organisations');
console.log('Country registry validated: '+data.countries.length+' organisations');
