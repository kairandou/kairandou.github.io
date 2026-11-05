# 学术主页后续完善清单

> 更新：2026-11-05 · 当前导航：About / Education / Internships / Papers · 维护方式见[内容填写指南](content-guide.md)

让导师、合作者或招聘方快速看到研究方向、教育、实习、代表成果和联系方式。以下清单不会自动修改页面；教育与实习保持简洁，不添加研究经历板块。

## 已保存的基础版本

- [x] Orbital Scholar 基础版已保存：commit `0fe5dba`，tag `homepage-v1-20261104`，作为新增动效前的基线。
- [x] 简介、教育、论文和可选经历已拆成独立数据；[改版前完整内容](archive/homepage-before-2026-11-04.md)保留。

## P0 · 对外分享前补齐与核对

- [x] **当前身份与机构**：根据新简历更新 ByteDance Seed 当前岗位与美团实习，移除简介中的研究经历。
- [x] **联系邮箱**：已在 [profile.yml](../_data/profile.yml) 更新为新简历中的 CMU 邮箱。
- [x] **教育与实习日期**：已按简历更新 [education.yml](../_data/education.yml) 与 [internships.yml](../_data/internships.yml)；CMU 标注 Incoming 和预计毕业时间。
- [ ] **入学后更新**：2027 年 1 月实际入学后，修改简介的未来时表达，并移除 CMU 的 Incoming 标记。
- [ ] **CV**：准备最新 PDF，放入 `files/` 后在 [profile.yml](../_data/profile.yml) 的 `links` 中添加 CV；注明更新日期，保持与主页一致。
- [ ] **论文信息**：逐项核对 [publications.yml](../_data/publications.yml) 的标题、作者顺序、等贡献标记、venue、年份和发表状态，区分 preprint、workshop 与正式会议／期刊。
- [ ] **论文入口**：为有公开资源的论文补齐 Paper、Code、Project、DOI；没有的资源不留空按钮。检查已有链接是否指向正确版本。
- [ ] **BibTeX**：从论文正式页面核对元数据，为每篇论文准备可下载的 `.bib`，通过现有 `links` 添加 BibTeX；后续再考虑一键复制。

## P1 · 最值得增加的内容

- [ ] **精选机器人／项目展示**：挑选 1–2 项最能说明能力的公开成果，写清任务、方法和本人贡献，配短视频及代码／项目页。视频注明 Sim/Real、是否加速；放在对应论文下或 About 内，材料充足后再决定是否独立成页。
- [ ] **简短近况**：整理最近 3–5 条值得公开的录用、报告或项目发布消息，附年月和可验证链接；作为 About 中的紧凑列表即可，旧消息归档。
- [ ] **实习维护**：岗位或任职状态变化时更新 [internships.yml](../_data/internships.yml)，继续只展示公司、岗位与日期。
- [ ] **合作与联系**：在 [profile.yml](../_data/profile.yml) 简介末尾说明希望交流的具体方向及首选联系方式；仅在确有需求时写开放合作／求职意向。

## P2 · 有材料再添加

- [ ] **Talks / Posters**：选少量报告或海报，补活动名称、日期、slides／视频，优先挂在对应论文或项目下。
- [ ] **Teaching / Mentoring**：有实际课程或指导经历时，列角色、时间和内容；短列表可并入 About。
- [ ] **Academic service**：仅列已完成、可公开的审稿或组织工作，标注 venue 与年份。
- [ ] **Selected awards**：保留与研究、工程或申请相关的少量奖项，核对名称和时间。
- [ ] **Research notes / Blog**：有持续写作计划再开设，优先发布实验复现、方法分析或技术笔记；不为凑栏目放空页。

## 展示与维护

- [x] 已加入首屏入场、滚动显现、缓慢轨道和悬停反馈；22 项动效逻辑检查通过，桌面／手机尺寸、键盘开关、偏好保存和图片查看已验证。正文默认可见，系统减少动态效果优先。
- [x] 统一 kd. 浏览器／手机收藏图标，新增首页光晕、扫描线、星点、双层轨道和悬停反馈；原版图标与照片保留。AI 清晰化头像的来源和切换方法见[素材说明](visual-assets.md)。
- [ ] 每次发布前检查图片、PDF 和外部链接；论文图继续完整显示并可放大，CV 与公开成果保持同步。
- [ ] 内容变多时先使用摘要、折叠或详情页；只有读者确实需要直接访问的内容才增加导航项。

## 参考

[al-folio](https://github.com/alshedivat/al-folio) 可作为学术主页信息组织的参考；[Minimal Light](https://github.com/yaoyao-liu/minimal-light#edit-included-files) 展示了通过数据文件维护论文及 PDF、Code、BibTeX 链接的方式。这里借鉴信息结构，后续按实际材料选择栏目。
