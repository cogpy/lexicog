import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Affidavit sections table (7-11)
 */
export const affidavitSections = mysqlTable("affidavit_sections", {
  id: int("id").autoincrement().primaryKey(),
  sectionNumber: varchar("section_number", { length: 10 }).notNull().unique(),
  title: text("title").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

/**
 * AD paragraphs from Peter's founding affidavit
 */
export const adParagraphs = mysqlTable("ad_paragraphs", {
  id: int("id").autoincrement().primaryKey(),
  sectionId: int("section_id").notNull(),
  paragraphNumber: varchar("paragraph_number", { length: 20 }).notNull().unique(),
  content: text("content").notNull(),
  summary: text("summary"),
  severity: int("severity").default(5), // 1-10 scale: 1=neutral (green), 10=serious (red)
  annexures: text("annexures"), // JSON array of annexure references
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

/**
 * JR responses from Jacqueline's affidavit
 */
export const jrResponses = mysqlTable("jr_responses", {
  id: int("id").autoincrement().primaryKey(),
  sectionId: int("section_id").notNull(),
  paragraphNumber: varchar("paragraph_number", { length: 20 }).notNull().unique(),
  content: text("content").notNull(),
  evidenceStrength: int("evidence_strength").default(5), // 1-10 scale: strength of evidence
  annexures: text("annexures"), // JSON array of annexure references
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

/**
 * DR responses from Daniel's affidavit
 */
export const drResponses = mysqlTable("dr_responses", {
  id: int("id").autoincrement().primaryKey(),
  sectionId: int("section_id").notNull(),
  paragraphNumber: varchar("paragraph_number", { length: 20 }).notNull().unique(),
  content: text("content").notNull(),
  evidenceStrength: int("evidence_strength").default(5), // 1-10 scale: strength of evidence
  annexures: text("annexures"), // JSON array of annexure references
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type AffidavitSection = typeof affidavitSections.$inferSelect;
export type InsertAffidavitSection = typeof affidavitSections.$inferInsert;
export type AdParagraph = typeof adParagraphs.$inferSelect;
export type InsertAdParagraph = typeof adParagraphs.$inferInsert;
export type JrResponse = typeof jrResponses.$inferSelect;
export type InsertJrResponse = typeof jrResponses.$inferInsert;
export type DrResponse = typeof drResponses.$inferSelect;
export type InsertDrResponse = typeof drResponses.$inferInsert;

/**
 * Comments/annotations on paragraphs
 */
export const comments = mysqlTable("comments", {
  id: int("id").autoincrement().primaryKey(),
  sectionNumber: varchar("section_number", { length: 10 }).notNull(),
  paragraphNumber: varchar("paragraph_number", { length: 20 }).notNull(),
  paragraphType: mysqlEnum("paragraph_type", ["AD", "JR", "DR"]).notNull(),
  content: text("content").notNull(),
  author: varchar("author", { length: 100 }).notNull().default("Anonymous"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type Comment = typeof comments.$inferSelect;
export type InsertComment = typeof comments.$inferInsert;