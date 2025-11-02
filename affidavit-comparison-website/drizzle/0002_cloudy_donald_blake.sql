CREATE TABLE `comments` (
	`id` int AUTO_INCREMENT NOT NULL,
	`section_number` varchar(10) NOT NULL,
	`paragraph_number` varchar(20) NOT NULL,
	`paragraph_type` enum('AD','JR','DR') NOT NULL,
	`content` text NOT NULL,
	`author` varchar(100) NOT NULL DEFAULT 'Anonymous',
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `comments_id` PRIMARY KEY(`id`)
);
