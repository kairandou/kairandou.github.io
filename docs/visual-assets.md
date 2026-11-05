# 网站标志与照片

## kd. 标志

浏览器标签、收藏和手机主屏幕使用 `images/branding/` 下的 kd. 图标，与页眉文字标志保持一致。矢量源为该目录中的 SVG；旧版图标仍保留，便于回退。

## 当前头像：左侧背景清理 v2

- 当前版本：`images/profile-left-clean-v2.png`，1254 × 1254。
- 生成方式：内置 imagegen 局部编辑，仅移除左侧背景的门、门框和设施，并以原有米黄色墙面补齐。原图与历史清晰化版本 v1 均保留。
- 本次提示摘要：仅清除左侧背景门和设施，以原米黄色墙面补齐；保留人物、讲台、麦克风和构图。这是编辑要求，不表示输出与输入逐像素一致。

## 历史清晰化版本 v1

- 原图：`images/profile.png`，1280 × 1280，完整保留。
- 历史清晰化版本：`images/profile-enhanced-v1.png`，1254 × 1254。
- 生成方式：内置 imagegen，以原图为编辑目标，做保守去模糊与清晰化。实际输出尺寸以文件为准；虽然提示请求 2048 × 2048，工具实际返回 1254 × 1254，因此这是清晰度增强，不是更高像素的原始照片。
- AI 可能重建原片缺失的细节，不能等同于找回相机原始细节。如果有相机原片，优先使用原片。

v1 使用的完整提示：

```text
Use case: identity-preserve. Asset type: existing personal academic homepage portrait, photo restoration. Input image 1 is the exact edit target. Primary request: carefully deblur and upscale this same photograph to a clean 2048 by 2048 square image. Preserve the person's identity, facial geometry, eye shape, expression, hair, glasses, head angle, body pose, dark suit, white shirt and tie exactly. Preserve the composition, framing, yellow lecture-room wall, dark lectern, microphone, lighting and colors. Only reduce blur and compression artifacts and restore natural-looking edge definition conservatively. Do not beautify, reshape the face, change apparent age, remove glasses, replace the background, crop, add details or objects, or turn it into a new portrait. Keep photographic texture and avoid waxy skin, artificial eyelashes and oversharpening halos. It should be recognizably the same real photo, with improved clarity rather than a reimagining.
```

## 切换与回退

在 `_data/profile.yml` 修改 `portrait`、`portrait_width` 和 `portrait_height`：

| 版本 | `portrait` | 宽高 |
| --- | --- | --- |
| 当前 v2 | `/images/profile-left-clean-v2.png` | 均为 `1254` |
| 历史 v1 | `/images/profile-enhanced-v1.png` | 均为 `1254` |
| 原图 | `/images/profile.png` | 均为 `1280` |
