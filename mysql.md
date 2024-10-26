# 这是一份用于说明本项目MySQL搭建以及结构的文档

## MySQL 表创建指令

### 用户数据表

```sql
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `sex` enum('M', 'F', 'Other') NOT NULL,
  `passwd` char(128) NOT NULL,
  `QQ` varchar(10) DEFAULT NULL,
  `status` tinyint DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 用户战绩表

```sql
CREATE TABLE `game_attempts` (
  `attempt_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `game_name` varchar(50) NOT NULL,
  `score` int DEFAULT '0',
  `attempts` int NOT NULL,
  `result` enum('win','lose') NOT NULL,
  `played_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`attempt_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `game_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

### 排行榜相关统计表

```sql
CREATE TABLE `game_stats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `game_name` varchar(50) NOT NULL,
  `total_score` int DEFAULT '0',
  `games_played` int DEFAULT '0',
  `average_score` decimal(5,2) DEFAULT '0.00',
  `wins` int DEFAULT '0',
  `losses` int DEFAULT '0',
  `play_count` int DEFAULT '0',
  `min_attempts` int DEFAULT NULL,
  `max_attempts` int DEFAULT NULL,
  `last_played` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `game_stats_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

## MySQL 数据结构

### 数据库表概述

本项目使用三个主要的 MySQL 数据表来存储用户数据和游戏相关信息：

1. **users** - 存储用户的基本信息。
2. **game_attempts** - 记录用户每次游戏的尝试情况。
3. **game_stats** - 存储用户游戏统计数据，以用于排名和个人记录分析。

### 表结构详解

#### 1. 用户数据表（`users`）

**用途**：存储用户的基本信息，如用户名、邮箱、性别、密码、QQ、状态以及创建时间、最后登录时间等。

| 表名           | 字段名         | 数据类型                   | 说明                       |
|----------------|----------------|----------------------------|----------------------------|
| **users**      | id             | int, AUTO_INCREMENT        | 主键                       |
|                | name           | char(50)                   | 用户名，唯一约束            |
|                | email          | varchar(100)               | 邮箱，唯一约束              |
|                | sex            | enum('M', 'F', 'Other')    | 性别字段                   |
|                | passwd         | char(128)                  | 加密密码                    |
|                | QQ             | varchar(10)                | QQ号码，允许为空            |
|                | status         | tinyint                    | 状态字段，默认值为 1        |
|                | created_at     | timestamp                  | 创建时间                    |
|                | updated_at     | timestamp                  | 更新时间                    |
|                | last_login     | datetime                   | 最后登录时间                |

#### 2. 用户战绩表（`game_attempts`）

**用途**：记录用户每次游戏的尝试情况，包括游戏名称、分数、尝试次数、结果（胜利或失败）等。

| 表名               | 字段名         | 数据类型              | 说明                       |
|--------------------|----------------|-----------------------|----------------------------|
| **game_attempts**  | attempt_id     | int, AUTO_INCREMENT  | 主键                       |
|                    | user_id        | int                  | 外键，关联 `users.id`       |
|                    | game_name      | varchar(50)          | 游戏名称                    |
|                    | score          | int                  | 分数                        |
|                    | attempts       | int                  | 尝试次数                    |
|                    | result         | enum('win', 'lose')  | 游戏结果                    |
|                    | played_at      | timestamp            | 尝试时间                    |

#### 3. 排行榜相关统计表（`game_stats`）

**用途**：记录用户在特定游戏中的总成绩、胜场、负场、最小/最大尝试次数、平均分等统计信息，用于生成排行榜和分析用户表现。

| 表名               | 字段名         | 数据类型              | 说明                       |
|--------------------|----------------|-----------------------|----------------------------|
| **game_stats**     | id             | int, AUTO_INCREMENT  | 主键                       |
|                    | user_id        | int                  | 外键，关联 `users.id`       |
|                    | game_name      | varchar(50)          | 游戏名称                    |
|                    | total_score    | int                  | 总得分                      |
|                    | games_played   | int                  | 已完成游戏次数              |
|                    | average_score  | decimal(5,2)         | 平均得分                    |
|                    | wins           | int                  | 胜场数                      |
|                    | losses         | int                  | 败场数                      |
|                    | play_count     | int                  | 游戏参与次数                |
|                    | min_attempts   | int                  | 最少尝试次数                |
|                    | max_attempts   | int                  | 最多尝试次数                |
|                    | last_played    | timestamp            | 最后一次参与时间            |
|                    | created_at     | timestamp            | 创建时间                    |
|                    | updated_at     | timestamp            | 最后更新时间                |

### 数据表关系

- **用户表与游戏表的关联**：`game_attempts` 表和 `game_stats` 表中的 `user_id` 字段与 `users` 表的 `id` 字段通过外键关联。
- **多对一关系**：每个用户在 `users` 表中有一条记录，但可以有多条 `game_attempts` 和 `game_stats` 记录，用于不同的游戏或尝试。

#### ER图

![ER图](https://pic.cloud.rpcrpc.com/data/671d19b915d31.png)
