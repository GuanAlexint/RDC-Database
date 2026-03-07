-- RDC Database Schema
-- 仅包含表结构，不含数据
-- 导入方式：mysql -u root -p rdcdb < schema.sql

CREATE DATABASE IF NOT EXISTS `rdcdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `rdcdb`;

-- 化合物基础信息
CREATE TABLE `compound_info` (
  `compound_id`      INT           NOT NULL AUTO_INCREMENT,
  `name`             VARCHAR(255)  DEFAULT NULL COMMENT '化合物名称',
  `cas_number`       VARCHAR(255)  DEFAULT NULL COMMENT 'CAS号',
  `molecular_weight` FLOAT         DEFAULT NULL COMMENT '分子量',
  `molecular_formula`VARCHAR(255)  DEFAULT NULL COMMENT '分子式',
  `logP`             VARCHAR(255)  DEFAULT NULL COMMENT '脂水分配系数',
  `smiles`           TEXT          COMMENT 'SMILES结构式',
  `inchi`            TEXT          COMMENT 'InChI标识符',
  PRIMARY KEY (`compound_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 靶点与探针信息
CREATE TABLE `target_info` (
  `target_id`   INT          NOT NULL AUTO_INCREMENT,
  `compound_id` INT          DEFAULT NULL COMMENT '关联化合物ID',
  `target`      VARCHAR(255) DEFAULT NULL COMMENT '靶点名称',
  `isotope`     VARCHAR(255) DEFAULT NULL COMMENT '同位素',
  `probe_type`  VARCHAR(255) DEFAULT NULL COMMENT '探针类型',
  `ki`          VARCHAR(255) DEFAULT NULL COMMENT 'Ki值',
  `kd`          VARCHAR(255) DEFAULT NULL COMMENT 'Kd值',
  `ic50`        VARCHAR(255) DEFAULT NULL COMMENT 'IC50值',
  PRIMARY KEY (`target_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- PET/SPECT成像数据
CREATE TABLE `imaging_data` (
  `imaging_id`  INT          NOT NULL AUTO_INCREMENT,
  `compound_id` INT          DEFAULT NULL COMMENT '关联化合物ID',
  `suv_max`     VARCHAR(255) DEFAULT NULL COMMENT 'SUVmax值',
  `suv_mean`    VARCHAR(255) DEFAULT NULL COMMENT 'SUVmean值',
  PRIMARY KEY (`imaging_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 生物分布数据（各器官摄取值 %ID/g）
CREATE TABLE `biodistribution` (
  `bio_id`          INT  NOT NULL AUTO_INCREMENT,
  `compound_id`     INT  DEFAULT NULL COMMENT '关联化合物ID',
  `tumor_uptake`    TEXT COMMENT '肿瘤摄取',
  `kidney_uptake`   TEXT COMMENT '肾摄取',
  `liver_uptake`    TEXT COMMENT '肝摄取',
  `spleen_uptake`   TEXT COMMENT '脾摄取',
  `lung_uptake`     TEXT COMMENT '肺摄取',
  `heart_uptake`    TEXT COMMENT '心脏摄取',
  `muscle_uptake`   TEXT COMMENT '肌肉摄取',
  `bone_uptake`     TEXT COMMENT '骨摄取',
  `blood_uptake`    TEXT COMMENT '血液摄取',
  `brain_uptake`    TEXT COMMENT '脑摄取',
  `stomach_uptake`  TEXT COMMENT '胃摄取',
  `prostate_uptake` TEXT COMMENT '前列腺摄取',
  PRIMARY KEY (`bio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 肿瘤对比度比率
CREATE TABLE `ratios` (
  `ratio_id`           INT          NOT NULL AUTO_INCREMENT,
  `compound_id`        INT          DEFAULT NULL COMMENT '关联化合物ID',
  `tumor_bone_ratio`   TEXT         COMMENT '肿瘤/骨比率',
  `tumor_muscle_ratio` VARCHAR(255) DEFAULT NULL COMMENT '肿瘤/肌肉比率',
  `tumor_blood_ratio`  TEXT         COMMENT '肿瘤/血液比率',
  `tumor_kidney_ratio` VARCHAR(255) DEFAULT NULL COMMENT '肿瘤/肾比率',
  PRIMARY KEY (`ratio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 药代动力学数据
CREATE TABLE `pharmacokinetics` (
  `pk_id`               INT          NOT NULL AUTO_INCREMENT,
  `compound_id`         INT          DEFAULT NULL COMMENT '关联化合物ID',
  `blood_half_life`     VARCHAR(255) DEFAULT NULL COMMENT '血液半衰期',
  `urine_half_life`     VARCHAR(255) DEFAULT NULL COMMENT '尿液半衰期',
  `blood_clearance_rate`VARCHAR(255) DEFAULT NULL COMMENT '血液清除率',
  `auc`                 VARCHAR(255) DEFAULT NULL COMMENT '药时曲线下面积',
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 参考文献
CREATE TABLE `reference_info` (
  `ref_id`          INT  NOT NULL AUTO_INCREMENT,
  `compound_id`     INT  DEFAULT NULL COMMENT '关联化合物ID',
  `reference_title` TEXT COMMENT '文献标题',
  `reference_link`  TEXT COMMENT '文献DOI或链接',
  PRIMARY KEY (`ref_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
