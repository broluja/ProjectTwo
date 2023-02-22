-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: localhost    Database: fletnix
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actors`
--

DROP TABLE IF EXISTS `actors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actors` (
  `id` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actors`
--

LOCK TABLES `actors` WRITE;
/*!40000 ALTER TABLE `actors` DISABLE KEYS */;
INSERT INTO `actors` VALUES ('11a96074-48db-4967-a8fe-6330dc091ef7','Jerry','Seinfeld','1966-03-22','USA'),('15be9b8e-36d8-4fb1-9f75-4e5fb4f0e737','Denzel','Washington','1954-12-28','USA'),('1a38cfa7-a1a5-4b48-b223-54b2844a960e','John','Goodman','1947-02-02','USA'),('1efcd0de-d8fe-4677-b9df-fe0fb37ab1d1','Bette','Davis','1908-04-05','USA'),('393a776c-610f-41c6-8365-9d7e71f49f1b','Katharine','Hepburn','1907-05-12','USA'),('3ba7ef2c-db21-4979-ae3b-a8b55d3e367a','Ray','Liotta','1952-12-01','USA'),('4d59a59e-8d88-4ccf-b9c8-33a14be815a0','Diane','Keaton','1956-09-01','USA'),('4d8a5663-299d-45b9-bf55-61e422ec9d0f','Jodie','Foster','1973-08-17','USA'),('5589c5e6-0cd8-466f-8e50-7b608686e9e8','Samuel L.','Jackson','1955-11-22','USA'),('56016e8f-6ae3-414f-bfd6-f36a31f79aca','James','Caan','1945-09-01','USA'),('7ad5c41f-8d4c-4102-adad-82ebe20fbf39','Cate','Blanchet','1969-05-17','USA'),('876413cd-926f-42d5-a472-9cc2a8a5cc25','Cary','Grant','1932-12-01','USA'),('93e398a4-8c34-4cde-bec4-c51cf952b832','Marlon','Brando','1943-08-17','USA'),('99b5058a-dcfb-4ded-802f-b441add9bfee','Al','Pacino','1949-09-01','USA'),('a7971c40-7a51-4547-8c34-3d39f5eafefe','Tom','Hanks','1943-08-17','USA'),('b96cefe9-6fd0-4e44-bd39-3a3e10bf3703','Sophia','Loren','1935-08-17','Italy'),('c5687dff-2e54-41c6-8c56-875dfb660247','Jack','Nicholson','1943-08-17','USA'),('cdc49f10-71f5-40cc-b99d-5b9b805b5e83','Robert','De Niro','1943-08-17','USA'),('da4f95f2-51d8-48c2-abc4-1b14ff1f374a','Kate','Winslet','1981-03-22','England'),('de2b26db-0858-4933-84c0-ee4bb726dd2a','Morgan','Freeman','1945-08-17','USA'),('e01d8601-1bd8-461b-ab52-5410516f2778','Bruce','Willis','1949-11-22','USA'),('e0e63bea-23c1-46be-9ece-2d0aae20d4b1','Vivien','Leigh','1933-08-17','England'),('e2b420f8-fafc-498f-9aa7-897c2cad29fa','John','Travolta','1956-11-22','USA'),('e5bda776-d7aa-4332-96d4-dff8c897fd18','Billy','Zane','1977-09-22','USA'),('e70d72a8-0c53-45a3-b8e8-feb4519584d2','Meryl ','Streep','1949-08-17','USA'),('f1f8ca6b-3809-45b1-a221-172dfdf89dd6','Leonardo','Di Caprio','1981-09-22','USA');
/*!40000 ALTER TABLE `actors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('5bc3cd50-65bf-4584-9a36-ccfbc09b2d58','Branko','Olujic','1st Street, Belgrade','Serbia','f56c8e3b-c613-451a-8551-3099386df914'),('95dfeb1d-2247-44d0-a701-aed4a973eb81','Name','Last name','1st Street 22 Chicago','USA','b0ae3237-7c0a-4449-b97e-c72b55b71211');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directors`
--

DROP TABLE IF EXISTS `directors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors` (
  `id` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors`
--

LOCK TABLES `directors` WRITE;
/*!40000 ALTER TABLE `directors` DISABLE KEYS */;
INSERT INTO `directors` VALUES ('011fb7f8-1b6b-4f2b-b8cd-d2fa56b6a6f7','Martin','Scorsese','USA'),('0a4d2cdb-0060-402f-a095-7b82bd6619bc','Francis','Ford Coppola','USA'),('2ef5d083-0535-4124-b8cd-e010c894665b','Stanley','Kubrick','USA'),('33354ae0-e884-4631-b4fd-79cc9dd8fd35','Pedro','Almodovar','Spain'),('3aa90cad-3789-4b1f-a1b9-5f500c5dc4bd','Chris','Carter','USA'),('56f4e74a-21e1-4808-b8df-e5c1ec8cfb51','David','Benioff','USA'),('664f1006-f10f-415f-90f4-511df135d226','Alfred','Hitchcock ','USA'),('70500b61-cb4b-45d0-bec6-fe09963057d5','Steven','Spilberg','USA'),('7c7e09bb-59a5-4e23-a441-7af4432cb8a3','James','Cameron','USA'),('8036019e-ef3d-452c-9006-8dac293242f1','Spike','Lee','USA'),('a0b98fae-94e6-4a09-9cce-7dca2b1e53e1','Gabriel','Macht','USA'),('c840a733-222a-4b87-908d-94939cd02fbe','Carry','Fukunaga','USA'),('dede2d73-4e2c-4ce6-8583-93d370ba38bb','Quentin','Tarantino','USA');
/*!40000 ALTER TABLE `directors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `episodes`
--

DROP TABLE IF EXISTS `episodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `episodes` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `series_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `series_id` (`series_id`),
  CONSTRAINT `episodes_ibfk_1` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `episodes`
--

LOCK TABLES `episodes` WRITE;
/*!40000 ALTER TABLE `episodes` DISABLE KEYS */;
INSERT INTO `episodes` VALUES ('0674b4c6-12df-4311-b9d3-d77812103f38','Episode Three','https://segr.fgg.mp4','c0a09cc1-848f-4df9-9499-12cc49098157'),('0f78f509-95bc-4920-baa1-44c187349991','Episode 2','https://segr.fgg.mp4','d75e963d-a4d1-4cb3-bdf1-5b10af895a31'),('1340815e-5442-4740-871e-00653c6f8e9f','Episode Four','https://segr.fgg.mp4','c0a09cc1-848f-4df9-9499-12cc49098157'),('2b6f0970-fed1-4a97-a8b3-2f5adb15d39b','Episode Two','https://segr.fgg.mp4','c0a09cc1-848f-4df9-9499-12cc49098157'),('3894e6b6-ebb6-4f80-bc54-beb8c98cc806','Episode Two','https://segr.fgg.mp4','9531d39c-d112-4211-8dca-7a9c31e736c0'),('44fa4ec6-fd99-4188-a93e-c8872dab337b','Episode Three','https://segr.fgg.mp4','9531d39c-d112-4211-8dca-7a9c31e736c0'),('5be609c7-f39e-4bab-87e8-c93a9afe148c','Episode 5','https://segr.fgg.mp4','fc457cdf-fe73-4c55-bbe4-4960b28fe5cd'),('6d61e50a-8a6b-4fc0-9d15-d323c8ed0b73','Episode 3','https://segr.fgg.mp4','fc457cdf-fe73-4c55-bbe4-4960b28fe5cd'),('6fe24fd4-1dbf-4f0f-8455-793c68df5162','Episode One','https://segr.fgg.mp4','c0a09cc1-848f-4df9-9499-12cc49098157'),('810d7a89-119a-4a9d-bf73-d2ebb4d3d37b','Intro','http://miller.com/north/glass.mp4','12d4b309-2421-4088-913a-1202a9bc7f54'),('82ec096d-7ad9-4c6b-978e-333c67be3e7b','Episode 4','https://segr.fgg.mp4','d75e963d-a4d1-4cb3-bdf1-5b10af895a31'),('9a882b80-c47b-49b7-a02b-e5b64df34ba5','Episode One','https://segr.fgg.mp4','9531d39c-d112-4211-8dca-7a9c31e736c0'),('9f795cd8-bd2e-4230-ab80-102fb9d86b08','Episode 1','https://segr.fgg.mp4','d75e963d-a4d1-4cb3-bdf1-5b10af895a31'),('c12ba79f-00de-455c-8562-bf9ff7555847','Episode 5','https://segr.fgg.mp4','d75e963d-a4d1-4cb3-bdf1-5b10af895a31'),('c4b73cd8-1f93-48cc-8dd9-578b80b08876','Episode 1','https://segr.fgg.mp4','fc457cdf-fe73-4c55-bbe4-4960b28fe5cd'),('e56d8118-697f-4c9c-ace9-da29d1e520d9','Episode 2','https://segr.fgg.mp4','fc457cdf-fe73-4c55-bbe4-4960b28fe5cd'),('eca4fb9a-d32f-4408-b651-b0f7aed6d8be','Episode 3','https://segr.fgg.mp4','d75e963d-a4d1-4cb3-bdf1-5b10af895a31'),('fbf1a78d-d75a-4835-b9fd-1caa3148fe0f','Episode 4','https://segr.fgg.mp4','fc457cdf-fe73-4c55-bbe4-4960b28fe5cd');
/*!40000 ALTER TABLE `episodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES ('143a6f7f-00fc-4b55-b50a-58cac3a8270e','Action'),('1955aa73-47d8-49ca-9e82-260a956b3173','Blockbuster'),('43ad84f2-0087-48ba-af57-f0bf33560ca1','Comedy'),('bccbae59-b690-4c26-8bb4-621f422bf25f','Dramma'),('7dc6458c-a00b-4867-abe7-c6a72a716ec0','Dramma-Thriller'),('ceebce78-22c5-4bc6-83e0-9a9ebf2f922a','Epic-Dramma'),('9c5f73a4-9d1d-4720-a3c7-baa11c6194fa','Horror'),('84a95ff4-8191-4e58-a438-1f0a3bfb74b4','Romance'),('e0209667-aece-4912-b341-e7f67a1920e4','Sci-Fi'),('e70e2e96-8965-4553-8fd9-e1e8e732381a','Thriller');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie_actors`
--

DROP TABLE IF EXISTS `movie_actors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movie_actors` (
  `id` varchar(50) NOT NULL,
  `movie_id` varchar(50) DEFAULT NULL,
  `actor_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `actor_id` (`actor_id`),
  CONSTRAINT `movie_actors_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`),
  CONSTRAINT `movie_actors_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `actors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie_actors`
--

LOCK TABLES `movie_actors` WRITE;
/*!40000 ALTER TABLE `movie_actors` DISABLE KEYS */;
INSERT INTO `movie_actors` VALUES ('12861441-af80-435a-bc0f-019be8df5082','beb04377-ad7b-44ae-8e33-840d57ad4548','56016e8f-6ae3-414f-bfd6-f36a31f79aca'),('21220962-ae62-4057-89a3-908633bae79f','d34dd040-219b-4519-8016-e7ef2e45fe3a','876413cd-926f-42d5-a472-9cc2a8a5cc25'),('29c797fd-6184-4726-a15e-cb74d34c0eaa','4040a6ee-95f8-4f79-afe2-c3c05638195b','e5bda776-d7aa-4332-96d4-dff8c897fd18'),('443d87d9-e7bc-4254-bd48-7350b3c7fd20','beb04377-ad7b-44ae-8e33-840d57ad4548','4d59a59e-8d88-4ccf-b9c8-33a14be815a0'),('4c8cdd5b-2e4e-48c7-a754-e43ec2a4a885','beb04377-ad7b-44ae-8e33-840d57ad4548','93e398a4-8c34-4cde-bec4-c51cf952b832'),('4e3b939e-c5e7-4341-b753-c4951f5e67ce','e619b21d-e7a9-4892-942f-0f2d14dae92a','5589c5e6-0cd8-466f-8e50-7b608686e9e8'),('62d0e4ee-7cc4-4894-824d-86248dd65b3f','6c0de0c5-e54d-484a-ad44-981bcedcdfe1','e0e63bea-23c1-46be-9ece-2d0aae20d4b1'),('6459b514-06d0-4916-8e46-3c10fa6466d9','e619b21d-e7a9-4892-942f-0f2d14dae92a','e2b420f8-fafc-498f-9aa7-897c2cad29fa'),('7ddd45f7-a567-47be-9329-85a3aab1c7bc','edd61c56-4559-4422-98af-6e5f7e7c8a15','cdc49f10-71f5-40cc-b99d-5b9b805b5e83'),('81785d05-8efb-4bd7-9312-cf2055a432ff','beb04377-ad7b-44ae-8e33-840d57ad4548','99b5058a-dcfb-4ded-802f-b441add9bfee'),('87c66768-fc74-4783-8587-d42a75fcdec1','edd61c56-4559-4422-98af-6e5f7e7c8a15','cdc49f10-71f5-40cc-b99d-5b9b805b5e83'),('b2c7cbae-4363-4aa3-b873-2fdbadcbf759','4040a6ee-95f8-4f79-afe2-c3c05638195b','da4f95f2-51d8-48c2-abc4-1b14ff1f374a'),('b9b81e28-ade7-49ba-869b-84b79b8e83b3','4040a6ee-95f8-4f79-afe2-c3c05638195b','f1f8ca6b-3809-45b1-a221-172dfdf89dd6'),('c5df64ca-3774-4f8f-9226-a436f01ca816','edd61c56-4559-4422-98af-6e5f7e7c8a15','3ba7ef2c-db21-4979-ae3b-a8b55d3e367a'),('ce78d72a-ae8a-466b-89db-5b1af7f4ce39','edd61c56-4559-4422-98af-6e5f7e7c8a15','5589c5e6-0cd8-466f-8e50-7b608686e9e8'),('fc22f3c0-5bd1-4577-a371-b864ba734851','e619b21d-e7a9-4892-942f-0f2d14dae92a','e01d8601-1bd8-461b-ab52-5410516f2778');
/*!40000 ALTER TABLE `movie_actors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movies` (
  `id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date_added` date DEFAULT NULL,
  `year_published` varchar(5) NOT NULL,
  `link` varchar(100) NOT NULL,
  `director_id` varchar(50) DEFAULT NULL,
  `genre_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `same_director_different_title` (`title`,`director_id`),
  KEY `director_id` (`director_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `movies_ibfk_1` FOREIGN KEY (`director_id`) REFERENCES `directors` (`id`),
  CONSTRAINT `movies_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES ('1226d980-2eb5-470c-8d9a-6b34cbc1434a','Psycho','2022-05-05','1952','https://segr.fggs78r.mp4','664f1006-f10f-415f-90f4-511df135d226','e0209667-aece-4912-b341-e7f67a1920e4'),('1dd54929-5e2f-40ff-ab61-166db1540cb8','Inglorious Bastards','2023-02-20','2005','http://baldwin.net/each/Mr.mp4','dede2d73-4e2c-4ce6-8583-93d370ba38bb','7dc6458c-a00b-4867-abe7-c6a72a716ec0'),('4040a6ee-95f8-4f79-afe2-c3c05638195b','Titanic','2023-02-21','1998','https://henson.com/shake/fill.mp4','7c7e09bb-59a5-4e23-a441-7af4432cb8a3','7dc6458c-a00b-4867-abe7-c6a72a716ec0'),('6c0de0c5-e54d-484a-ad44-981bcedcdfe1','Birds','2022-05-05','1962','https://segr.fggsegr.mp4','664f1006-f10f-415f-90f4-511df135d226','9c5f73a4-9d1d-4720-a3c7-baa11c6194fa'),('80d17b2c-88c5-46e8-90a3-7a5300aaf5ce','2001: A Space Odyssey','2022-05-05','1962','https://segr.fggsegr.mp4','2ef5d083-0535-4124-b8cd-e010c894665b','9c5f73a4-9d1d-4720-a3c7-baa11c6194fa'),('9ccacb25-8978-48fc-a3ae-723419021aa3','Jurrasic Park','2022-05-05','1962','https://segr.fggsegr.mp4','70500b61-cb4b-45d0-bec6-fe09963057d5','9c5f73a4-9d1d-4720-a3c7-baa11c6194fa'),('beb04377-ad7b-44ae-8e33-840d57ad4548','The Godfather','2023-02-21','1972','https://miller.com/good/through.mp4','0a4d2cdb-0060-402f-a095-7b82bd6619bc','e70e2e96-8965-4553-8fd9-e1e8e732381a'),('d34dd040-219b-4519-8016-e7ef2e45fe3a','North by Northwest','2023-02-21','1959','http://schwartz-kelley.com/bad/sign.mp4','664f1006-f10f-415f-90f4-511df135d226','9c5f73a4-9d1d-4720-a3c7-baa11c6194fa'),('e619b21d-e7a9-4892-942f-0f2d14dae92a','Pulp Fiction','2022-05-05','1992','https://segr.fgg.mp4','dede2d73-4e2c-4ce6-8583-93d370ba38bb','143a6f7f-00fc-4b55-b50a-58cac3a8270e'),('edd61c56-4559-4422-98af-6e5f7e7c8a15','Goodfellas','2023-02-21','1990','https://www.vega-cruz.com/mean/listen.mp4','011fb7f8-1b6b-4f2b-b8cd-d2fa56b6a6f7','e70e2e96-8965-4553-8fd9-e1e8e732381a');
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `series`
--

DROP TABLE IF EXISTS `series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series` (
  `id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date_added` date DEFAULT NULL,
  `year_published` varchar(5) NOT NULL,
  `director_id` varchar(50) DEFAULT NULL,
  `genre_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `same_director_different_title` (`title`,`director_id`),
  KEY `director_id` (`director_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `series_ibfk_1` FOREIGN KEY (`director_id`) REFERENCES `directors` (`id`),
  CONSTRAINT `series_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `series`
--

LOCK TABLES `series` WRITE;
/*!40000 ALTER TABLE `series` DISABLE KEYS */;
INSERT INTO `series` VALUES ('12d4b309-2421-4088-913a-1202a9bc7f54','Seinfeld','2023-02-21','1991','56f4e74a-21e1-4808-b8df-e5c1ec8cfb51','43ad84f2-0087-48ba-af57-f0bf33560ca1'),('9531d39c-d112-4211-8dca-7a9c31e736c0','True Detective','2023-02-02','2016','56f4e74a-21e1-4808-b8df-e5c1ec8cfb51','7dc6458c-a00b-4867-abe7-c6a72a716ec0'),('c0a09cc1-848f-4df9-9499-12cc49098157','Suits','2023-02-02','2016','a0b98fae-94e6-4a09-9cce-7dca2b1e53e1','bccbae59-b690-4c26-8bb4-621f422bf25f'),('d75e963d-a4d1-4cb3-bdf1-5b10af895a31','Game of Thrones','2023-02-02','2016','56f4e74a-21e1-4808-b8df-e5c1ec8cfb51','e0209667-aece-4912-b341-e7f67a1920e4'),('fc457cdf-fe73-4c55-bbe4-4960b28fe5cd','X-Files','2023-02-02','1992','3aa90cad-3789-4b1f-a1b9-5f500c5dc4bd','e0209667-aece-4912-b341-e7f67a1920e4');
/*!40000 ALTER TABLE `series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `series_actors`
--

DROP TABLE IF EXISTS `series_actors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `series_actors` (
  `id` varchar(50) NOT NULL,
  `series_id` varchar(50) DEFAULT NULL,
  `actor_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `series_id` (`series_id`),
  KEY `actor_id` (`actor_id`),
  CONSTRAINT `series_actors_ibfk_1` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`),
  CONSTRAINT `series_actors_ibfk_2` FOREIGN KEY (`actor_id`) REFERENCES `actors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `series_actors`
--

LOCK TABLES `series_actors` WRITE;
/*!40000 ALTER TABLE `series_actors` DISABLE KEYS */;
INSERT INTO `series_actors` VALUES ('2ffd1263-1cae-4270-ae5f-7d7e22a35e29','12d4b309-2421-4088-913a-1202a9bc7f54','11a96074-48db-4967-a8fe-6330dc091ef7'),('364019e4-81eb-4225-b1c6-ad5222b00efb','9531d39c-d112-4211-8dca-7a9c31e736c0','1a38cfa7-a1a5-4b48-b223-54b2844a960e'),('71c2dee2-4499-4cb6-b2b6-6c956b124628','c0a09cc1-848f-4df9-9499-12cc49098157','4d59a59e-8d88-4ccf-b9c8-33a14be815a0'),('a00a1bac-f1cd-4aec-9e2b-bac637f00738','c0a09cc1-848f-4df9-9499-12cc49098157','da4f95f2-51d8-48c2-abc4-1b14ff1f374a'),('a22d189c-3ad3-464b-9882-7d0a543393c0','12d4b309-2421-4088-913a-1202a9bc7f54','3ba7ef2c-db21-4979-ae3b-a8b55d3e367a'),('d2069d60-b935-4eea-bf9e-2a42277dcca7','9531d39c-d112-4211-8dca-7a9c31e736c0','4d59a59e-8d88-4ccf-b9c8-33a14be815a0');
/*!40000 ALTER TABLE `series_actors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subusers`
--

DROP TABLE IF EXISTS `subusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subusers` (
  `id` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `date_subscribed` date DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_subuser_name` (`user_id`,`name`),
  CONSTRAINT `subusers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subusers`
--

LOCK TABLES `subusers` WRITE;
/*!40000 ALTER TABLE `subusers` DISABLE KEYS */;
INSERT INTO `subusers` VALUES ('7f003ae2-dcf2-401a-bc93-65f1d55c5bf5','subuser 1','2023-02-14','b7baa4ca-070b-4fd7-9d77-b26cd5dd5f12'),('96487fcd-7a7d-4231-bb27-3b7d9ad05375','Sub One','2023-02-20','b7b1cd2d-754f-404d-ad88-f1a79f507a14'),('add0693f-eb3d-4814-b622-ae348ba8314f','Sub Last One','2023-02-14','0b9aba93-f056-49e6-9068-1ea658f04884'),('ce1d421d-6368-40f1-a8d9-94e4837ebb72','subuser 2','2023-02-14','b7baa4ca-070b-4fd7-9d77-b26cd5dd5f12'),('e37a5b85-e676-4704-8d58-65905b923ad9','Terminator','2023-02-14','b7b1cd2d-754f-404d-ad88-f1a79f507a14');
/*!40000 ALTER TABLE `subusers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_watch_episodes`
--

DROP TABLE IF EXISTS `user_watch_episodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_watch_episodes` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `episode_id` varchar(50) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `date_watched` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `one_user_one_rate` (`user_id`,`episode_id`),
  KEY `episode_id` (`episode_id`),
  CONSTRAINT `user_watch_episodes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_watch_episodes_ibfk_2` FOREIGN KEY (`episode_id`) REFERENCES `episodes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_watch_episodes`
--

LOCK TABLES `user_watch_episodes` WRITE;
/*!40000 ALTER TABLE `user_watch_episodes` DISABLE KEYS */;
INSERT INTO `user_watch_episodes` VALUES ('41a308aa-724e-4d28-beaa-ee610ae743be','0b9aba93-f056-49e6-9068-1ea658f04884','6fe24fd4-1dbf-4f0f-8455-793c68df5162',NULL,'2023-02-18'),('8a0bf9d2-d3e5-4ead-9c42-87b4f403f904','b7b1cd2d-754f-404d-ad88-f1a79f507a14','810d7a89-119a-4a9d-bf73-d2ebb4d3d37b',NULL,'2023-02-21'),('9888025f-175d-46a4-aa69-242e2b815370','f56c8e3b-c613-451a-8551-3099386df914','c4b73cd8-1f93-48cc-8dd9-578b80b08876',NULL,'2023-02-16'),('ae47edb8-b2c2-4611-a874-6b0eb394e60d','b7b1cd2d-754f-404d-ad88-f1a79f507a14','3894e6b6-ebb6-4f80-bc54-beb8c98cc806',7,'2023-02-21'),('bbf82ce2-ee0d-4706-b79a-c8eae61a08da','f56c8e3b-c613-451a-8551-3099386df914','e56d8118-697f-4c9c-ace9-da29d1e520d9',NULL,'2023-02-16'),('cad4b2a3-986a-4d71-bd0a-856c1e7c2e0f','b7b1cd2d-754f-404d-ad88-f1a79f507a14','9a882b80-c47b-49b7-a02b-e5b64df34ba5',7,'2023-02-21'),('ce22bf4e-cc28-478e-be8b-e91c572f6376','0b9aba93-f056-49e6-9068-1ea658f04884','c4b73cd8-1f93-48cc-8dd9-578b80b08876',NULL,'2023-02-18'),('ef4e0310-b4f2-4d0d-abea-cbf3dde4985e','b7b1cd2d-754f-404d-ad88-f1a79f507a14','44fa4ec6-fd99-4188-a93e-c8872dab337b',9,'2023-02-21'),('f2b99f9a-ae7d-45c8-b2ff-aa77fcf2c4d1','0b9aba93-f056-49e6-9068-1ea658f04884','9f795cd8-bd2e-4230-ab80-102fb9d86b08',NULL,'2023-02-18');
/*!40000 ALTER TABLE `user_watch_episodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_watch_movies`
--

DROP TABLE IF EXISTS `user_watch_movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_watch_movies` (
  `id` varchar(50) NOT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `movie_id` varchar(50) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `date_watched` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `one_user_one_rating` (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `user_watch_movies_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_watch_movies_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_watch_movies`
--

LOCK TABLES `user_watch_movies` WRITE;
/*!40000 ALTER TABLE `user_watch_movies` DISABLE KEYS */;
INSERT INTO `user_watch_movies` VALUES ('02b70bd2-0e91-4f26-aa53-261abed3a4e4','b7baa4ca-070b-4fd7-9d77-b26cd5dd5f12','1226d980-2eb5-470c-8d9a-6b34cbc1434a',6,'2023-02-20'),('09ae80b1-ddea-4a42-9349-dcea760c55e3','f56c8e3b-c613-451a-8551-3099386df914','e619b21d-e7a9-4892-942f-0f2d14dae92a',NULL,'2023-02-16'),('234a6422-213c-4e48-9654-449a7c4fb94b','f56c8e3b-c613-451a-8551-3099386df914','9ccacb25-8978-48fc-a3ae-723419021aa3',7,'2023-02-19'),('5ffcf506-4d12-49fa-afc7-4365decc1051','0b9aba93-f056-49e6-9068-1ea658f04884','6c0de0c5-e54d-484a-ad44-981bcedcdfe1',NULL,'2023-02-17'),('6cdee312-742a-443e-90fa-aaef699c0146','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','1226d980-2eb5-470c-8d9a-6b34cbc1434a',8,'2023-02-21'),('7de7dcc0-0a3e-498e-b0e3-394b3840826a','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','6c0de0c5-e54d-484a-ad44-981bcedcdfe1',8,'2023-02-21'),('9ccf9c2d-f6d1-4e7e-9594-03994555a50c','0b9aba93-f056-49e6-9068-1ea658f04884','1226d980-2eb5-470c-8d9a-6b34cbc1434a',9,'2023-02-18'),('a38f9f3e-8171-4b6c-8828-6a9c2a70fe39','f56c8e3b-c613-451a-8551-3099386df914','6c0de0c5-e54d-484a-ad44-981bcedcdfe1',8,'2023-02-19'),('b5672e1e-f65f-478a-9d96-04d292d92e36','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','edd61c56-4559-4422-98af-6e5f7e7c8a15',9,'2023-02-21'),('bb365387-ca55-404a-8fe7-0ddc4355161c','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','e619b21d-e7a9-4892-942f-0f2d14dae92a',8,'2023-02-21'),('bcb07391-3b59-4324-b8f1-bf1a2f18d64d','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','4040a6ee-95f8-4f79-afe2-c3c05638195b',8,'2023-02-21'),('c580d336-31b2-4577-8c8e-2e7462fefe4f','cb61eb90-8426-4631-a564-42d163147531','9ccacb25-8978-48fc-a3ae-723419021aa3',6,'2023-02-20'),('c5c14581-18da-40b7-b798-3c3453365ad2','87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','beb04377-ad7b-44ae-8e33-840d57ad4548',9,'2023-02-21'),('ceeaa385-cbce-4e85-977c-7045c6dc0b06','f56c8e3b-c613-451a-8551-3099386df914','1226d980-2eb5-470c-8d9a-6b34cbc1434a',10,'2023-02-19'),('da9cacb8-4a5c-4d27-adda-7dc4aabcf310','0b9aba93-f056-49e6-9068-1ea658f04884','e619b21d-e7a9-4892-942f-0f2d14dae92a',NULL,'2023-02-17'),('e94697a2-f78d-4ce2-8f20-2cd144f2d14a','b7b1cd2d-754f-404d-ad88-f1a79f507a14','1226d980-2eb5-470c-8d9a-6b34cbc1434a',10,'2023-02-18');
/*!40000 ALTER TABLE `user_watch_movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password_hashed` varchar(100) DEFAULT NULL,
  `username` varchar(100) DEFAULT NULL,
  `date_subscribed` date DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT NULL,
  `verification_code` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('0b9aba93-f056-49e6-9068-1ea658f04884','branko.teamcubate@gmail.com','fb33c1942df4cdd4fd078179fcb8e52ec3351fa94232505a702ad1bc92a5febb','branko','2023-02-14',1,0,NULL),('87de1978-b1ad-4568-9c5a-3a7e3d8a3ebd','dumbo@gmail.com','5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8','dumbo','2023-02-21',1,0,NULL),('b0ae3237-7c0a-4449-b97e-c72b55b71211','superuser@netflix.com','a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3','branko','2023-02-14',1,1,NULL),('b7b1cd2d-754f-404d-ad88-f1a79f507a14','brolujay@gmail.com','fb33c1942df4cdd4fd078179fcb8e52ec3351fa94232505a702ad1bc92a5febb','brolujay','2023-02-14',1,0,NULL),('b7baa4ca-070b-4fd7-9d77-b26cd5dd5f12','dummy3@netflix.com','fb33c1942df4cdd4fd078179fcb8e52ec3351fa94232505a702ad1bc92a5febb','dummy3','2023-02-14',0,0,NULL),('cb61eb90-8426-4631-a564-42d163147531','dummy2@netflix.com','fb33c1942df4cdd4fd078179fcb8e52ec3351fa94232505a702ad1bc92a5febb','dummy2','2023-02-14',1,0,NULL),('f56c8e3b-c613-451a-8551-3099386df914','olujic.branko@gmail.com','fb33c1942df4cdd4fd078179fcb8e52ec3351fa94232505a702ad1bc92a5febb','brankovic','2023-02-14',1,1,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-22 17:11:24
