# 学术主页后续完善清单

> 更新：2026-11-04 · 当前导航：About / Education / Papers · 维护方式见[内容填写指南](content-guide.md)

让导师、合作者或招聘方快速看到“研究方向 → 代表成果 → 经历与贡献 → 联系方式”。优先补齐可信内容，再增加栏目；以下清单不会自动修改页面，顶层导航继续保持三个入口。

## 已保存的基础版本

- [x] Orbital Scholar 基础版已保存：commit `0fe5dba`，tag `homepage-v1-20261104`，作为新增动效前的基线。
- [x] 简介、教育、论文和可选经历已拆成独立数据；[改版前完整内容](archive/homepage-before-2026-11-04.md)保留。

## P0 · 对外分享前补齐与核对

- [ ] **当前身份与机构**：核对并更新 [profile.yml](../_data/profile.yml) 的简介，用一句话说明现在做什么；不把旧的研究经历回顾当作当前任职。
- [ ] **可用邮箱**：确认现有 Berkeley 邮箱是否仍适合作为长期联系地址；在 [profile.yml](../_data/profile.yml) 统一修改 Email 链接。
- [ ] **经历日期**：核对 [experience.yml](../_data/experience.yml) 中 MIT/Harvard、UT Austin 的结束日期；目前 `null` 仅沿用旧站信息。核对 [education.yml](../_data/education.yml) 的学位名称与实际起止日期。
- [ ] **CV**：准备最新 PDF，放入 `files/` 后在 [profile.yml](../_data/profile.yml) 的 `links` 中添加 CV；注明更新日期，保持与主页一致。
- [ ] **论文信息**：逐项核对 [publications.yml](../_data/publications.yml) 的标题、作者顺序、等贡献标记、venue、年份和发表状态，区分 preprint、workshop 与正式会议／期刊。
- [ ] **论文入口**：为有公开资源的论文补齐 Paper、Code、Project、DOI；没有的资源不留空按钮。检查已有链接是否指向正确版本。
- [ ] **BibTeX**：从论文正式页面核对元数据，为每篇论文准备可下载的 `.bib`，通过现有 `links` 添加 BibTeX；后续再考虑一键复制。

## P1 · 最值得增加的内容

- [ ] **精选机器人／项目展示**：挑选 1–2 项最能说明能力的公开成果，写清任务、方法和本人贡献，配短视频及代码／项目页。视频注明 Sim/Real、是否加速；放在对应论文下或 About 内，材料充足后再决定是否独立成页。
- [ ] **简短近况**：整理最近 3–5 条值得公开的录用、报告或项目发布消息，附年月和可验证链接；作为 About 中的紧凑列表即可，旧消息归档。
- [ ] **详细科研／工作经历（可选）**：核对信息后启用 [experience.yml](../_data/experience.yml)，每段保留 1–2 句研究问题和个人贡献；显示在 About 的 Research experience 内，不新增导航。
- [ ] **合作与联系**：在 [profile.yml](../_data/profile.yml) 简介末尾说明希望交流的具体方向及首选联系方式；仅在确有需求时写开放合作／求职意向。

## P2 · 有材料再添加

- [ ] **Talks / Posters**：选少量报告或海报，补活动名称、日期、slides／视频，优先挂在对应论文或项目下。
- [ ] **Teaching / Mentoring**：有实际课程或指导经历时，列角色、时间和内容；短列表可并入 About。
- [ ] **Academic service**：仅列已完成、可公开的审稿或组织工作，标注 venue 与年份。
- [ ] **Selected awards**：保留与研究、工程或申请相关的少量奖项，核对名称和时间。
- [ ] **Research notes / Blog**：有持续写作计划再开设，优先发布实验复现、方法分析或技术笔记；不为凑栏目放空页。

## 展示与维护

- [x] 已加入首屏入场、滚动显现、缓慢轨道和悬停反馈；22 项动效逻辑检查通过，桌面／手机尺寸、键盘开关、偏好保存和图片查看已验证。正文默认可见，系统减少动态效果优先。
- [ ] 每次发布前检查图片、PDF 和外部链接；论文图继续完整显示并可放大，CV 与公开成果保持同步。
- [ ] 内容变多时先使用摘要、折叠或详情页；只有读者确实需要直接访问的内容才增加导航项。

## 参考

[al-folio](https://github.com/alshedivat/al-folio) 可作为学术主页信息组织的参考；[Minimal Light](https://github.com/yaoyao-liu/minimal-light#edit-included-files) 展示了通过数据文件维护论文及 PDF、Code、BibTeX 链接的方式。这里借鉴信息结构，后续按实际材料选择栏目。
