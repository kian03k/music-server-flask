-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS music_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE music_platform;

-- 用户表（对应你代码里的 users 表）
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    name VARCHAR(50) NOT NULL COMMENT '用户名',
    password VARCHAR(100) NOT NULL COMMENT '密码',
    age INT NULL COMMENT '年龄',
    addr VARCHAR(255) NULL COMMENT '地址',
    birth VARCHAR(50) NULL COMMENT '生日',
    sex VARCHAR(10) NULL COMMENT '性别',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

USE music_platform;

-- 给用户表加 role 字段（admin / user）
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' COMMENT '角色：admin/user';