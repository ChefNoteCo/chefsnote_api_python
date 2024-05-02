DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS ingredient;



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
  parent_id INTEGER NOT NULL,
  child_id INTEGER NOT NULL,
  recipe_name TEXT NOT NULL DEFAULT 'UNNAMED',
  prepTime INTEGER NOT NULL DEFAULT 0,
  cookTime INTEGER NOT NULL DEFAULT 0,
  servings INTEGER NOT NULL DEFAULT 0,
  feedback_notes TEXT,
  prep_notes TEXT,
  instruction TEXT
);

CREATE TABLE recipe_ingredients (
  id TEXT PRIMARY KEY,
  external_id INTEGER,
  user_id TEXT,
  ingredient_id TEXT,
  measurement INTEGER DEFAULT 0
);

CREATE TABLE ingredient (
  id TEXT PRIMARY KEY,
  userID INTEGER,
  ingredient_name TEXT NOT NULL,
  unit TEXT DEFAULT 'g',
  quantity INTEGER NOT NULL DEFAULT 0
);
