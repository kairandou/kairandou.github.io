# 主页内容维护

> 适用：Kairan Dou 个人主页 · 更新：2026-11-05

页面分为 **About、Education、Internships、Papers**。日常更新只改 `_data/` 中的内容文件，不需要编辑 HTML 或 CSS。教育与实习按开始日期倒序排列；论文按文件中的顺序展示，新增论文通常放在最前面。教育只展示学校、学习阶段和时间；实习只展示公司、岗位和时间，不展示项目职责或研究经历。

| 要修改的内容 | 文件 |
| --- | --- |
| 姓名、照片、简介、研究方向、联系方式 | `_data/profile.yml` |
| 教育经历 | `_data/education.yml` |
| 论文、作者、配图、链接 | `_data/publications.yml` |
| 公司、实习岗位、时间和标志 | `_data/internships.yml` |

## 修改 About

`bio` 中每个 `- >-` 是一个自然段，支持 Markdown 链接和 `**加粗**`。`research_interests` 是研究方向列表；联系方式在 `links` 中填写。头像放入 `images/`，然后修改 `portrait`，并填写照片实际像素宽高 `portrait_width` 和 `portrait_height`。原图和 AI 清晰化版本均已保留，切换方法见[视觉素材说明](visual-assets.md)。

现有简介、教育、实习和邮箱根据 2026 年 11 月提供的简历更新；邮箱为 CMU 邮箱。CMU 项目于 2027 年 1 月开始，因此当前写为即将入学，不写为已在读。入学后请同步更新简介和教育条目的 `status`。旧 `_data/experience.yml` 仅留作历史数据，当前模板不读取它。

## 添加教育经历

在 `_data/education.yml` 中复制一项并填写：

```yaml
- institution: "学校名称"
  degree: "Graduate student"
  status: "Incoming"
  start: "2026-09"
  end: "2028-06"
  end_label: "Expected"
  logo: "/images/school.png"
  url: "https://example.edu"
```

`degree` 只写 `Undergraduate`、`Exchange student` 或 `Graduate student`，不写专业。日期使用带引号的 `YYYY-MM`。尚未入学时填写 `status: "Incoming"`；入学后将它留空或删去。预计毕业日期可加 `end_label: "Expected"`；已完成的经历不用这两个字段。结束日期未知时可写 `end: null`；没有 logo 或学校链接时可留空、填写空字符串 `""` 或省略字段。教育经历自动按 `start` 倒序排列，无需手动调整先后。

## 添加论文

在 `_data/publications.yml` 顶部复制以下条目：

```yaml
- id: "short-unique-paper-name"
  title: "论文标题"
  authors: 'First Author\*, **Kairan Dou**, Other Author'
  venue: "Conference / Journal / arXiv"
  year: 2026
  scholar_id: ""
  citations: null
  citations_updated: ""
  image: "/images/paper.png"
  image_alt: "图片内容的简短描述"
  links:
    - label: "Paper"
      url: "https://example.com/paper"
    - label: "Code"
      url: "https://github.com/owner/repository"
```

`id` 必须唯一，用小写英文、数字和连字符。作者字段支持 Markdown；用 `**Kairan Dou**` 突出本人，等贡献星号写成 `\*`，此时使用示例中的单引号或 `>-` 长文本写法，避免 YAML 双引号的转义规则。论文只展示主图和标题、作者、发表信息、引用数、资源入口，不填写或显示介绍段落。链接可按需要添加 Project、Code 等。

配图放在 `images/`，使用 `/images/paper.png` 这样的根相对路径。图片按原始比例完整显示，点击可放大；无需预先裁成固定尺寸。没有配图时将 `image` 和 `image_alt` 留空即可。

论文的 Paper 链接统一使用 `https://arxiv.org/abs/论文编号`。尚无公开入口时填写 `links: []`，标题保持纯文本，也不生成空的 Paper 按钮。

### 每篇论文的引用数

`scholar_id` 填 Google Scholar 论文详情页 URL 中 `citation_for_view=` 后的完整 ID，例如 `tWcg0ZsAAAAJ:u-x6o8ySG0sC`。`citations` 与 `citations_updated` 保存已核对的引用数和日期，例如 `159` 与 `"2026-11-05"`；未核对时填 `null` 和 `""`。未知不等于 0，网页显示 `Citations: —`。

网页加载后读取仓库 `google-scholar-stats` 分支的 `gs_data.json`，有更新时显示新数字和抓取日期。优先按 Scholar ID 匹配；新论文未填写 ID 时，只接受唯一且完整标题一致的记录，不将同名新版本的引用数混用。网络失败、字段无效或数据比页面快照更旧时，保留已核验快照。

仓库的 **Get Citation Data** 工作流负责定时更新，也可在 GitHub Actions 手动触发。Scholar ID 是公开标识，默认为当前主页作者；工作流无需为这个默认值配置 secret。Google Scholar 可能临时限制抓取，失败不会把旧数字覆写成 0。仓库私有时，浏览器无法匿名读取统计分支，但页面静态快照仍正常显示。引用核验来源与新论文配图见[论文素材说明](paper-sources.md)。

## 添加实习

在 `_data/internships.yml` 复制一项并填写即可，不需要修改网页模板：

```yaml
- organization: "公司名称"
  role: "实习岗位名称"
  start: "2026-07"
  end: null
  logo: "/images/companies/company.png"
  url: "https://example.com"
```

`end: null` 表示 Present；已结束的实习填写结束年月。不需要写 `summary`、项目职责或导师。标志完整显示，不裁切；横版公司字标使用横版容器。没有标志或公司网址可留空。所有实习删除并将文件内容设为 `[]` 时，实习板块与导航自动隐藏。学校与公司标志来源见[素材来源](institution-assets.md)。

## 保存与发布

使用两个空格缩进，不要使用 Tab。标题含冒号时加引号；长段落用 `>-`，后续文字保持缩进。保存后在本地预览，确认内容、图片和链接，再提交并推送到 GitHub，由 GitHub Pages 更新线上网站。网页本身不会直接写入仓库。

## 动效与阅读偏好

页面底部的 **Motion on / off** 可以开关动效，选择保存在当前浏览器中。系统启用“减少动态效果”时，页面优先遵循系统设置，显示 Motion reduced。首页包含柔和光晕、星点明暗、慢速扫描线和双层轨道；导航、学校 logo、论文链接提供轻量反馈。循环动效在首页区域离开视野或页面切到后台后暂停；正文不依赖 JavaScript 显示。图片仍保持完整比例，动效不改变填写内容的方式。

后续内容规划见 [TODO](TODO.md)。当前改版前的基础版本可通过本地标签 `homepage-v1-20261104` 查看。
