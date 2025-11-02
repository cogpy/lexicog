import { drizzle } from 'drizzle-orm/mysql2';
import { affidavitSections, adParagraphs, jrResponses, drResponses } from './drizzle/schema.ts';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Read the JSON data
const jsonPath = join(__dirname, 'client', 'public', 'affidavit-data.json');
const data = JSON.parse(readFileSync(jsonPath, 'utf-8'));

// Connect to database
const db = drizzle(process.env.DATABASE_URL);

console.log('Starting data migration...');

for (const [sectionNum, sectionData] of Object.entries(data)) {
  console.log(`\nMigrating Section ${sectionNum}: ${sectionData.title}`);
  
  // Insert section
  const [section] = await db.insert(affidavitSections).values({
    sectionNumber: sectionNum,
    title: sectionData.title,
  }).onDuplicateKeyUpdate({
    set: { title: sectionData.title }
  });
  
  const sectionId = section.insertId;
  console.log(`  Section ID: ${sectionId}`);
  
  // Insert AD paragraphs
  const adCount = Object.keys(sectionData.paragraphs || {}).length;
  if (adCount > 0) {
    for (const [paraNum, content] of Object.entries(sectionData.paragraphs)) {
      await db.insert(adParagraphs).values({
        sectionId,
        paragraphNumber: paraNum,
        content,
      }).onDuplicateKeyUpdate({
        set: { content, sectionId }
      });
    }
    console.log(`  Inserted ${adCount} AD paragraphs`);
  }
  
  // Insert JR responses
  const jrCount = Object.keys(sectionData.jr_responses || {}).length;
  if (jrCount > 0) {
    for (const [paraNum, content] of Object.entries(sectionData.jr_responses)) {
      await db.insert(jrResponses).values({
        sectionId,
        paragraphNumber: paraNum,
        content,
      }).onDuplicateKeyUpdate({
        set: { content, sectionId }
      });
    }
    console.log(`  Inserted ${jrCount} JR responses`);
  }
  
  // Insert DR responses
  const drCount = Object.keys(sectionData.dr_responses || {}).length;
  if (drCount > 0) {
    for (const [paraNum, content] of Object.entries(sectionData.dr_responses)) {
      await db.insert(drResponses).values({
        sectionId,
        paragraphNumber: paraNum,
        content,
      }).onDuplicateKeyUpdate({
        set: { content, sectionId }
      });
    }
    console.log(`  Inserted ${drCount} DR responses`);
  }
}

console.log('\n✅ Data migration completed successfully!');
process.exit(0);
