-- --------------------------------------------------------
-- Máy chủ:                      127.0.0.1
-- Server version:               8.4.0 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Phiên bản:           12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for quanlynongsan
CREATE DATABASE IF NOT EXISTS `quanlynongsan` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `quanlynongsan`;

-- Dumping structure for table quanlynongsan.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_group: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_permission: ~108 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add auth group', 7, 'add_authgroup'),
	(26, 'Can change auth group', 7, 'change_authgroup'),
	(27, 'Can delete auth group', 7, 'delete_authgroup'),
	(28, 'Can view auth group', 7, 'view_authgroup'),
	(29, 'Can add auth group permissions', 8, 'add_authgrouppermissions'),
	(30, 'Can change auth group permissions', 8, 'change_authgrouppermissions'),
	(31, 'Can delete auth group permissions', 8, 'delete_authgrouppermissions'),
	(32, 'Can view auth group permissions', 8, 'view_authgrouppermissions'),
	(33, 'Can add auth permission', 9, 'add_authpermission'),
	(34, 'Can change auth permission', 9, 'change_authpermission'),
	(35, 'Can delete auth permission', 9, 'delete_authpermission'),
	(36, 'Can view auth permission', 9, 'view_authpermission'),
	(37, 'Can add auth user', 10, 'add_authuser'),
	(38, 'Can change auth user', 10, 'change_authuser'),
	(39, 'Can delete auth user', 10, 'delete_authuser'),
	(40, 'Can view auth user', 10, 'view_authuser'),
	(41, 'Can add auth user groups', 11, 'add_authusergroups'),
	(42, 'Can change auth user groups', 11, 'change_authusergroups'),
	(43, 'Can delete auth user groups', 11, 'delete_authusergroups'),
	(44, 'Can view auth user groups', 11, 'view_authusergroups'),
	(45, 'Can add auth user user permissions', 12, 'add_authuseruserpermissions'),
	(46, 'Can change auth user user permissions', 12, 'change_authuseruserpermissions'),
	(47, 'Can delete auth user user permissions', 12, 'delete_authuseruserpermissions'),
	(48, 'Can view auth user user permissions', 12, 'view_authuseruserpermissions'),
	(49, 'Can add danhmuc', 13, 'add_danhmuc'),
	(50, 'Can change danhmuc', 13, 'change_danhmuc'),
	(51, 'Can delete danhmuc', 13, 'delete_danhmuc'),
	(52, 'Can view danhmuc', 13, 'view_danhmuc'),
	(53, 'Can add django admin log', 14, 'add_djangoadminlog'),
	(54, 'Can change django admin log', 14, 'change_djangoadminlog'),
	(55, 'Can delete django admin log', 14, 'delete_djangoadminlog'),
	(56, 'Can view django admin log', 14, 'view_djangoadminlog'),
	(57, 'Can add django content type', 15, 'add_djangocontenttype'),
	(58, 'Can change django content type', 15, 'change_djangocontenttype'),
	(59, 'Can delete django content type', 15, 'delete_djangocontenttype'),
	(60, 'Can view django content type', 15, 'view_djangocontenttype'),
	(61, 'Can add django migrations', 16, 'add_djangomigrations'),
	(62, 'Can change django migrations', 16, 'change_djangomigrations'),
	(63, 'Can delete django migrations', 16, 'delete_djangomigrations'),
	(64, 'Can view django migrations', 16, 'view_djangomigrations'),
	(65, 'Can add django session', 17, 'add_djangosession'),
	(66, 'Can change django session', 17, 'change_djangosession'),
	(67, 'Can delete django session', 17, 'delete_djangosession'),
	(68, 'Can view django session', 17, 'view_djangosession'),
	(69, 'Can add donhang', 18, 'add_donhang'),
	(70, 'Can change donhang', 18, 'change_donhang'),
	(71, 'Can delete donhang', 18, 'delete_donhang'),
	(72, 'Can view donhang', 18, 'view_donhang'),
	(73, 'Can add giamgia', 19, 'add_giamgia'),
	(74, 'Can change giamgia', 19, 'change_giamgia'),
	(75, 'Can delete giamgia', 19, 'delete_giamgia'),
	(76, 'Can view giamgia', 19, 'view_giamgia'),
	(77, 'Can add kho', 20, 'add_kho'),
	(78, 'Can change kho', 20, 'change_kho'),
	(79, 'Can delete kho', 20, 'delete_kho'),
	(80, 'Can view kho', 20, 'view_kho'),
	(81, 'Can add nguoidung', 21, 'add_nguoidung'),
	(82, 'Can change nguoidung', 21, 'change_nguoidung'),
	(83, 'Can delete nguoidung', 21, 'delete_nguoidung'),
	(84, 'Can view nguoidung', 21, 'view_nguoidung'),
	(85, 'Can add nhacungcap', 22, 'add_nhacungcap'),
	(86, 'Can change nhacungcap', 22, 'change_nhacungcap'),
	(87, 'Can delete nhacungcap', 22, 'delete_nhacungcap'),
	(88, 'Can view nhacungcap', 22, 'view_nhacungcap'),
	(89, 'Can add nhanvien', 23, 'add_nhanvien'),
	(90, 'Can change nhanvien', 23, 'change_nhanvien'),
	(91, 'Can delete nhanvien', 23, 'delete_nhanvien'),
	(92, 'Can view nhanvien', 23, 'view_nhanvien'),
	(93, 'Can add nongsan', 24, 'add_nongsan'),
	(94, 'Can change nongsan', 24, 'change_nongsan'),
	(95, 'Can delete nongsan', 24, 'delete_nongsan'),
	(96, 'Can view nongsan', 24, 'view_nongsan'),
	(97, 'Can add ordernhacungcap', 25, 'add_ordernhacungcap'),
	(98, 'Can change ordernhacungcap', 25, 'change_ordernhacungcap'),
	(99, 'Can delete ordernhacungcap', 25, 'delete_ordernhacungcap'),
	(100, 'Can view ordernhacungcap', 25, 'view_ordernhacungcap'),
	(101, 'Can add taikhoan', 26, 'add_taikhoan'),
	(102, 'Can change taikhoan', 26, 'change_taikhoan'),
	(103, 'Can delete taikhoan', 26, 'delete_taikhoan'),
	(104, 'Can view taikhoan', 26, 'view_taikhoan'),
	(105, 'Can add tonkho', 27, 'add_tonkho'),
	(106, 'Can change tonkho', 27, 'change_tonkho'),
	(107, 'Can delete tonkho', 27, 'delete_tonkho'),
	(108, 'Can view tonkho', 27, 'view_tonkho'),
	(109, 'Can add don hang detail', 28, 'add_donhangdetail'),
	(110, 'Can change don hang detail', 28, 'change_donhangdetail'),
	(111, 'Can delete don hang detail', 28, 'delete_donhangdetail'),
	(112, 'Can view don hang detail', 28, 'view_donhangdetail'),
	(113, 'Can add cart', 29, 'add_cart'),
	(114, 'Can change cart', 29, 'change_cart'),
	(115, 'Can delete cart', 29, 'delete_cart'),
	(116, 'Can view cart', 29, 'view_cart');

-- Dumping structure for table quanlynongsan.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_user: ~1 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$720000$xbsk8TSUEYSv4N1vElCNvR$EmgbPu9o3ta5X8XpfwCxhtNjM1R7tLUDLK/eAWOZ4AI=', '2024-07-02 02:31:00.485428', 1, 'admin', '', '', 'quachduy1762003@gmail.com', 1, 1, '2024-06-25 00:04:11.253643');

-- Dumping structure for table quanlynongsan.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.cart
CREATE TABLE IF NOT EXISTS `cart` (
  `cart_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `nongsan_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `quantity` int NOT NULL DEFAULT (0),
  PRIMARY KEY (`cart_id`),
  KEY `FK_cart_nguoidung` (`user_id`),
  KEY `FK_cart_nongsan` (`nongsan_id`),
  CONSTRAINT `FK_cart_nguoidung` FOREIGN KEY (`user_id`) REFERENCES `nguoidung` (`MaNguoiDung`),
  CONSTRAINT `FK_cart_nongsan` FOREIGN KEY (`nongsan_id`) REFERENCES `nongsan` (`IdNongSan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.cart: ~2 rows (approximately)
INSERT INTO `cart` (`cart_id`, `user_id`, `nongsan_id`, `quantity`) VALUES
	('c1', 'KH-76dbc388-6f15-4bd4-8f4c-e201e7b08f33', 'ns1', 17),
	('c2', 'KH-76dbc388-6f15-4bd4-8f4c-e201e7b08f33', 'ns2', 2);

-- Dumping structure for table quanlynongsan.danhmuc
CREATE TABLE IF NOT EXISTS `danhmuc` (
  `MaDanhMuc` varchar(50) NOT NULL,
  `TenDanhMuc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`MaDanhMuc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.danhmuc: ~6 rows (approximately)
INSERT INTO `danhmuc` (`MaDanhMuc`, `TenDanhMuc`) VALUES
	('dm1', 'Ngũ Cốc'),
	('dm2', 'Trứng-Sữa'),
	('dm3', 'Rau'),
	('dm4', 'Hoa Quả'),
	('dm5', 'Hải Sản'),
	('dm6', 'Gia Vị');

-- Dumping structure for table quanlynongsan.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.django_admin_log: ~15 rows (approximately)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2024-06-25 00:05:09.741295', 'dm1', 'Danhmuc object (dm1)', 1, '[{"added": {}}]', 13, 1),
	(2, '2024-06-25 00:05:27.094150', 'dm2', 'Danhmuc object (dm2)', 1, '[{"added": {}}]', 13, 1),
	(3, '2024-06-25 00:05:34.823302', 'dm3', 'Danhmuc object (dm3)', 1, '[{"added": {}}]', 13, 1),
	(4, '2024-06-25 00:05:48.214342', 'dm4', 'Danhmuc object (dm4)', 1, '[{"added": {}}]', 13, 1),
	(5, '2024-06-25 00:06:00.587861', 'dm5', 'Danhmuc object (dm5)', 1, '[{"added": {}}]', 13, 1),
	(6, '2024-06-25 00:06:20.414865', 'dm6', 'Danhmuc object (dm6)', 1, '[{"added": {}}]', 13, 1),
	(7, '2024-06-25 06:13:10.741401', 'ns1', 'Nongsan object (ns1)', 1, '[{"added": {}}]', 24, 1),
	(8, '2024-06-25 06:14:24.305537', 'ns1', 'Nongsan object (ns1)', 2, '[{"changed": {"fields": ["Image"]}}]', 24, 1),
	(9, '2024-06-25 06:25:38.341108', 'ns1', 'Nongsan object (ns1)', 2, '[{"changed": {"fields": ["Image"]}}]', 24, 1),
	(10, '2024-06-25 06:40:00.369424', 'KH1', 'Nguoidung object (KH1)', 1, '[{"added": {}}]', 21, 1),
	(11, '2024-06-25 06:40:27.463067', 'TK1', 'Taikhoan object (TK1)', 1, '[{"added": {}}]', 26, 1),
	(12, '2024-06-25 06:40:36.597856', 'KH1', 'Nguoidung object (KH1)', 2, '[{"changed": {"fields": ["Idtaikhoan"]}}]', 21, 1),
	(13, '2024-06-25 06:46:31.200400', 'ns1', 'Nongsan object (ns1)', 2, '[{"changed": {"fields": ["Image"]}}]', 24, 1),
	(14, '2024-06-25 06:50:53.547727', 'dh1', 'Donhang object (dh1)', 1, '[{"added": {}}]', 18, 1),
	(15, '2024-06-25 09:05:15.849204', 'KH1', 'Nguoidung object (KH1)', 2, '[{"changed": {"fields": ["Image"]}}]', 21, 1),
	(16, '2024-06-25 09:34:05.481691', 'KH1', 'Nguoidung object (KH1)', 2, '[{"changed": {"fields": ["Image"]}}]', 21, 1),
	(17, '2024-06-25 15:00:13.917046', 'KH1', 'Nguoidung object (KH1)', 2, '[{"changed": {"fields": ["Image"]}}]', 21, 1),
	(18, '2024-06-26 00:11:58.956403', 'mdhdt1', 'mdhdt1', 1, '[{"added": {}}]', 28, 1),
	(19, '2024-06-26 00:55:07.511359', 'dh1', 'Donhang object (dh1)', 2, '[]', 18, 1),
	(20, '2024-06-26 08:03:44.730681', 'ns2', 'Nongsan object (ns2)', 1, '[{"added": {}}]', 24, 1),
	(21, '2024-06-26 08:04:04.581792', 'mdhdt2', 'mdhdt2', 1, '[{"added": {}}]', 28, 1);

-- Dumping structure for table quanlynongsan.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.django_content_type: ~27 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(7, 'app', 'authgroup'),
	(8, 'app', 'authgrouppermissions'),
	(9, 'app', 'authpermission'),
	(10, 'app', 'authuser'),
	(11, 'app', 'authusergroups'),
	(12, 'app', 'authuseruserpermissions'),
	(29, 'app', 'cart'),
	(13, 'app', 'danhmuc'),
	(14, 'app', 'djangoadminlog'),
	(15, 'app', 'djangocontenttype'),
	(16, 'app', 'djangomigrations'),
	(17, 'app', 'djangosession'),
	(18, 'app', 'donhang'),
	(28, 'app', 'donhangdetail'),
	(19, 'app', 'giamgia'),
	(20, 'app', 'kho'),
	(21, 'app', 'nguoidung'),
	(22, 'app', 'nhacungcap'),
	(23, 'app', 'nhanvien'),
	(24, 'app', 'nongsan'),
	(25, 'app', 'ordernhacungcap'),
	(26, 'app', 'taikhoan'),
	(27, 'app', 'tonkho'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Dumping structure for table quanlynongsan.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.django_migrations: ~18 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2024-06-24 23:58:47.724915'),
	(2, 'auth', '0001_initial', '2024-06-24 23:58:48.618985'),
	(3, 'admin', '0001_initial', '2024-06-24 23:58:48.846077'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2024-06-24 23:58:48.855076'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-06-24 23:58:48.867615'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2024-06-24 23:58:48.969958'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2024-06-24 23:58:49.076103'),
	(8, 'auth', '0003_alter_user_email_max_length', '2024-06-24 23:58:49.110708'),
	(9, 'auth', '0004_alter_user_username_opts', '2024-06-24 23:58:49.125220'),
	(10, 'auth', '0005_alter_user_last_login_null', '2024-06-24 23:58:49.229432'),
	(11, 'auth', '0006_require_contenttypes_0002', '2024-06-24 23:58:49.233427'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2024-06-24 23:58:49.246076'),
	(13, 'auth', '0008_alter_user_username_max_length', '2024-06-24 23:58:49.391738'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2024-06-24 23:58:49.520024'),
	(15, 'auth', '0010_alter_group_name_max_length', '2024-06-24 23:58:49.548328'),
	(16, 'auth', '0011_update_proxy_permissions', '2024-06-24 23:58:49.560321'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2024-06-24 23:58:49.683749'),
	(18, 'sessions', '0001_initial', '2024-06-24 23:58:49.758989'),
	(19, 'app', '0001_initial', '2024-06-25 00:01:42.161540'),
	(20, 'app', '0002_donhangdetail', '2024-06-25 23:43:38.726182'),
	(21, 'app', '0003_alter_donhangdetail_options', '2024-06-25 23:51:57.315563'),
	(22, 'app', '0004_alter_donhangdetail_table', '2024-06-26 00:09:54.976193'),
	(23, 'app', '0005_cart', '2024-07-02 02:28:38.956894');

-- Dumping structure for table quanlynongsan.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.django_session: ~2 rows (approximately)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('n77305232bl4fxqcj1yo77vabnanm0ji', '.eJxVj71qAzEQhF_lUB3s1d_plCpFigODIZDScCjSRlJsSbYPFU7Iu0dKd93y7cww80NsQHu-FB8zeSbvB0qeSDLZ1xJdzb6xw9zZORgb5vZYsknY8Fs9VQCkNgztoBROlSJqO7zWx0aPycRLM9xqI64-qBoZAH_xne9sSRt1TMbjUu_dsc8l-9Xk_beUI5dawiQUFQsHIRCcZEI5JWGkEvn0CTAZqz-MZruvq9-EGufuuK4tcv4vDcOxt3U6bmTXUHKfBnzkTHEGlJPfP2nUWg8:1sN7hZ:3qEWf2DyPWNcSCEuj-sk4hZi_AI3PJhWvqO61egWrQs', '2024-07-12 09:15:29.734697'),
	('ycxbyejeqm03xefp8uyw3ws3gequo7sq', '.eJxdkDtPxDAQhP_KKTWO_I5NhRDFSScKJMqTIq8fcbjEQcm5QIj_zgZRcHSrnflmx_5sfI7-Mi3DWJr75vVEXOqC54ISESMjUiVBLBWJmMCBd7gUMjV3zezKUJcx1DIgdzqSTgfwwhiiE1NEQpDEJOlJ5JTFDqhJQiB3yc7nI8J9cXNE9KWeK6WR-XzAgTF6rixG6w9P9ePGH2c3Tgi4h2GfWr_MN_o4uyH2dUVPqdP0V3IhrHHbED7-HKOHsl8JdrxJeM9L2StRoQU-FYuj3Lt6zX3d4tqPAcV_O3D-EssuhDfMWLBWua4jtLul_VW39nkJcXr89d4EZLdlpGWgRlNlE9cKpNTahhAAuOXJOustlZAMMPAghQHRKcnxs0Ep7bxSoJqvb6HmkGc:1sOTIK:YUo6OaxhhubSDyXVfbhhNtY0OAO4Z3qqqqAxI70Vc4M', '2024-07-16 02:31:00.488462');

-- Dumping structure for table quanlynongsan.donhang
CREATE TABLE IF NOT EXISTS `donhang` (
  `MaDonHang` varchar(50) NOT NULL,
  `MaNguoiDung` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `TongGia` decimal(15,2) DEFAULT NULL,
  `NgayDat` date DEFAULT NULL,
  `TrangThai` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`MaDonHang`),
  KEY `MaNguoiDung` (`MaNguoiDung`),
  CONSTRAINT `donhang_ibfk_1` FOREIGN KEY (`MaNguoiDung`) REFERENCES `nguoidung` (`MaNguoiDung`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.donhang: ~1 rows (approximately)
INSERT INTO `donhang` (`MaDonHang`, `MaNguoiDung`, `TongGia`, `NgayDat`, `TrangThai`) VALUES
	('dh1', 'KH1', 25000.00, '2024-06-25', 'Đã mua'),
	('DH2b660afd-86d3-4044-abf2-7bce09c013d1', 'KH-76dbc388-6f15-4bd4-8f4c-e201e7b08f33', NULL, NULL, 'Chưa thanh toán'),
	('DH3cd8c60b-e136-4266-92e1-d836dbe09491', 'KH-76dbc388-6f15-4bd4-8f4c-e201e7b08f33', NULL, NULL, NULL);

-- Dumping structure for table quanlynongsan.donhang_detail
CREATE TABLE IF NOT EXISTS `donhang_detail` (
  `MaDonHangDetail` varchar(255) NOT NULL,
  `MaDonHang` varchar(255) NOT NULL,
  `IdNongSan` varchar(255) NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`MaDonHangDetail`),
  KEY `FK__donhang` (`MaDonHang`),
  KEY `FK_donhang_detail_nongsan` (`IdNongSan`),
  CONSTRAINT `FK__donhang` FOREIGN KEY (`MaDonHang`) REFERENCES `donhang` (`MaDonHang`),
  CONSTRAINT `FK_donhang_detail_nongsan` FOREIGN KEY (`IdNongSan`) REFERENCES `nongsan` (`IdNongSan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.donhang_detail: ~0 rows (approximately)
INSERT INTO `donhang_detail` (`MaDonHangDetail`, `MaDonHang`, `IdNongSan`, `Quantity`) VALUES
	('', 'DH2b660afd-86d3-4044-abf2-7bce09c013d1', 'ns2', 1),
	('DHT-1857e012-d373-49bb-a4ca-8c39981d1eed', 'DH2b660afd-86d3-4044-abf2-7bce09c013d1', 'ns1', 1);

-- Dumping structure for table quanlynongsan.giamgia
CREATE TABLE IF NOT EXISTS `giamgia` (
  `MaGiamGia` varchar(50) NOT NULL,
  `IdNongSan` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `PhanTramGiam` decimal(5,2) NOT NULL,
  `NgayBatDau` date NOT NULL,
  `NgayKetThuc` date NOT NULL,
  `MoTa` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`MaGiamGia`),
  KEY `IdNongSan` (`IdNongSan`),
  CONSTRAINT `giamgia_ibfk_1` FOREIGN KEY (`IdNongSan`) REFERENCES `nongsan` (`IdNongSan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.giamgia: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.kho
CREATE TABLE IF NOT EXISTS `kho` (
  `IdKho` varchar(50) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `DiaChi` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`IdKho`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.kho: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.nguoidung
CREATE TABLE IF NOT EXISTS `nguoidung` (
  `MaNguoiDung` varchar(50) NOT NULL,
  `HoVaTen` varchar(100) DEFAULT NULL,
  `DiaChi` varchar(255) DEFAULT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `IdTaiKhoan` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `image` text,
  PRIMARY KEY (`MaNguoiDung`),
  KEY `FK_nguoidung_taikhoan` (`IdTaiKhoan`),
  CONSTRAINT `FK_nguoidung_taikhoan` FOREIGN KEY (`IdTaiKhoan`) REFERENCES `taikhoan` (`IdTaiKhoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.nguoidung: ~1 rows (approximately)
INSERT INTO `nguoidung` (`MaNguoiDung`, `HoVaTen`, `DiaChi`, `Phone`, `Email`, `IdTaiKhoan`, `image`) VALUES
	('KH-76dbc388-6f15-4bd4-8f4c-e201e7b08f33', 'Quách Đức Duy', 'Hà nội', '0363273201', 'a@gmail.com', 'TK-af7dc230-3ee1-45f3-903f-8d2b273ee34f', ''),
	('KH1', 'Quách Đức Duy', 'Hà Nội', '03632732013', 'quachduy1762003@gmail.com', 'TK1', 'z5563595084714_3044e0d5247d750615e38f008ac9ba92.jpg'),
	('KHa00b9559-6409-4d4b-a6e0-b332861311fe', 'Duy', 'Tân Hội', '03632732013', 'quachduy@gmail.com', 'TK84497603-0a3f-403f-93bc-31eaec915183', '');

-- Dumping structure for table quanlynongsan.nhacungcap
CREATE TABLE IF NOT EXISTS `nhacungcap` (
  `MaNhaCungCap` varchar(50) NOT NULL,
  `TenNhaCungCap` varchar(100) DEFAULT NULL,
  `DiaChi` varchar(255) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `SDT` varchar(20) DEFAULT NULL,
  `NongSanId` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`MaNhaCungCap`),
  KEY `NongSanId` (`NongSanId`),
  CONSTRAINT `nhacungcap_ibfk_1` FOREIGN KEY (`NongSanId`) REFERENCES `nongsan` (`IdNongSan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.nhacungcap: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.nhanvien
CREATE TABLE IF NOT EXISTS `nhanvien` (
  `MaNhanVien` varchar(50) NOT NULL,
  `TenNhanVien` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `SoDienThoai` varchar(20) DEFAULT NULL,
  `Luong` decimal(12,2) DEFAULT NULL,
  `CaLamViec` varchar(50) DEFAULT NULL,
  `IdTaiKhoan` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `image` text,
  PRIMARY KEY (`MaNhanVien`),
  KEY `FK_nhanvien_taikhoan` (`IdTaiKhoan`),
  CONSTRAINT `FK_nhanvien_taikhoan` FOREIGN KEY (`IdTaiKhoan`) REFERENCES `taikhoan` (`IdTaiKhoan`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.nhanvien: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.nongsan
CREATE TABLE IF NOT EXISTS `nongsan` (
  `IdNongSan` varchar(50) NOT NULL,
  `Ten` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `MoTa` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Gia` decimal(15,2) NOT NULL,
  `TrongLuong` decimal(10,2) NOT NULL,
  `MaDanhMuc` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`IdNongSan`),
  KEY `MaDanhMuc` (`MaDanhMuc`),
  CONSTRAINT `nongsan_ibfk_1` FOREIGN KEY (`MaDanhMuc`) REFERENCES `danhmuc` (`MaDanhMuc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.nongsan: ~1 rows (approximately)
INSERT INTO `nongsan` (`IdNongSan`, `Ten`, `MoTa`, `Gia`, `TrongLuong`, `MaDanhMuc`, `image`) VALUES
	('ns1', 'Gạo nếp', 'Ngon dẻo', 25000.00, 1500.00, 'dm1', 'vegetable-item-5_jhVE32O.jpg'),
	('ns2', 'Táo', 'vdvds', 30000.00, 1500.00, 'dm2', 'best-product-6_dKVeTD2.jpg');

-- Dumping structure for table quanlynongsan.ordernhacungcap
CREATE TABLE IF NOT EXISTS `ordernhacungcap` (
  `IdOrder` varchar(50) NOT NULL,
  `NhaCungCapId` varchar(50) DEFAULT NULL,
  `NgayGiaoDich` date DEFAULT NULL,
  `LoaiGiaoDich` enum('Purchase','Return') DEFAULT NULL,
  `SoLuong` int DEFAULT NULL,
  PRIMARY KEY (`IdOrder`),
  KEY `NhaCungCapId` (`NhaCungCapId`),
  CONSTRAINT `ordernhacungcap_ibfk_1` FOREIGN KEY (`NhaCungCapId`) REFERENCES `nhacungcap` (`MaNhaCungCap`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.ordernhacungcap: ~0 rows (approximately)

-- Dumping structure for table quanlynongsan.taikhoan
CREATE TABLE IF NOT EXISTS `taikhoan` (
  `IdTaiKhoan` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `UserName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IdTaiKhoan`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.taikhoan: ~0 rows (approximately)
INSERT INTO `taikhoan` (`IdTaiKhoan`, `UserName`, `Password`, `Role`) VALUES
	('TK-af7dc230-3ee1-45f3-903f-8d2b273ee34f', 'quachduy', 'pbkdf2_sha256$720000$LjxmdG8TU6HGKSvZk6Rwi2$bGAcymirHA9Twt2vL5nNNdYcOCp88qNG8KX/tRdLyIc=', 'customer'),
	('TK1', 'admin', '123', 'admin'),
	('TK84497603-0a3f-403f-93bc-31eaec915183', 'user', '12345678', 'customer');

-- Dumping structure for table quanlynongsan.tonkho
CREATE TABLE IF NOT EXISTS `tonkho` (
  `IdTonKho` varchar(50) NOT NULL,
  `IdNongSan` varchar(50) DEFAULT NULL,
  `IdKho` varchar(50) DEFAULT NULL,
  `SoLuong` int DEFAULT NULL,
  `NgayNhapVao` date DEFAULT NULL,
  `NgayHetHan` date DEFAULT NULL,
  PRIMARY KEY (`IdTonKho`),
  KEY `IdNongSan` (`IdNongSan`),
  KEY `IdKho` (`IdKho`),
  CONSTRAINT `tonkho_ibfk_1` FOREIGN KEY (`IdNongSan`) REFERENCES `nongsan` (`IdNongSan`),
  CONSTRAINT `tonkho_ibfk_2` FOREIGN KEY (`IdKho`) REFERENCES `kho` (`IdKho`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table quanlynongsan.tonkho: ~0 rows (approximately)

-- Dumping structure for procedure quanlynongsan.update_inventory_after_order
DELIMITER //
CREATE PROCEDURE `update_inventory_after_order`(
    IN p_order_detail_id VARCHAR(255),
    IN p_order_id VARCHAR(255)
)
BEGIN
    DECLARE v_product_id VARCHAR(255);
    DECLARE v_quantity INT;
    DECLARE v_message VARCHAR(100);

    SET v_message = '';

    SELECT product_id, quantity INTO v_product_id, v_quantity
    FROM orderdetails
    WHERE order_detail_id = p_order_detail_id AND order_id = p_order_id;

    IF v_quantity > 0 THEN
        UPDATE inventory
        SET quantity = quantity - v_quantity
        WHERE product_id = v_product_id AND kho_id = 'kho1'; -- Thêm điều kiện WHERE

        IF ROW_COUNT() > 0 THEN -- Kiểm tra xem có bản ghi nào được cập nhật hay không
            SET v_message = 'Đã trừ số lượng từ kho 1.';
        ELSE
            SELECT quantity INTO v_quantity
            FROM inventory
            WHERE product_id = v_product_id AND kho_id = 'kho2';

            IF v_quantity > 0 THEN
                UPDATE inventory
                SET quantity = quantity - v_quantity
                WHERE product_id = v_product_id AND kho_id = 'kho2'; -- Thêm điều kiện WHERE

                IF ROW_COUNT() > 0 THEN
                    SET v_message = 'Đã trừ số lượng từ kho 2.';
                ELSE
                    SET v_message = 'Hết hàng.';
                END IF;
            ELSE
                SET v_message = 'Hết hàng.';
            END IF;
        END IF;
    ELSE
        SET v_message = 'Số lượng không hợp lệ.';
    END IF;

END//
DELIMITER ;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
