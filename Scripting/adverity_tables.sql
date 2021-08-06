CREATE TABLE `factual_item` (
  `platform_id` int,
  `clicks` int,
  `views` int,
  `video100` int,
  `engagement` int,
  `impressions` int,
  `dollar_cost` float,
  `day` datetime,
  `created_at` timestamp,
  PRIMARY KEY (`platform_id`)
);

CREATE TABLE `dimension` (
  `campaign_internal_id` int,
  `campaign_name` varchar(255),
  `platform_id` int,
  `datastream` varchar(255),
  PRIMARY KEY (`campaign_internal_id`)
);

ALTER TABLE `dimension` ADD FOREIGN KEY (`platform_id`) REFERENCES `factual_item` (`platform_id`);

