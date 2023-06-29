-- --------------------------------------------------------
-- 主机:                           121.46.23.132
-- 服务器版本:                        5.7.22 - MySQL Community Server (GPL)
-- 服务器操作系统:                      Linux
-- HeidiSQL 版本:                  11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 导出  表 aicrm.bus_calllog 结构
CREATE TABLE IF NOT EXISTS `bus_calllog` (
  `__uid__` int(100) DEFAULT NULL COMMENT '数据源',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `sn` varchar(100) NOT NULL DEFAULT '',
  `source` varchar(100) DEFAULT NULL COMMENT '任务编号',
  `started_at` datetime DEFAULT NULL COMMENT '外呼时间',
  `talktimes` int(11) DEFAULT NULL COMMENT '通话时长',
  `status` varchar(100) DEFAULT NULL COMMENT '意向等级',
  `status_manual` varchar(100) DEFAULT NULL COMMENT '人工分类',
  `operator` varchar(100) DEFAULT NULL COMMENT '话务员',
  `team_name` varchar(100) DEFAULT NULL COMMENT '分组',
  `notes` varchar(255) DEFAULT NULL COMMENT '备注',
  `download_status` varchar(20) DEFAULT NULL COMMENT '下载状态',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`sn`) USING BTREE,
  KEY `uid` (`__uid__`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.bus_calllog 的数据：~2 rows (大约)
/*!40000 ALTER TABLE `bus_calllog` DISABLE KEYS */;
INSERT INTO `bus_calllog` (`__uid__`, `phone`, `sn`, `source`, `started_at`, `talktimes`, `status`, `status_manual`, `operator`, `team_name`, `notes`, `download_status`, `update_time`, `create_time`) VALUES
	(1, '85256163491', 'account|e1857e3d2352aa1c4edf124e9eba2600', '20230618094701', '2023-06-19 13:28:44', 82, 'E', 'A', 'mo912143', '周翠翠客户', NULL, NULL, '2023-06-28 23:42:43', '2023-06-28 09:04:10'),
	(2, '85256676389', 'account|e43ac674a5e6e1e3f403c92624419d3e', '20230618094701', '2023-06-19 12:14:31', 114, 'E', 'A', 'mo912143', '周翠翠客户', NULL, NULL, '2023-06-28 09:15:00', '2023-06-28 09:15:00');
/*!40000 ALTER TABLE `bus_calllog` ENABLE KEYS */;

-- 导出  表 aicrm.bus_report 结构
CREATE TABLE IF NOT EXISTS `bus_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `__uid__` int(11) DEFAULT NULL COMMENT '数据源',
  `date` date DEFAULT NULL COMMENT '日期',
  `agent_name` varchar(50) DEFAULT NULL COMMENT '坐席名字',
  `company_name` varchar(100) DEFAULT NULL COMMENT '公司名',
  `outbound_area` varchar(50) DEFAULT NULL COMMENT '外呼地区',
  `outbound_count` int(11) DEFAULT NULL COMMENT '外呼数量',
  `connection_rate` decimal(5,2) DEFAULT NULL COMMENT '接通率',
  `connection_count` int(11) DEFAULT NULL COMMENT '接通数量',
  `screen_pop_count` int(11) DEFAULT NULL COMMENT '可弹屏数',
  `screen_pop_rate` decimal(5,2) DEFAULT NULL COMMENT '可弹屏率',
  `offline_screen_pop_count` int(11) DEFAULT NULL COMMENT '未在线弹屏',
  `offline_screen_pop_rate` decimal(5,2) DEFAULT NULL COMMENT '未在线弹屏率',
  `pushed_at` int(11) DEFAULT NULL COMMENT '弹屏数量',
  `pushed_rate` decimal(5,2) DEFAULT NULL COMMENT '弹屏率',
  `listened_at` int(11) DEFAULT NULL COMMENT '监听数量',
  `listened_rate` decimal(5,2) DEFAULT NULL COMMENT '监听率',
  `intervention_at` int(11) DEFAULT NULL COMMENT '介入数量',
  `intervention_rate` decimal(5,2) DEFAULT NULL COMMENT '介入率',
  `customer_count` int(11) DEFAULT NULL COMMENT '客户数量',
  `connected_customer_success_rate` decimal(5,2) DEFAULT NULL COMMENT '接通客户成功率',
  `intervention_customer_success_rate` decimal(5,2) DEFAULT NULL COMMENT '介入客户成功率',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `索引 2` (`date`,`agent_name`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.bus_report 的数据：~8 rows (大约)
/*!40000 ALTER TABLE `bus_report` DISABLE KEYS */;
INSERT INTO `bus_report` (`id`, `__uid__`, `date`, `agent_name`, `company_name`, `outbound_area`, `outbound_count`, `connection_rate`, `connection_count`, `screen_pop_count`, `screen_pop_rate`, `offline_screen_pop_count`, `offline_screen_pop_rate`, `pushed_at`, `pushed_rate`, `listened_at`, `listened_rate`, `intervention_at`, `intervention_rate`, `customer_count`, `connected_customer_success_rate`, `intervention_customer_success_rate`, `create_time`, `update_time`) VALUES
	(12, NULL, '2023-06-19', 'mo912143002', 'mo912143', '', 15764, 0.56, 8786, 120, 0.01, 44, 0.01, 76, 0.01, 43, 0.57, 10, 0.23, 2, 0.00, 0.20, '2023-06-20 02:50:15', '2023-06-23 20:13:47'),
	(13, NULL, '2023-06-20', 'mo912143002', 'mo912143', '', 16023, 0.54, 8730, 94, 0.01, 83, 0.01, 11, 0.00, 5, 0.45, 1, 0.20, 0, 0.00, 0.00, '2023-06-20 17:43:21', '2023-06-23 20:22:42'),
	(14, NULL, '2023-06-21', 'mo912143002', 'mo912143', '', 15999, 0.56, 8942, 93, 0.01, 93, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-23 18:34:30', '2023-06-23 20:22:43'),
	(15, NULL, '2023-06-22', 'mo912143002', 'mo912143', '', 14236, 0.87, 12372, 115, 0.01, 115, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-23 18:33:36', '2023-06-23 20:22:46'),
	(16, NULL, '2023-06-23', 'mo912143002', 'mo912143', '', 14314, 0.86, 12276, 110, 0.01, 104, 0.01, 6, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-23 18:18:20', '2023-06-23 20:25:06'),
	(25, NULL, '2023-06-24', 'mo912143002', 'mo912143', '', 14285, 0.86, 12320, 138, 0.01, 138, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-24 16:30:20', '2023-06-24 16:30:20'),
	(26, NULL, '2023-06-25', 'mo912143002', 'mo912143', '', 7165, 0.89, 6364, 59, 0.01, 59, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-25 16:30:10', '2023-06-25 16:30:10'),
	(27, 2, '2023-06-26', 'mo912143002', 'mo912143', '', 6066, 0.59, 3553, 32, 0.01, 32, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-26 16:30:07', '2023-06-26 20:29:38'),
	(28, 2, '2023-06-27', 'mo912143002', 'mo912143', '', 16565, 0.68, 11333, 124, 0.01, 124, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-27 16:30:17', '2023-06-28 03:53:00'),
	(29, 2, '2023-06-28', 'mo912143002', 'mo912143', '', 14682, 0.84, 12308, 116, 0.01, 116, 0.01, 0, 0.00, 0, 0.00, 0, 0.00, 0, 0.00, 0.00, '2023-06-28 16:30:19', '2023-06-28 16:30:19');
/*!40000 ALTER TABLE `bus_report` ENABLE KEYS */;

-- 导出  表 aicrm.depts 结构
CREATE TABLE IF NOT EXISTS `depts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL DEFAULT '',
  `parentId` int(11) NOT NULL DEFAULT '0',
  `sort` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `leader` varchar(100) DEFAULT NULL,
  `mobile` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.depts 的数据：~3 rows (大约)
/*!40000 ALTER TABLE `depts` DISABLE KEYS */;
INSERT INTO `depts` (`id`, `name`, `parentId`, `sort`, `status`, `leader`, `mobile`, `email`, `create_time`, `update_time`) VALUES
	(1, '客户组', 0, 1, 1, NULL, NULL, NULL, '2023-06-26 00:00:00', '2023-06-26 16:00:44'),
	(2, '部门12', 1, 2, 1, NULL, NULL, NULL, '2023-06-26 18:23:44', '2023-06-26 10:23:35'),
	(3, '部门13', 1, 3, 1, NULL, NULL, NULL, '2023-06-26 00:00:00', '2023-06-26 15:48:52');
/*!40000 ALTER TABLE `depts` ENABLE KEYS */;

-- 导出  表 aicrm.dict 结构
CREATE TABLE IF NOT EXISTS `dict` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentId` int(11) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `value` varchar(500) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `parentId` (`parentId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.dict 的数据：~7 rows (大约)
/*!40000 ALTER TABLE `dict` DISABLE KEYS */;
INSERT INTO `dict` (`id`, `parentId`, `remark`, `name`, `code`, `status`, `value`, `create_time`, `update_time`) VALUES
	(1, 0, NULL, '性别', 'gender', 1, NULL, NULL, NULL),
	(2, 1, NULL, '男', NULL, 1, '1', NULL, '2023-06-26 19:56:47'),
	(3, 1, NULL, '女', NULL, 1, '2', NULL, '2023-06-26 19:56:48'),
	(4, 1, NULL, '未知', NULL, 1, '0', NULL, '2023-06-26 19:56:50'),
	(5, 0, NULL, 'API', 'API', 1, NULL, '2023-06-26 20:06:06', '2023-06-26 20:06:41'),
	(6, 5, NULL, 'ai193', NULL, 1, 'ai193.ciopaas.com,be00bad65585da7e9202d30cef13a976,61a460cb2640e62246bb92166d574804', '2023-06-26 20:06:39', '2023-06-28 03:52:32'),
	(7, 0, NULL, '配置', 'config', 1, NULL, '2023-06-28 09:16:05', '2023-06-28 09:16:05');
/*!40000 ALTER TABLE `dict` ENABLE KEYS */;

-- 导出  表 aicrm.menus 结构
CREATE TABLE IF NOT EXISTS `menus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parentId` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `routeName` varchar(100) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  `component` varchar(100) DEFAULT NULL,
  `redirect` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `perm` varchar(100) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  `alwaysShow` int(11) DEFAULT NULL,
  `hidden` int(11) DEFAULT NULL,
  `keepAlive` int(11) DEFAULT NULL,
  `visible` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.menus 的数据：~12 rows (大约)
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` (`id`, `parentId`, `name`, `icon`, `routeName`, `path`, `component`, `redirect`, `type`, `perm`, `sort`, `alwaysShow`, `hidden`, `keepAlive`, `visible`, `create_time`, `update_time`) VALUES
	(1, 0, '系统管理', 'system', NULL, '/system', 'Layout', '/system/user', 'CATALOG', NULL, 1, NULL, NULL, 1, 1, '2023-06-26 20:07:20', '2023-06-27 17:05:07'),
	(2, 1, '用户管理', 'user', NULL, 'user', 'system/user/index', NULL, 'MENU', NULL, 1, NULL, NULL, 1, 1, '2023-06-26 20:07:21', '2023-06-27 17:05:09'),
	(3, 1, '角色管理', 'role', NULL, 'role', 'system/role/index', NULL, 'MENU', '', 2, NULL, NULL, 1, 1, '2023-06-26 20:07:22', '2023-06-27 17:05:12'),
	(4, 1, '菜单管理', 'menu', NULL, 'cmenu', 'system/menu/index', NULL, 'MENU', '', 3, NULL, NULL, 1, 1, '2023-06-26 20:07:22', '2023-06-27 17:05:13'),
	(5, 1, '部门管理', 'tree', NULL, 'dept', 'system/dept/index', NULL, 'MENU', NULL, 4, NULL, NULL, 1, 1, '2023-06-26 20:07:23', '2023-06-27 17:05:13'),
	(6, 1, '字典管理', 'dict', NULL, 'dict', 'system/dict/index', NULL, 'MENU', NULL, 5, NULL, NULL, 1, 1, '2023-06-26 20:07:23', '2023-06-27 17:05:14'),
	(40, 2, '新增用户', NULL, NULL, NULL, NULL, NULL, 'BUTTON', 'sys:user:add', 1, NULL, NULL, 1, 1, '2023-06-26 20:07:25', '2023-06-27 17:05:14'),
	(41, 2, '修改用户', NULL, NULL, NULL, NULL, NULL, 'BUTTON', 'sys:user:edit', 2, NULL, NULL, 1, 1, '2023-06-26 20:07:25', '2023-06-27 17:05:15'),
	(42, 2, '删除用户', NULL, NULL, NULL, NULL, NULL, 'BUTTON', 'sys:user:del', 3, NULL, NULL, 1, 1, '2023-06-26 20:07:26', '2023-06-27 17:05:16'),
	(43, 0, '数据分析', 'redis', NULL, '/analysis', 'Layout', '/analysis/report', 'CATALOG', NULL, 1, 1, NULL, 1, 1, '2023-06-26 00:00:00', '2023-06-27 17:05:17'),
	(44, 43, '人机耦合', 'dict', NULL, 'report', 'analysis/report/index', NULL, 'MENU', NULL, 1, NULL, NULL, 1, 1, '2023-06-26 00:00:00', '2023-06-27 17:05:17'),
	(46, 0, '流水管理', 'nested', NULL, '/customer', 'Layout', '/customer/calllog', 'CATALOG', NULL, 1, 1, NULL, 1, 1, '2023-06-26 18:59:52', '2023-06-27 19:38:28'),
	(47, 43, '手动报表', 'dict', NULL, 'semiauto', 'analysis/semiauto/index', NULL, 'MENU', NULL, 2, NULL, NULL, 1, 1, '2023-06-27 13:34:12', '2023-06-27 17:05:19'),
	(48, 46, '通话流水', 'order', NULL, 'calllog', 'customer/calllog/index', NULL, 'MENU', NULL, 1, NULL, NULL, NULL, 1, '2023-06-27 19:01:45', '2023-06-27 19:10:24');
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;

-- 导出  表 aicrm.roles 结构
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `code` varchar(50) DEFAULT NULL,
  `dataScope` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  `menus` varchar(100) DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.roles 的数据：~2 rows (大约)
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` (`id`, `name`, `code`, `dataScope`, `status`, `sort`, `menus`, `update_time`, `create_time`) VALUES
	(1, '系统管理员', 'ADMIN', 0, 1, 1, '1,2,40,41,42,3,4,5,6,43,44,47,46,48', '2023-06-28 23:42:07', '2023-06-26 08:19:47'),
	(6, '客户', 'CUSTOMER', 3, 1, 11, '46,48', '2023-06-27 19:39:02', '2023-06-26 00:00:00');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- 导出  表 aicrm.setting 结构
CREATE TABLE IF NOT EXISTS `setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `section` varchar(64) NOT NULL COMMENT '节',
  `key` varchar(64) NOT NULL COMMENT '键',
  `value` text NOT NULL COMMENT '值',
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_key_uindex` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='可修改配置';

-- 正在导出表  aicrm.setting 的数据：~2 rows (大约)
/*!40000 ALTER TABLE `setting` DISABLE KEYS */;
INSERT INTO `setting` (`id`, `section`, `key`, `value`, `description`) VALUES
	(1, 'api', 'url', 'ai193.ciopaas.com', NULL),
	(2, 'api', 'api_access_id', 'be00bad65585da7e9202d30cef13a976', NULL),
	(3, 'api', 'api_access_secret', '61a460cb2640e62246bb92166d574804', NULL);
/*!40000 ALTER TABLE `setting` ENABLE KEYS */;

-- 导出  表 aicrm.users 结构
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(120) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `roleIds` varchar(120) DEFAULT NULL,
  `nickname` varchar(100) DEFAULT NULL,
  `mobile` varchar(100) DEFAULT NULL,
  `genderLabel` varchar(10) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `deptId` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- 正在导出表  aicrm.users 的数据：~2 rows (大约)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `username`, `password`, `roleIds`, `nickname`, `mobile`, `genderLabel`, `avatar`, `email`, `status`, `deptId`, `create_time`, `update_time`) VALUES
	(1, 'admin', '0938dd517f1326876d52f0373a733601', '1', 'admin', NULL, NULL, 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', NULL, 1, 1, '2023-06-27 00:41:28', '2023-06-26 16:41:19'),
	(2, 'ai193', '1a9c762dff80b15930fb05446cc9d396', '6', 'ai193', NULL, NULL, 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', NULL, 1, 1, '2023-06-26 00:00:00', '2023-06-27 19:42:11'),
	(3, 'ai194', NULL, '6', 'ai194', NULL, NULL, NULL, NULL, 1, 1, '2023-06-27 19:41:57', '2023-06-27 19:41:57');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
