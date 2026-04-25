# music_platform 数据库结构

## users 用户表
- id：主键
- username：用户名
- password_hash：密码哈希
- created_at：创建时间

## songs 歌曲表
- id：主键
- title：歌曲名
- singer_id：歌手ID
- duration：时长（秒）
...