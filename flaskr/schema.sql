DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS ingredient;


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
  instruction TEXT,
  recipe_id TEXT,
  FOREIGN KEY (recipe_id) REFERENCES recipe_ingredients(id)
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
