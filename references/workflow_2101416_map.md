# 工作流 2101416149702504449 图谱与实测（2026-10-04 钉死）

来源：零扣费哨兵普查（49 个存在节点）＋回片元数据里嵌的完整 ComfyUI 执行图谱＋2 条 6 秒付费实测。原始普查日志：~/workspace/audio_drive_rant/probe_2101416_*.log、probe_2101416_census.md。

## 主线路（MiniMax H3 Ref2VA · 音频驱动 · 音画同出）

| 功能 | 节点.字段 | 实证接线 |
| :--- | :--- | :--- |
| **提示词** | **79**.prompt | CR Prompt Text → 76.prompt。**全流唯一的真提示词位**，字段名是 `prompt` 不是 text/value——只扫 text/value 的普查会漏掉它（首测就栽在这） |
| 时长 | **73**.value | PrimitiveFloat（秒）→ 75 帧数公式 `max(5, round(a*24)) + 补齐到 17 的倍数` |
| 画幅 | **78**.aspect_ratio | ResolutionSelector，默认 `9:16 (Portrait Widescreen)`，1.0MP |
| 种子 | **62**.noise_seed | RandomNoise |
| 图片 1 | **72**.image | LoadImage → 76.ref_images.ref_image_0 |
| 图片 2 | **101**.image | LoadImage → 76.ref_images.ref_image_1 |
| **驱动音频** | **74**.audio | LoadAudio → 76.drive_audio（真驱动口） |
| 合流出口 | **84**（VHS_VideoCombine） | **audio 输入绝不许传值**——作者默认接线负责把声音合进出片；传任何值（哪怕静音文件名）都会顶掉音轨，首测实证出无声片 |

核心算子：76 MiniMaxH3AudioConditioningT8（task_type=Ref2VA，audio_mode=remix_source，strict_prompt_tags=True，prompt_primary_audio_ordinal=1）＋ 65 MiniMaxH3DualClockSamplerT8「STABLE 4v4a」（8 步，shift_audio 3.0 / shift_video 12.0）＋ 80 MiniMaxH3AVDecodeT8。模型 UNET = DasiwaMinimaxH3_dasiwaREF2VAHybridV1 + turbo LoRA（71）。

## 支线（与主视频无关，永不传值）

- 104–129：anima/qwen 生图支线（17 个 LoRA + KSampler 121，positive=125 / negative=124），产 80×80 图打包 zip（126）。123 是 JjkText，无消费者。
- 131 SaveImage「rh_publish_fix」：把成片逐帧存成 PNG（发布修复用）。

## 出片实测（测试2，taskId 2106741900399833089）

- 输入：刁哥图（72）＋老婆图（101）＋6s 餐厅抱怨原声（74）＋79 换成抱怨版 Ref2VA 词＋73=6.0＋78=9:16＋62 种子；84 不碰。
- 出片：768×1376 / 24fps / 6.583s（时长仍有 +0.58s 帧数溢出），**自带 AAC 44.1kHz 音轨**，与驱动原声互相关 **0.998 @ 零时滞**（电平低约 3.8dB——remix_source 混入了提示词写的环境声，属预期）。
- 质检：验脸 PASS（两人对版）、刁哥全程开口＋手势、老婆闭口聆听、无烧字。用户看片评「非常完美」，2026-10-04 拍板以此流**替换**旧线 2106642679642812418。
- 测试片：~/workspace/your_files/新流2101416_音频驱动测试6秒.mp4

## 坑位清单

1. 79 字段名 `prompt`：普查/派发都别按 text/value 找它。
2. 84 传值 = 没音轨：派发清单里永远不要出现 nodeId 84。
3. results 顺序不稳：zip 可能排第一，取文件按 outputType == "mp4" 挑，不许拿 results[0]。
4. 作者预置提示词（79 默认值）是一支奶茶店双女主样片词——每单必须整段替换成当单提示词，漏换就演作者的戏（首测实证）。
5. 回片元数据（comment 标签）里含完整图谱 JSON + 全部提示词：拼片交付时按既有定版剥元数据（-map_metadata -1）。

## 用户自存版（现行派发出口，2026-10-04 晚）

- 用户在网页端屏蔽 131 后另存为自己的工作流：**2106756389191372802**（https://www.runninghub.cn/post/2106756389191372802）。
- 零扣费探针复验：79.prompt / 73.value / 78.aspect_ratio / 62.noise_seed / 72.image / 101.image / 74.audio 全部 OK、与源流一致；**131 已不在图内**（node_not_found）——出片不再带帧图，results 应只有 mp4（＋可能一个 zip，若支线未屏蔽）。
- H3YQ 派发器与 SKILL.md 已切到此 ID；源流 2101416149702504449 只作图谱出处留档。
