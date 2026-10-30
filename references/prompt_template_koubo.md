# 口播专用提示词模板（只锁脸＋服装/场景/听众全自动设计）

用户定版（2026-10-29/30）：口播/训话类片子一律按本模板写词——**只锁主角的脸，服装由模型按场景自动设计，场景由助手按音频内容自动设计、每片必换，听众（吃瓜群众）由助手自动设计、每片必换**，不用问用户。整片一段平词一次丢（英文平词，v3 式），结构七块：Picture 1 → Setting → Who speaks → Story → Camera → Sound → Negative prompts。

## 固定句（逐字照抄，不许改写）
- 锁脸＋服装自动设计：`Only his face is locked, 1:1 identical to the card, short spiky black hair. Do not copy the reference outfit. He wears ... automatically designed by the model: ...`（中间填本片着装基调一句：按场景给方向，如休闲衬衫/深色休闲西装外套；细节款式由模型定。收尾固定带 `not a suit, not formal, no leather jacket` 一类排斥项，按本片场景增减。）
- 说话人锁定：`Only the man speaks, driven by (Audio 1), for the whole film.` 听众句固定骨架：`The N listeners never speak, their lips stay closed and still the whole time, they only listen with their own different expressions: ...（逐人写表情）... They never nod together in unison.`
- 机位固定块：`Camera: third-person observer at the side of the table for the whole film, never a point-of-view shot, never front-on to the man. The man always looks across the table at the listeners, never into the camera lens. The camera moves slowly and smoothly.`（桌子/场景物按本片场景替换）
- 声音固定块：`Sound: Only the man speaks. No narration, no background music. Non-diegetic music: none. No burned subtitles, no on-screen text, no watermark.`
- 负向词表基底（按本片场景增减场景类词）：`subtitles, closed captions, on-screen text, watermark, logo, background music, musical instruments, rhythm, narration, voiceover, listeners speaking, lip-sync from listeners, listeners nodding in unison, elderly listeners, old man, old woman, grey hair, white hair, man looking into camera lens, man facing camera front-on, point-of-view shot, selfie angle, changed face, leather jacket, young listeners`

## 可变槽（每片新填）
- **Setting**：场景助手按音频内容自动设计（地点/时段/桌椅道具/光线逐项写死）；主角位置写死；听众逐人点名（人数与男女组合自动设计、年龄一律四十多岁、逐人衣着）。
- **Who speaks 的表情部分**：逐人分开写（震惊低头/皱眉沉思/轻叹/托腮等），不许雷同、不许齐点头。
- **Story**：按原声内容写剧情与动作链；结尾高潮（起身/张臂等）整链放同一段写完、末态单独写死、关键动作至少出现两次；错误末态进负向词表（如 `the man remaining seated in the final frame`）。

## 定版样例一（母本）：《二婚警告》咖啡馆版（任务 2115849514689716225 / v20 版 2115880070819303426）

```
Picture 1: The man in the reference card. Only his face is locked, 1:1 identical to the card, short spiky black hair. Do not copy the reference outfit. He wears casual clothes automatically designed by the model: a relaxed short-sleeve casual shirt, dark casual trousers, casual sneakers, comfortable style, not a suit, not formal, no leather jacket.

Setting: daytime, a quiet café, a round marble table with comfortable chairs in a corner by a large window, coffee cups and a small teapot on the table, warm wood interior, soft daylight through the window. The man sits at one side of the table speaking intensely to 3 middle-aged listeners, all around 40 years old, seated around the table: a man of about 42 in a dark polo shirt directly across from him, a man of about 40 in a light casual shirt, and a woman of about 40 with black hair in a low ponytail wearing a casual blouse. None of the listeners is elderly.

Who speaks: Only the man speaks, driven by (Audio 1), for the whole film. The 3 listeners never speak, their lips stay closed and still the whole time, they only listen with their own different expressions: the man across is stunned and ashamed, slowly lowering his head; the other man frowns in deep thought; the woman sighs quietly and looks down. They never nod together in unison.

Story: The man lectures the man across the table about not betting his happiness on a remarried woman whose best years and savings went to her ex-husband and children. He rises halfway, leans over the table and points at him as he speaks. Near the end the man across looks down and tugs blankly at his own empty trouser pockets with both hands, lips closed. The speaker finishes standing and leaning with his finger pointed straight at him, holding that pose to the final frame, the listeners with bowed heads.

Camera: third-person observer at the side of the table for the whole film, never a point-of-view shot, never front-on to the man. The man always looks across the table at the listeners, never into the camera lens. The camera moves slowly and smoothly.

Sound: Only the man speaks. No narration, no background music. Non-diegetic music: none. No burned subtitles, no on-screen text, no watermark.

Negative prompts: subtitles, closed captions, on-screen text, watermark, logo, background music, musical instruments, rhythm, narration, voiceover, listeners speaking, lip-sync from listeners, listeners nodding in unison, elderly listeners, old man, old woman, grey hair, white hair, man looking into camera lens, man facing camera front-on, point-of-view shot, selfie angle, changed face, suit, formal outfit, leather jacket, night, park, young listeners.
```

## 变体样例二：办公室版（《折腾训话》，任务 2115913430815952898；场景＝会议室、听众＝4 名老板）

```
Picture 1: The man in the reference card. Only his face is locked, exactly 1:1 identical to the card, short spiky black hair. Do not copy the outfit in the reference picture. He wears a dignified outfit designed by the model for a senior man lecturing in an office: a dark casual blazer over a plain dark shirt, dark trousers, clean and commanding, no tie, no leather jacket.

Setting: Daytime, a modern company office meeting room, a long dark wooden conference table with leather chairs, a few documents and teacups on the table, floor-to-ceiling windows with soft daylight, dark office cabinets along the wall. The man stands at the head of the table, lecturing four company bosses seated along both sides of the table, all in their forties: a heavyset man in a dark suit, a slim man in a grey suit, a man in a navy blazer, and a woman with neat shoulder-length hair in a dark business blazer. No elderly people.

Who speaks: Only the standing man speaks for the whole video, driven by (Audio 1). The four bosses never speak, their lips stay closed and still the whole time, they only listen, each with a different expression: the heavyset man frowns and looks down, thinking hard; the slim man nods slowly once, thoughtful; the man in the navy blazer looks stunned and embarrassed; the woman presses her lips together and looks down at her notebook. They never nod together at the same time.

Story: The standing man passionately lectures the seated bosses: there is no business in the world with zero risk, nobody gets rich sitting at home, and only by constantly hustling and taking action can a person find money and opportunity and become a big boss. He points at them while he speaks, slaps his own chest, raises one finger to drive a point home, and near the end thrusts his open palm forward toward them, finishing in a strong, determined pose held to the very last frame while the bosses sit in silence with lowered heads.

Camera: A third-person observer camera at the side of the conference table for the whole video, never a POV shot, never facing the man frontally. The man always looks at the bosses along the table, never at the camera. The camera moves slowly and smoothly.

Sound: Only the standing man speaking. No narration, no background music, non-diegetic music: none. No burned subtitles, no on-screen text, no watermark.

Negative prompts: subtitles, closed captions, on-screen text, watermark, logo, background music, musical instruments, rhythm, narration, voice-over, listeners speaking, listener lip movement, listeners nodding together, elderly people, old man, old woman, white hair, the man looking at the camera, the man facing the camera frontally, POV shot, selfie angle, face change, leather jacket, night scene, young listeners.
```

## 变体样例三：茶馆版（《吹牛语录》，任务 2115919797740064769；场景＝老茶馆、听众＝3 名茶客）

```
Picture 1: The man in the reference card. Only his face is locked, exactly 1:1 identical to the card, short spiky black hair. Do not copy the outfit in the reference picture. He wears a casual outfit designed by the model: a loose dark short-sleeve shirt and dark trousers, relaxed and dignified, no tie, no leather jacket.

Setting: Daytime, an old Chengdu-style teahouse, bamboo chairs around a square wooden table, covered porcelain tea bowls and a small teapot on the table, carved wooden lattice windows with soft daylight streaming in, green potted plants, a few empty tables softly blurred in the background. The man sits at one side of the table, lecturing three listeners seated around the same table, all in their forties: a heavyset man in a dark polo shirt, a woman with neat short hair in a light blouse, and a slim man in a light-colored casual shirt. No elderly people.

Who speaks: Only the man speaks for the whole video, driven by (Audio 1). The three listeners never speak, their lips stay closed and still the whole time, they only listen, each with a different expression: the heavyset man looks skeptical, frowning with his arms crossed; the woman looks amused, with a slight smile and one hand resting on her chin; the slim man looks thoughtful and nods slowly once. They never nod together at the same time.

Story: The man lectures the listeners that bragging is the great wisdom of the I Ching: bragging is yang energy, and however capable a person is, if he never brags he will never rise; yin and yang generate each other, and with yin alone nothing can get moving, and this principle applies to everything. Seated, he jabs one finger upward to make his points and slaps the table lightly once. In the final seconds he puts both hands on the table, stands up, spreads his arms wide toward the listeners and delivers the last line standing, ending frozen in that standing pose with arms spread wide at the very last frame, while the listeners look up at him in silence.

Camera: A third-person observer camera at the side of the table for the whole video, never a POV shot, never facing the man frontally. The man always looks at the listeners across the table, never at the camera. The camera moves slowly and smoothly.

Sound: Only the man speaking. No narration, no background music, non-diegetic music: none. No burned subtitles, no on-screen text, no watermark.

Negative prompts: subtitles, closed captions, on-screen text, watermark, logo, background music, musical instruments, rhythm, narration, voice-over, listeners speaking, listener lip movement, listeners nodding together, elderly people, old man, old woman, white hair, the man looking at the camera, the man facing the camera frontally, POV shot, selfie angle, face change, leather jacket, the man remaining seated in the final frame, night scene, rooftop, office.
```
