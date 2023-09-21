-- 创建表
CREATE TABLE comics
(
    id       INT          NOT NULL AUTO_INCREMENT COMMENT '漫画唯一标识',
    name     VARCHAR(255) NOT NULL COMMENT '漫画名称',
    author   VARCHAR(255) NOT NULL DEFAULT '未知' COMMENT '作者名称',
    date     DATE         NOT NULL COMMENT '漫画发布日期',
    intro    TEXT COMMENT '漫画简介，支持Markdown语法',
    cover    VARCHAR(255) NOT NULL COMMENT '封面图片文件名',
    magazine VARCHAR(255) COMMENT '所属刊物。例如："刊物1"',
    auto     BOOLEAN      NOT NULL DEFAULT FALSE COMMENT '是否为自动生成',
    PRIMARY KEY (id)
);
CREATE TABLE categories
(
    id       INT          NOT NULL AUTO_INCREMENT COMMENT '分类唯一标识',
    name     VARCHAR(255) NOT NULL COMMENT '分类名称',
    category VARCHAR(255) NOT NULL COMMENT '漫画/文章分类',
    PRIMARY KEY (id)
);
CREATE TABLE tags
(
    id   INT          NOT NULL AUTO_INCREMENT COMMENT '标签唯一标识',
    name VARCHAR(255) NOT NULL COMMENT '标签名称',
    tag  VARCHAR(255) NOT NULL COMMENT '漫画/文章标签',
    PRIMARY KEY (id)
);
CREATE TABLE comic_category_map
(
    comic_id    INT NOT NULL COMMENT '漫画唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (comic_id, category_id),
    FOREIGN KEY (comic_id) REFERENCES comics (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
CREATE TABLE comic_tag_map
(
    comic_id INT NOT NULL COMMENT '漫画唯一标识',
    tag_id   INT NOT NULL COMMENT '标签唯一标识',
    PRIMARY KEY (comic_id, tag_id),
    FOREIGN KEY (comic_id) REFERENCES comics (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);
CREATE TABLE articles
(
    id          INT          NOT NULL AUTO_INCREMENT COMMENT '文章唯一标识',
    title       VARCHAR(255) NOT NULL COMMENT '文章标题',
    date        DATE         NOT NULL COMMENT '文章发布日期',
    content     TEXT COMMENT '文章内容，支持Markdown语法',
    cover       varchar(255)      DEFAULT NULL COMMENT '文章封面',
    comic       varchar(255)      DEFAULT NULL COMMENT '关联漫画',
    recommended BOOLEAN      NULL DEFAULT FALSE COMMENT '是否为推荐文章',
    PRIMARY KEY (id)
);
CREATE TABLE article_category_map
(
    article_id  INT NOT NULL COMMENT '文章唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
CREATE TABLE article_tag_map
(
    article_id INT NOT NULL COMMENT '文章唯一标识',
    tag_id     INT NOT NULL COMMENT '标签唯一标识',
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);
CREATE TABLE settings
(
    topswiper VARCHAR(255) NOT NULL COMMENT 'topswiper的文章id'
);
-- 添加漫画分类
INSERT INTO categories (name, category)
VALUES ('Kirara', '漫画'),
       ('MAX', '漫画'),
       ('Carat', '漫画'),
       ('Forward', '漫画'),
       ('未分类','文章')