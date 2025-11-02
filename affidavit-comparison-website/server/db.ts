import { eq, and } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { InsertUser, users, affidavitSections, adParagraphs, jrResponses, drResponses, comments, InsertComment } from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

/**
 * Get all affidavit data organized by section
 */
export async function getAllAffidavitData() {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get affidavit data: database not available");
    return null;
  }

  const sections = await db.select().from(affidavitSections);
  const result: Record<string, any> = {};

  for (const section of sections) {
    const adParas = await db
      .select()
      .from(adParagraphs)
      .where(eq(adParagraphs.sectionId, section.id));
    
    const jrResps = await db
      .select()
      .from(jrResponses)
      .where(eq(jrResponses.sectionId, section.id));
    
    const drResps = await db
      .select()
      .from(drResponses)
      .where(eq(drResponses.sectionId, section.id));

    result[section.sectionNumber] = {
      title: section.title,
      paragraphs: Object.fromEntries(
        adParas.map((p) => [p.paragraphNumber, {
          content: p.content,
          summary: p.summary,
          severity: p.severity,
          annexures: p.annexures ? JSON.parse(p.annexures) : [],
        }])
      ),
      jr_responses: Object.fromEntries(
        jrResps.map((r) => [r.paragraphNumber, {
          content: r.content,
          evidenceStrength: r.evidenceStrength,
          annexures: r.annexures ? JSON.parse(r.annexures) : [],
        }])
      ),
      dr_responses: Object.fromEntries(
        drResps.map((r) => [r.paragraphNumber, {
          content: r.content,
          evidenceStrength: r.evidenceStrength,
          annexures: r.annexures ? JSON.parse(r.annexures) : [],
        }])
      ),
    };
  }

  return result;
}

/**
 * Get comments with optional filters
 */
export async function getComments(filters: {
  sectionNumber?: string;
  paragraphNumber?: string;
  paragraphType?: "AD" | "JR" | "DR";
}) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get comments: database not available");
    return [];
  }

  const conditions = [];
  if (filters.sectionNumber) {
    conditions.push(eq(comments.sectionNumber, filters.sectionNumber));
  }
  if (filters.paragraphNumber) {
    conditions.push(eq(comments.paragraphNumber, filters.paragraphNumber));
  }
  if (filters.paragraphType) {
    conditions.push(eq(comments.paragraphType, filters.paragraphType));
  }

  const query = conditions.length > 0
    ? db.select().from(comments).where(and(...conditions))
    : db.select().from(comments);

  return await query;
}

/**
 * Add a new comment
 */
export async function addComment(comment: InsertComment) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot add comment: database not available");
    throw new Error("Database not available");
  }

  const result = await db.insert(comments).values({
    sectionNumber: comment.sectionNumber,
    paragraphNumber: comment.paragraphNumber,
    paragraphType: comment.paragraphType,
    content: comment.content,
    author: comment.author || "Anonymous",
  });

  return result;
}

/**
 * Delete a comment by ID
 */
export async function deleteComment(id: number) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot delete comment: database not available");
    throw new Error("Database not available");
  }

  await db.delete(comments).where(eq(comments.id, id));
}
