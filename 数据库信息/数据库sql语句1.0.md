# 数据库设计

## 1.活动（主要是指博物馆与外界联合举办的活动）

```
CREATE TABLE `activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `museumID` int NOT NULL,
  `time` datetime NOT NULL,
  `introduction` varchar(10000) NOT NULL,
  `photo` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 2.藏品信息

```
CREATE TABLE `collection` (
  `id` int NOT NULL AUTO_INCREMENT,
  `museumID` int NOT NULL,
  `type` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `introduction` varchar(10000) NOT NULL,
  `photo` json DEFAULT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 3.展览信息

```
CREATE TABLE `exhibition` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `time` datetime NOT NULL,
  `introduction` varchar(10000) NOT NULL,
  `photo` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 4.讲解信息

```
CREATE TABLE `explain` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `userID` int NOT NULL,
  `introduction` varchar(10000) NOT NULL,
  `audio` json DEFAULT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 5.新闻信息

```
CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `museumID` int NOT NULL,
  `time` datetime NOT NULL,
  `type` varchar(45) NOT NULL,
  `content` varchar(10000) NOT NULL,
  `photo` json DEFAULT NULL,
  `source` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 6.博物馆信息

```
CREATE TABLE `overview` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `introduction` varchar(10000) NOT NULL,
  `photo` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 7.评论信息

```
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `museumID` int NOT NULL,
  `score0` int NOT NULL,
  `score1` int NOT NULL,
  `score2` int NOT NULL,
  `discuss` varchar(10000) NOT NULL,
  `time` datetime NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 8.用户信息

```
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `status` int NOT NULL,
  `regtime` datetime NOT NULL,
  `root` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `phone_UNIQUE` (`phone`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

