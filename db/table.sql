CREATE DATABASE admin;

CREATE TABLE `admin`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `password` VARCHAR(100) NULL,
  `createAt` DATETIME NULL,
  `updateAt` DATETIME NULL,
  `status` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_status` (`status` ASC) VISIBLE);

ALTER TABLE `admin`.`user` 
CHANGE COLUMN `updateAt` `lastLoginAt` DATETIME NULL DEFAULT NULL AFTER `password`;
