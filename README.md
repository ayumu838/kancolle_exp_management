# 艦これ経験値管理

# 環境
- python3

- 使用DB
    - sqlite

#  DBテーブル

# GET_EXP
|name|type|
|:-:|:-:|
|date|DATE|
|exp|INTEGER|

# MONTHLY_EXP
|name|type|
|:-:|:-:|
|month|DATE|
|exp|INTGER|


# connect database

```bash

$ sqlite3 "DB NAME"

```