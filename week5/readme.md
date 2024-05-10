# Week 5 Task 1
安裝MySQL

# Week 5 Task 2

## Task 2-1  Create a new database named website.
```SQL
CREATE DATABASE `website`;
```
![2-1](pic/2-1.png)

## Task 2-2 Create a new table named member, in the website database, designed as below
```SQL
USE `website`;
# Database changed
CREATE TABLE `member`(
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `follower_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
```
![2-2](pic/2-2.png)

# Week 5 Task 3

## Task 3-1 INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.

```SQL
INSERT INTO `member`(`name`, `username`, `password`) VALUES ('test','test','test');
```
![3-1](pic/3-1.png)

```SQL
INSERT INTO `member`(`name`, `username`, `password`) VALUES ('江戶川柯南','柯南','4869'),
    ('毛利蘭','小蘭','05'),
    ('Gin','黑衣人','7'),
    ('目暮十三','警官','13');
```
![3-1-2](pic/3-1-2.png)

## Task 3-2 SELECT all rows from the member table.
```SQL
SELECT * FROM `member`;
```
![3-2](pic/3-2.png)

## Task 3-3 SELECT all rows from the member table, in descending order of time.
```SQL
SELECT * FROM `member` ORDER BY `time` DESC;
```
![3-3](pic/3-3.png)

## Task 3-4 SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.
```SQL
SELECT * FROM `member` ORDER BY `time` DESC LIMIT 3 OFFSET 1;
```
![3-4](pic/3-4.png)

## Task 3-5 SELECT rows where username equals to test.
```SQL
SELECT * FROM `member` WHERE `username` = 'test';
```
![3-5](pic/3-5.png)

## Task 3-6 SELECT rows where name includes the es keyword.
```SQL
SELECT * FROM `member` WHERE `name` LIKE '%es%';
```
![3-6](pic/3-6.png)

## Task 3-7 SELECT rows where both username and password equal to test.
```SQL
SELECT * FROM `member` WHERE `username` = 'test' AND `password` = 'test';
```
![3-7](pic/3-7.png)

## Task 3-8  UPDATE data in name column to test2 where username equals to test.
```SQL
UPDATE `member` SET `name` = 'test2' WHERE username = 'test';
```
![3-8](pic/3-8.png)

# Week 5 Task 4

## Task 4-1 SELECT how many rows from the member table.
```SQL
SELECT COUNT(*) FROM `member`;
```
![4-1](pic/4-1.png)

## Task 4-2 SELECT the sum of follower_count of all the rows from the member table.
```SQL
SELECT SUM(`follower_count`) FROM `member`;
```
![4-2](pic/4-2.png)

## Task 4-3 SELECT the average of follower_count of all the rows from the member table.
```SQL
SELECT AVG(`follower_count`) FROM `member`;
```
![4-3](pic/4-3.png)

## Task 4-4 SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
```SQL
SELECT AVG(`follower_count`)
    FROM (
    SELECT `follower_count` FROM `member` ORDER BY `follower_count` DESC LIMIT 2
    ) AS top_two;
```
![4-4](pic/4-4.png)

# Week 5 Task 5

## Task 5-1 Create a new table named message, in the website database. designed as below
```SQL
CREATE TABLE `message`(
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `member_id` BIGINT NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `like_count` INT UNSIGNED NOT NULL DEFAULT 0,
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`member_id`) REFERENCES `member`(`id`)
);
```
![5-1](pic/5-1.png)
![5-1-2](pic/5-1-2.png)

```SQL
INSERT INTO `message` (`member_id`,`content`,`like_count`) VALUES
    (2,'東京死神',10077),
    (1,'彭彭就是讚',30004),
    (1,'看彭彭寫code好療癒',1588),
    (4,'整個組織只有你認真工作',5555),
    (3,'人間兵器',4432),
    (2,'阿勒勒',752);
```

![5-1-3](pic/5-1-3.png)

## Task 5-2 SELECT all messages, including sender names. We have to JOIN the member table to get that.
```SQL
SELECT * FROM `message` JOIN `member` ON `message`.`member_id` = `member`.`id`;
```
![5-2](pic/5-2.png)

## Task 5-3 SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
```SQL
SELECT * FROM `message` JOIN `member` ON `message`.`member_id` = `member`.`id`
    -WHERE `member`.`username`='test';
```
![5-3](pic/5-3.png)

## Task 5-4 Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
```SQL
SELECT AVG(`like_count`)
FROM (
	SELECT `message`.`like_count`
	FROM `message` 
	JOIN `member` ON `message`.`member_id` = `member`.`id`
	WHERE `member`.`username`='test'
) AS combine ;
```
![5-4](pic/5-4.png)

## Task 5-5 Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
```SQL
SELECT 
    `member`.`username`, 
    AVG(`message`.`like_count`) AS `average_like_count`
FROM 
    `message`
RIGHT JOIN
    `member` ON `message`.`member_id` = `member`.`id`
GROUP BY 
    `member`.`username`;
```
![5-5](pic/5-5.png)


