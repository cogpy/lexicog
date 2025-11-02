# Affidavit Comparison Website

Interactive web application for comparing Peter's AD paragraphs with Jacqueline's JR and Daniel's DR responses.

## Features

- **Three-column comparison view** - Side-by-side display of AD, JR, and DR paragraphs
- **Grouped view** - AD-centered sections with all responses grouped together
- **Synchronized scrolling** - All columns scroll together proportionally
- **Color coding** - Visual indicators for severity (AD) and evidence strength (JR/DR)
- **Search functionality** - Find keywords or paragraph numbers across all documents
- **Hover highlighting** - Highlights corresponding paragraphs across columns
- **PDF export** - Export comparison view as PDF for offline review
- **Comments/Annotations** - Add notes to specific paragraphs
- **Database persistence** - All data stored in MySQL/TiDB database

## Technology Stack

- **Frontend**: React 19 + TypeScript + Tailwind CSS + shadcn/ui
- **Backend**: Node.js + tRPC + Express
- **Database**: MySQL/TiDB (via Drizzle ORM)
- **Build**: Vite

## Setup

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Set up environment variables (see `.env.example`)

3. Push database schema:
   ```bash
   pnpm db:push
   ```

4. Run data migration:
   ```bash
   pnpm tsx migrate-data.mjs
   ```

5. Start development server:
   ```bash
   pnpm dev
   ```

## Database Schema

- `affidavit_sections` - Section metadata (7-11)
- `ad_paragraphs` - Peter's AD paragraphs with severity ratings
- `jr_responses` - Jacqueline's JR responses with evidence strength
- `dr_responses` - Daniel's DR responses with evidence strength
- `comments` - User annotations on paragraphs

## Live Demo

The website is deployed and accessible via Manus platform.

## Data Source

All affidavit data is extracted from the `cogpy/canima` repository:
- Peter's Founding Affidavit (structured version)
- Jacqueline's Answering Affidavit v8 (JR numbering)
- Daniel's Answering Affidavit v8 (DR numbering)
