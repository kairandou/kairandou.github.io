# 主页内容维护

> 适用：Kairan Dou 个人主页 · 更新：2026-11-04

页面导航固定为 **About、Education、Papers** 三个部分。日常更新只改 `_data/` 中的内容文件，不需要编辑 HTML 或 CSS。教育经历和可选的科研／工作经历自动按开始日期倒序排列；论文按文件中的顺序展示，新增论文通常放在最前面。

| 要修改的内容 | 文件 |
| --- | --- |
| 姓名、照片、简介、研究方向、联系方式 | `_data/profile.yml` |
| 教育经历 | `_data/education.yml` |
| 论文、作者、配图、链接 | `_data/publications.yml` |
| 科研与工作经历，默认不显示 | `_data/experience.yml` |

## 修改 About

`bio` 中每个 `- >-` 是一个自然段，支持 Markdown 链接和 `**加粗**`。`research_interests` 是研究方向列表；联系方式在 `links` 中填写。头像放入 `images/`，然后修改 `portrait`。

现有简介根据旧站内容改写，未添加新的雇主或学位。邮箱仍沿用旧站的 Berkeley 邮箱；发布更新时请按实际情况修改。About 使用研究经历回顾的表达，不把旧站的 “present” 自动视为当前任职。

## 添加教育经历

在 `_data/education.yml` 中复制一项并填写：

```yaml
- institution: "学校名称"
  degree: "学位 / 项目名称"
  start: "2026-09"
  end: "2028-06"
  logo: "/images/school.png"
  url: "https://example.edu"
```

日期使用带引号的 `YYYY-MM`。正在进行的经历可写 `end: null`；没有 logo 或学校链接时可留空、填写空字符串 `""` 或省略字段。教育经历自动按 `start` 倒序排列，无需手动调整先后。

## 添加论文

在 `_data/publications.yml` 顶部复制以下条目：

```yaml
- id: "short-unique-paper-name"
  title: "论文标题"
  authors: 'First Author\*, **Kairan Dou**, Other Author'
  venue: "Conference / Journal / arXiv"
  year: 2026
  image: "/images/paper.png"
  image_alt: "图片内容的简短描述"
  summary: "可选的一句话介绍。"
  links:
    - label: "Paper"
      url: "https://example.com/paper"
    - label: "Code"
      url: "https://github.com/owner/repository"
```

`id` 必须唯一，用小写英文、数字和连字符。作者字段支持 Markdown；用 `**Kairan Dou**` 突出本人，等贡献星号写成 `\*`，此时使用示例中的单引号或 `>-` 长文本写法，避免 YAML 双引号的转义规则。论文介绍 `summary` 可留空或省略，链接可按需要添加 Project、Code、PDF 等。

配图放在 `images/`，使用 `/images/paper.png` 这样的根相对路径。图片按原始比例完整显示，点击可放大；无需预先裁成固定尺寸。没有配图时将 `image` 和 `image_alt` 留空即可。

## 添加科研或工作经历

经历数据单独保存在 `_data/experience.yml`，`enabled: false` 时不显示。需要展示时，先核对所有条目的日期，再改为 `enabled: true`，经历会作为 **Research experience** 子部分出现在 About 内，并自动按 `start` 倒序排列。不会新增顶层部分或导航，页面仍然是 About、Education、Papers。在 `items:` 下复制条目，保持缩进：

```yaml
enabled: false
items:
  - organization: "机构名称"
    role: "职位 / 身份"
    start: "2026-07"
    end: null
    summary: "工作内容或研究方向，支持 Markdown。"
    links:
      - label: "Project"
        url: "https://example.com"
```

`end: null` 表示页面显示 Present。迁移来的 MIT/Harvard、UT Austin 条目在旧站中没有结束日期，当前保留为 `null`，**这不代表已确认仍在任**；启用前请补充或确认。简介可留空或省略，链接不需要时可写 `links: []` 或省略字段。

## 保存与发布

使用两个空格缩进，不要使用 Tab。标题含冒号时加引号；长段落用 `>-`，后续文字保持缩进。保存后在本地预览，确认内容、图片和链接，再提交并推送到 GitHub，由 GitHub Pages 更新线上网站。网页本身不会直接写入仓库。

## 动效与阅读偏好

页面底部的 **Motion on / off** 可以开关动效，选择保存在当前浏览器中。系统启用“减少动态效果”时，页面优先遵循系统设置，显示 Motion reduced。轨道在头像离开视野或页面切到后台后暂停；正文不依赖 JavaScript 显示。图片仍保持完整比例，动效不改变填写内容的方式。

后续内容规划见 [TODO](TODO.md)。当前改版前的基础版本可通过本地标签 `homepage-v1-20261104` 查看。
