DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS recipes;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE recipes (
  id TEXT PRIMARY KEY,
  version INTEGER NOT NULL,
  latest TEXT NOT NULL DEFAULT 'TRUE',
  name TEXT NOT NULL DEFAULT 'UNNAMED',
  prepTime INTEGER NOT NULL DEFAULT 0,
  cookTime INTEGER NOT NULL DEFAULT 0,
  servings INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ingredient (
  id TEXT PRIMARY KEY
  userID INTEGER,
  name TEXT NOT NULL,
  unit TEXT DEFAULT 'g',
  quantity INTEGER NOT NULL DEFAULT 0
)
