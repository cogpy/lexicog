CREATE TABLE `ad_paragraphs` (
	`id` int AUTO_INCREMENT NOT NULL,
	`section_id` int NOT NULL,
	`paragraph_number` varchar(20) NOT NULL,
	`content` text NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `ad_paragraphs_id` PRIMARY KEY(`id`),
	CONSTRAINT `ad_paragraphs_paragraph_number_unique` UNIQUE(`paragraph_number`)
);
--> statement-breakpoint
CREATE TABLE `affidavit_sections` (
	`id` int AUTO_INCREMENT NOT NULL,
	`section_number` varchar(10) NOT NULL,
	`title` text NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `affidavit_sections_id` PRIMARY KEY(`id`),
	CONSTRAINT `affidavit_sections_section_number_unique` UNIQUE(`section_number`)
);
--> statement-breakpoint
CREATE TABLE `dr_responses` (
	`id` int AUTO_INCREMENT NOT NULL,
	`section_id` int NOT NULL,
	`paragraph_number` varchar(20) NOT NULL,
	`content` text NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `dr_responses_id` PRIMARY KEY(`id`),
	CONSTRAINT `dr_responses_paragraph_number_unique` UNIQUE(`paragraph_number`)
);
--> statement-breakpoint
CREATE TABLE `jr_responses` (
	`id` int AUTO_INCREMENT NOT NULL,
	`section_id` int NOT NULL,
	`paragraph_number` varchar(20) NOT NULL,
	`content` text NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `jr_responses_id` PRIMARY KEY(`id`),
	CONSTRAINT `jr_responses_paragraph_number_unique` UNIQUE(`paragraph_number`)
);
