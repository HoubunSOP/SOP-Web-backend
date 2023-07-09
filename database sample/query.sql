-------------------
-- 获取漫画分类和标签
-------------------
SELECT c.name AS comic_name,
  ca.name AS category_name,
  t.name AS tag_name
FROM comics c
  LEFT JOIN comic_category_map cc ON c.id = cc.comic_id
  LEFT JOIN categories ca ON cc.category_id = ca.id
  LEFT JOIN comic_tag_map ct ON c.id = ct.comic_id
  LEFT JOIN tags t ON ct.tag_id = t.id
WHERE c.id = 漫画ID;
-------------------
-- 获取文章分类和标签
-------------------
SELECT a.title AS article_title,
  ca.name AS category_name,
  t.name AS tag_name
FROM articles a
  LEFT JOIN article_category_map ac ON a.id = ac.article_id
  LEFT JOIN categories ca ON ac.category_id = ca.id
  LEFT JOIN article_tag_map at ON a.id = at.article_id
  LEFT JOIN tags t ON at.tag_id = t.id
WHERE a.id = 文章ID;
--------------
-- 添加漫画信息
--------------