-- MySQL dump 10.13  Distrib 8.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `follower_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test','test',0,'2024-04-30 21:05:51'),(2,'江戶川柯南','柯南','4869',1012234,'2024-04-30 21:14:18'),(3,'毛利蘭','小蘭','05',142455,'2024-04-30 21:14:18'),(4,'Gin','黑衣人','7',80,'2024-04-30 21:14:18'),(5,'目暮十三','警官','13',135,'2024-04-30 21:14:18'),(6,'a','a','a',0,'2024-05-11 12:30:13');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `member_id` bigint NOT NULL,
  `content` varchar(255) NOT NULL,
  `like_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,2,'東京死神',10077,'2024-05-01 14:46:58'),(2,1,'彭彭就是讚',30004,'2024-05-01 14:46:58'),(3,1,'看彭彭寫code好療癒',1588,'2024-05-01 14:46:58'),(4,4,'整個組織只有你認真工作',5555,'2024-05-01 14:46:58'),(7,3,'空手道冠軍',0,'2024-05-11 13:53:58'),(8,3,'東京',0,'2024-05-11 13:54:19'),(9,2,'快給我解藥',0,'2024-05-11 13:59:29'),(10,4,'這麼遠也可以',0,'2024-05-11 14:00:42'),(11,6,'路人',0,'2024-05-11 14:01:50');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week6`
--

DROP TABLE IF EXISTS `week6`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week6` (
  `member_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week6`
--

LOCK TABLES `week6` WRITE;
/*!40000 ALTER TABLE `week6` DISABLE KEYS */;
INSERT INTO `week6` VALUES (1,'a','a','a','2024-05-08 22:04:03'),(2,'b','b','b','2024-05-08 22:05:01'),(3,'柯南','conan','conan','2024-05-09 16:15:26'),(4,'毛利','mori','mori','2024-05-09 16:29:33'),(5,'博士','doctor','doctor','2024-05-09 16:36:27'),(6,'小蘭','ran','ran','2024-05-10 22:54:50'),(7,'部長','部長','bubu','2024-05-10 23:28:21');
/*!40000 ALTER TABLE `week6` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `week6message`
--

DROP TABLE IF EXISTS `week6message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `week6message` (
  `message_id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  `message_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  KEY `username` (`username`),
  CONSTRAINT `week6message_ibfk_1` FOREIGN KEY (`username`) REFERENCES `week6` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `week6message`
--

LOCK TABLES `week6message` WRITE;
/*!40000 ALTER TABLE `week6message` DISABLE KEYS */;
INSERT INTO `week6message` VALUES (1,'a','hello','2024-05-09 14:46:09'),(2,'a','好吃好吃','2024-05-09 14:52:31'),(3,'a','今天風很大','2024-05-09 14:55:20'),(4,'a','第四個','2024-05-09 14:58:13'),(5,'a','喝茶','2024-05-09 15:03:13'),(6,'a','震動','2024-05-09 15:05:30'),(7,'b','哈哈哈','2024-05-09 15:12:45'),(9,'conan','真相只有一個','2024-05-09 16:15:49'),(10,'ran','新一你怎麼還不回來','2024-05-10 22:56:05'),(14,'部長','九州真棒','2024-05-10 23:29:26'),(15,'部長','熊本第一','2024-05-10 23:29:35');
/*!40000 ALTER TABLE `week6message` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-11 14:07:29
