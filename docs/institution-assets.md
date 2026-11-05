# 学校与公司标志来源

核对日期：2026-11-05。用于个人教育与实习经历展示，不表示相关机构背书。图片保留来源的颜色与比例，网页使用 `object-fit: contain` 完整显示，不裁切标志。来源文件下载至仓库后本地加载，不依赖远程图片热链。

| 机构 | 网站使用的文件 | 来源与说明 |
| --- | --- | --- |
| Carnegie Mellon University | `images/institutions/carnegie-mellon.png`，900 × 900 | [官方品牌页](https://brand.cmu.edu/visual-identity/carnegie-mellon-trademarks/university-logo)的红底白字方形标志；[原始图片](https://live-cmu-brand.pantheonsite.io/sites/default/files/cmu-brand-files/inline-images/cmu-wordmark-square-w-on-r%201.png)。 |
| University of California, Berkeley | `images/ucb.png`，沿用现有校徽 | 对照[官方校徽说明](https://brand.berkeley.edu/visual-identity/icons-secondary-marks/uc-berkeley-seal/)核对。新收集的官网示意图带大幅背景与留白，保留现有小尺寸展示更清楚的校徽。 |
| Nankai University | `images/institutions/nankai.png`，1200 × 1200 | 原仓库 `images/nku.png` 的原样副本；对照[南开官方校徽页](https://www.nankai.edu.cn/164/list.htm)核对双圆、八角星和 1919 图形。官网图片下载遇到 TLS 错误，因此未将此文件标记为本次官网下载。 |
| ByteDance Seed | `images/companies/bytedance-seed.png`，720 × 96 | [Seed 官网](https://seed.bytedance.com/en/)当前使用的完整 ByteDance Seed 横版字标；[官方图片](https://lf-flow-web-cdn.doubao.com/obj/flow-doubao/deploy/flow/ai_official_website/88329/static/image/footer_brand_logo.a2d9c12f.png)。没有用 ByteDance 通用图形替代 Seed 字标。 |
| Meituan | `images/companies/meituan.png`，1896 × 687 | [美团官方媒体资源页](https://www.meituan.com/media)的[官方素材包](https://s3plus.meituan.net/smart/22c45b30-80ba-4aa5-bfad-2bfaed7beb4e.zip)，其中的 `美团/美团横式色彩标识.png`。 |

## 已收集的备选原始素材

- `images/institutions/berkeley-wordmark.png`，4100 × 2625：[官方 logo 页](https://brand.berkeley.edu/visual-identity/logos/)的[示意图](https://brand.berkeley.edu/wp-content/uploads/2024/08/logo-variations-thumbnail-blue-white.png)。
- `images/institutions/berkeley-seal.png`，4100 × 2625：[官方校徽示意图](https://brand.berkeley.edu/wp-content/uploads/2024/08/brand-essentials-thumbnail.png)。这两张图片均保留官网原始背景和留白，未直接用于紧凑经历列表。
- `images/companies/meituan-symbol.png`，100 × 100：[美团官网分享图片](https://p0.meituan.net/smartvenus/519f64f1d51d8470ecad1f9b5fce83591696.png)，适用于约 44–48px 的小图标；当前页面使用更清晰的横版原图。

之后更换图片，只需修改 `_data/education.yml` 或 `_data/internships.yml` 的 `logo` 字段；使用以 `/images/` 开头的仓库路径。
