#
# SQL Export
# Created by Querious (201067)
# Created: 7 October 2019 13.03.20 GMT+7
# Encoding: Unicode (UTF-8)
#


SET @PREVIOUS_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;


CREATE TABLE `tbl_campaign` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `client_id` bigint(20) NOT NULL,
  `campaign_name` varchar(160) CHARACTER SET utf8 DEFAULT NULL,
  `campaign_start` date DEFAULT NULL,
  `campaign_end` date DEFAULT NULL,
  `n_status` int(3) DEFAULT '1' COMMENT '0-> off, 1 -> on',
  `campaign_added` datetime NOT NULL,
  `channels` varchar(100) CHARACTER SET latin1 NOT NULL COMMENT '1 => TwS, 2 => TwAS, 3 => FbS, 4 => FbAS, 5 => FoS, 6 => NeS, 7 => CoS',
  `tracking_method` int(3) NOT NULL DEFAULT '0',
  `campaign_desc` text CHARACTER SET latin1 NOT NULL,
  `lang` varchar(3) CHARACTER SET latin1 NOT NULL DEFAULT 'id',
  `geotarget` varchar(3) CHARACTER SET latin1 NOT NULL DEFAULT 'all' COMMENT 'all => global, id => indo, sg => singapore DST',
  `twitter_account` text CHARACTER SET latin1 NOT NULL,
  `fb_account` text CHARACTER SET latin1,
  `hastag` text CHARACTER SET latin1 NOT NULL,
  `group_id` int(11) NOT NULL DEFAULT '0',
  `category_id` int(11) DEFAULT '0' COMMENT '0 -> no category, xx->set to some category',
  `historical_interval` int(3) NOT NULL DEFAULT '0' COMMENT 'days of historical data to be taken.',
  `dtlastchange` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `case_type` tinyint(3) DEFAULT '0' COMMENT '0->person 1->issue',
  `process_summary_priority` smallint(6) NOT NULL DEFAULT '0',
  `keywords` varchar(1024) COLLATE utf8_unicode_ci NOT NULL,
  `twitter_rule_id` int(11) NOT NULL DEFAULT '0',
  `color` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lang` (`lang`),
  KEY `geotarget` (`geotarget`),
  KEY `account_id` (`client_id`),
  KEY `group_id` (`group_id`),
  KEY `idx_n_status_process_priority` (`n_status`,`process_summary_priority`),
  KEY `idx_n_status_dtlastchange` (`n_status`,`dtlastchange`)
) ENGINE=InnoDB AUTO_INCREMENT=2296 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




SET FOREIGN_KEY_CHECKS = @PREVIOUS_FOREIGN_KEY_CHECKS;


