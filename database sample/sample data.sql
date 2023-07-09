INSERT INTO categories (name, category)
VALUES ('分类1', '漫画'),
  ('分类2', '漫画'),
  ('分类3', '文章'),
  ('分类4', '文章');
INSERT INTO tags (name, tag)
VALUES ('标签1', '漫画'),
  ('标签2', '漫画'),
  ('标签3', '文章'),
  ('标签4', '文章');
INSERT INTO comics (name, date, intro, cover, magazine)
VALUES (
    '漫画1',
    '2021-01-01',
    '这是漫画1的简介，支持Markdown语法。',
    'comic1_cover.jpg',
    '刊物1'
  ),
  (
    '漫画2',
    '2021-02-01',
    '这是漫画2的简介，支持Markdown语法。',
    'comic2_cover.jpg',
    '刊物2'
  ),
  (
    '漫画3',
    '2021-03-01',
    '这是漫画3的简介，支持Markdown语法。',
    'comic3_cover.jpg',
    '刊物1'
  );
INSERT INTO articles (title, date, content)
VALUES ('文章1', '2021-01-01', '这是文章1的内容，支持Markdown语法。'),
  ('文章2', '2021-02-01', '这是文章2的内容，支持Markdown语法。'),
  ('文章3', '2021-03-01', '这是文章3的内容，支持Markdown语法。');
INSERT INTO comic_category_map (comic_id, category_id)
VALUES (1, 1),
  (1, 2),
  (2, 1),
  (2, 2),
  (3, 1);
INSERT INTO comic_tag_map (comic_id, tag_id)
VALUES (1, 1),
  (1, 2),
  (2, 1),
  (2, 2),
  (3, 1),
  (3, 2);
INSERT INTO article_category_map (article_id, category_id)
VALUES (1, 3),
  (1, 4),
  (2, 3),
  (2, 4),
  (3, 3);
INSERT INTO article_tag_map (article_id, tag_id)
VALUES (1, 3),
  (1, 4),
  (2, 3),
  (2, 4),
  (3, 3),
  (3, 4);