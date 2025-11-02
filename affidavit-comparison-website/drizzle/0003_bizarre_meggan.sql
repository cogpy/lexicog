ALTER TABLE `ad_paragraphs` ADD `summary` text;--> statement-breakpoint
ALTER TABLE `ad_paragraphs` ADD `severity` int DEFAULT 5;--> statement-breakpoint
ALTER TABLE `ad_paragraphs` ADD `annexures` text;--> statement-breakpoint
ALTER TABLE `dr_responses` ADD `evidence_strength` int DEFAULT 5;--> statement-breakpoint
ALTER TABLE `dr_responses` ADD `annexures` text;--> statement-breakpoint
ALTER TABLE `jr_responses` ADD `evidence_strength` int DEFAULT 5;--> statement-breakpoint
ALTER TABLE `jr_responses` ADD `annexures` text;