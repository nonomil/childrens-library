# 儿童互动课件·有声绘本·AI开发 — 完整合并版调研报告

# 儿童互动课件·有声绘本·AI开发 — 完整合并版调研报告

版本：v2\.0 合并版 \| 日期：2026\-05\-28 \| 数据源：Camoufox直抓小红书 \+ GitHub \+ 行业政策

---

## 一、调研概况

本报告整合了两份独立调研（完整调研报告 \+ 全景指南），合并重复内容，补全5项关键遗漏，统一技术选型结论。

### 核心发现（5句话）

- ① 翻页引擎 Turn\.js 够用不换，分支叙事选 Ink/inkjs（MIT授权，AI生成脚本最友好）

- ② 最大差异化机会：Galgame式分支互动 \+ AI语音朗读（构建阶段用Edge\-TTS/Qwen3\-TTS生成mp3）

- ③ PBS\-KIDS/HTML5\-Storybook 可学习架构但注意其代码默认All Rights Reserved，不能直接用

- ④ 组件运行时契约（init→mount→unmount→resize→update）是当前方案从「能用」到「好复用」的关键缺失

- ⑤ 音频文件走OSS/CDN而非放仓库（每个课件5\-15MB），GitHub Pages只托管HTML/CSS/JS

---

### 调研方法

- GitHub搜索：Turn\.js\(7\.4k⭐\)、OpenMAIC\(4\.5k\+⭐\)、WebGAL、Ink/inkjs、PixiJS\(47k⭐\)、Phaser\(37k⭐\)等

- Camoufox直抓小红书：10个关键词，6个有有效结果，TOP10高赞笔记提取

- 行业政策：教育部2025政策、江苏省2025\-2027方案、市场规模数据

- 交叉验证：XHS数据 vs GitHub星标 vs 行业政策，关键结论至少2个独立来源确认

---

## 二、开源引擎选型

### 2\.1 翻页引擎对比

- Turn\.js（7\.4k⭐，jQuery）— 当前方案，成熟稳定已跑通，建议不换

- premium\-flipbook\-pdf\-viewer（WebGL\+CSS3D）— 三模渲染，若升级翻页效果是最佳替代

- FlipBook\.js（零依赖）— 太轻功能不够，不推荐

- 3D FlipBook（jQuery\+Three\.js）— 过重，杀鸡用牛刀

结论：Turn\.js 继续用，不换引擎。当前阶段翻页不是瓶颈。

---

### 2\.2 分支叙事引擎对比 — Ink vs WebGAL vs Twine

统一结论：Ink/inkjs 是本项目的最佳选择



选型决策表：

- 想快速原型，非开发者操作 → WebGAL（有图形编辑器）

- 想让AI批量生成分支脚本 → Ink（纯文本，AI输出最友好）★★★ 本项目选这个

- 分支逻辑嵌入现有HTML课件 → inkjs（纯JS渲染，嵌入方便）

- 孩子自己创作分支故事 → WebGAL \+ WebGAL\_Terre

- 用Twine快速做原型验证 → Twine（H5P格式，但不适合生产）



Ink 详解：

- 来源：Inkle Studios，MIT授权，专业叙事脚本语言

- 核心优势：纯文本脚本 → AI（Claude/DeepSeek）可直接批量生成\.ink文件

- 运行时：inkjs（JavaScript库）可在任何现代浏览器运行，无需后端

- 与TEMPLATE\_CONFIG集成：定义 branch\-story 组件类型，\.ink脚本作为数据源

- GitHub: inkle/ink（13k\+⭐），社区活跃，文档完善



WebGAL 详情：

- 来源：OpenWebGAL团队，MPL\-2\.0协议（有传染性，修改需开源）

- 核心能力：零代码创建分支剧情，支持背景/立绘/对话/选择分支

- 编辑器：WebGAL\_Terre 提供图形化编辑界面

- 缺点：协议传染性、包体较大、偏成人向需适配儿童UI

- 适用场景：孩子自己创作分支故事时使用

---

### 2\.3 互动引擎参考

PBS\-KIDS/HTML5\-Storybook：PBS官方儿童故事书引擎

- 发现价值：专为儿童设计的HTML5故事书架构，支持动画\+音频\+交互

- 许可注意：⚠️ 仓库无明确开源许可证，默认All Rights Reserved

- 使用方式：仅可学习架构设计思路，不可直接复制代码

- 当前状态：GitHub仓库可能已私有化或迁移（404），需确认



其他参考项目：

- LiveStory（4⭐）— AI角色语音对话互动绘本

- flipbook\-builder（0⭐）— 单文件儿童电子书编辑器

- Generative\-AI\-Storybook — AI故事书生成器

---

### 2\.4 Canvas渲染层选型

- Canvas 2D（当前方案）— 齿轮/太阳系场景绑绑有余，不换

- PixiJS（47k⭐，WebGL）— 等交互复杂到粒子/碰撞时再引入

- Phaser（37k⭐，基于PixiJS）— 如果要做小游戏（匹配/拖拽），比纯Canvas好

- Paper\.js（矢量图形）— 适合太阳系轨道等精确路径，可作为备选

结论：Canvas 2D不动，不引入PixiJS/Phaser。

---

### 2\.5 TTS方案对比（构建阶段调用，输出静态mp3）

重要说明：Edge\-TTS/Qwen3\-TTS 是在内容生成阶段调用API，产出mp3文件存入assets/，最终部署到GitHub Pages的是静态音频文件。浏览器端不运行TTS。



- Edge\-TTS（免费）— 微软Azure语音，300\+声音，支持中文童声（XiaoxiaoNeural/XiaoyiNeural），零成本，pip install edge\-tts

- MiniMax TTS（付费）— minimax\-speech\-2\.8，音质最佳支持情感控制，适合高级场景

- Qwen3\-TTS（开源）— 阿里通义，10语言SOTA级稳定性，支持语音克隆

- Qwen3\-TTS\-VC — 声音克隆变体，录制3\-5秒参考音频即可克隆音色，可用家长声音讲绘本

- CosyVoice（开源）— 阿里通义，零样本语音克隆，适合定制童声



推荐路径：

- 默认方案：Edge\-TTS（免费\+质量够用，中文童声XiaoxiaoNeural效果好）

- 高级方案：Qwen3\-TTS\-VC（用家长声音克隆讲绘本，情感更自然）

- 未来方案：Qwen3\-TTS开源自部署（免API费用，SOTA级质量）

---

### 2\.6 音频文件存储策略

每个课件预计5\-15MB音频文件（多角色朗读\+音效），GitHub Pages有1GB仓库限制。



- 方案A（推荐）：音频存OSS/CDN — 构建时上传到阿里云OSS/腾讯云COS，HTML用绝对URL引用

- 方案B：音频存GitHub仓库 — 仅适合小体量（\&lt;10个课件），超过1GB需拆仓库

- 方案C：浏览器端Web Speech API — 免存储但音质差、无情感控制、不可靠



推荐：起步阶段用方案B（音频直接放仓库），课件超过10个后迁移到方案A（OSS/CDN）

---

## 三、AI辅助开发工作流

### 3\.1 开发工具链

- Hermes Agent — 主力开发Agent，协调子任务

- Claude Code — 高质量代码生成（适合复杂组件）

- DeepSeek — 中文理解强，适合故事脚本生成

- OpenCode — 轻量级编码助手

---

### 3\.2 内容生成流水线（构建阶段）

完整管线：AI生成故事 → AI生成分支\(\.ink\) → Edge\-TTS生成音频\(\.mp3\) → 模板渲染HTML → 部署



- 步骤1：DeepSeek/Claude生成故事文本（中文，适龄4\-8岁）

- 步骤2：Claude生成\.ink分支脚本（分支点设计：安全选择为主，偶有挑战）

- 步骤3：Edge\-TTS批量生成mp3（多角色：旁白XiaoxiaoNeural \+ 角色YunxiNeural）

- 步骤4：HTML模板 \+ inkjs渲染器 \+ 音频引用 → 单文件课件

- 步骤5：手动审核（安全检查：无恐惧元素、分支结果积极）

---

### 3\.3 AI生成内容安全检查清单

- 分支选择后无永久负面后果（可以绕回来）

- 不含恐怖/暴力/惩罚性内容

- 角色遇到困难时有支持系统（朋友/家人/老师）

- 鼓励好奇心和探索，不惩罚错误选择

- 语言适龄（4\-8岁词汇范围）

---

## 四、内容设计与儿童体验

### 4\.1 视觉风格体系

四个适龄变体（已定义CSS变量）：

- 太空冒险（Space Adventure）— 深蓝\#0B1026 \+ 星光色 \+ 星球/火箭元素

- 森林动物（Forest Friends）— 森林绿\#1A3A2A \+ 蘑菇/蝴蝶元素

- 海洋世界（Ocean World）— 海洋蓝\#0A1628 \+ 鱼群/珊瑚元素

- 童话城堡（Fairy Tale）— 紫色\#2A1B3D \+ 城堡/星星元素



设计原则：

- 圆角8px\+柔和阴影，无锐利元素

- 配色柔和不刺眼，对比度适中

- 角色大头小身（chibi风格），表情夸张友好

- 字体：圆体优先（如站酷快乐体、思源圆体）

---

### 4\.2 组件库清单

基础组件：

- text\-block — 文本展示（支持打字机效果）

- image\-display — 图片展示（支持缩放/动画）

- audio\-player — 音频播放（支持自动播放/循环）

- interactive\-canvas — Canvas交互（齿轮/太阳系等）

- choice\-button — 选择按钮（分支叙事触发器）



新增分支叙事组件：

- branch\-story — Ink脚本驱动的分支叙事引擎（详见第六章）

---

### 4\.3 主题扩展路线图（按优先级）

第一批（核心）— 已完成：齿轮联动、太阳系、太阳的旅程

第二批（高优先级）— 本周探索：

- 恐龙世界 — 互动探索\+分支选择（用Ink做：选A路遇到霸王龙/选B路遇到三角龙）

- 海底探险 — 拼图\+声音互动\+分支叙事

第三批（中优先级）— 下周：太空站、城市建造

第四批（低优先级）— 未来：自然四季、中国传统文化

---

## 五、家庭教育AI设计原则

来自真实用户访谈和教育心理学研究的5条原则：



- ① AI做脚手架，家长做见证者 — AI引导过程，但让家长成为孩子的「首席观众」

- ② 声音比文字先行 — 4岁孩子不认字，TTS朗读\+音效是核心交互通道

- ③ 选择即学习 — 分支叙事让孩子做选择，每个选择都有意义但没有「错误答案」

- ④ 3分钟原则 — 单次互动不超过3分钟，超时自动暂停\+鼓励休息

- ⑤ 安全边界硬编码 — 分支选择后无永久负面后果，不含恐怖/惩罚性内容

---

### 5\.1 语音与朗读策略

- 默认自动朗读每页文本（用Edge\-TTS预生成mp3）

- 多角色：旁白用XiaoxiaoNeural，角色对话用YunxiNeural/XiaoyiNeural

- 支持「再读一遍」按钮（孩子常要求重复）

- 音效：翻页声、选择正确提示音、环境音（可选）

---

### 5\.2 家长陪伴模式

- 家长端显示：孩子当前进度、选择偏好、停留时间

- 可选：家长收到孩子完成课件的通知

- 可选：家长可自定义故事角色名字（如把主角改成孩子名字）

---

## 六、TEMPLATE\_CONFIG 架构升级

### 6\.1 组件生命周期契约

所有组件必须实现：init\(el, config\) → \{ mount, unmount, resize, update \}

- init: 创建组件实例，绑定DOM元素

- mount: 组件进入活跃状态（开始动画/音频）

- unmount: 组件离开（停止动画/音频，释放资源）

- resize: 容器尺寸变化时响应

- update: 配置更新时重新渲染

这是从「能用」到「好复用」的关键缺失。没有这个契约，换主题时组件行为不可预测。

---

### 6\.2 branch\-story 组件定义（Ink集成）

新增组件类型：branch\-story，将Ink脚本嵌入TEMPLATE\_CONFIG



数据结构示例：

> \{\&\#34;id\&\#34;: \&\#34;greeting\&\#34;, \&\#34;component\&\#34;: \&\#34;branch\-story\&\#34;, \&\#34;componentConfig\&\#34;: \{\&\#34;source\&\#34;: \&\#34;ink\&\#34;, \&\#34;script\&\#34;: \&\#34;stories/steve\-first\-day\.ink\&\#34;, \&\#34;characters\&\#34;: \{\&\#34;narrator\&\#34;: \&\#34;zh\-CN\-XiaoxiaoNeural\&\#34;, \&\#34;steve\&\#34;: \&\#34;zh\-CN\-YunxiNeural\&\#34;, \&\#34;alex\&\#34;: \&\#34;zh\-CN\-XiaoyiNeural\&\#34;\}, \&\#34;fallbackText\&\#34;: \&\#34;史蒂夫第一天上学\.\.\.\&\#34;\}\}



组件行为：

- 加载阶段：inkjs解析\.ink脚本，生成故事树

- 渲染阶段：显示当前节点文本，自动朗读（Edge\-TTS预生成mp3）

- 交互阶段：遇到分支点，渲染选择按钮

- 音频映射：characters配置中的角色名 → 对应mp3文件路径



Ink脚本示例（AI可批量生成）：

> == first day ==
Steve walks to school with his new backpack\.
\+ \[Walk in nervously\] \-\&gt; nervous
\+ \[Run in happily\] \-\&gt; excited
== nervous ==
Steve is nervous, but takes a deep breath\.\.\.
\-\&gt; meet\_alex
== excited ==
Steve runs into the classroom\!
\-\&gt; meet\_alex
== meet\_alex ==
A boy waves: \&\#34;Hi\! I am Alex\!\&\#34;
\+ \[Wave back\] \-\&gt; friends
\+ \[Nod shyly\] \-\&gt; friends
== friends ==
Steve made his first friend\!
\-\&gt; END

---

### 6\.3 图片预加载管线

- 模板层加 preloadPrev/Next 策略（预加载前后各1页图片）

- 配图缺口自动管理：loading → fallback（纯色占位） → loaded

- 支持懒加载（Intersection Observer API）

---

### 6\.4 选做：更多组件类型

- quiz — 互动小测验（选择题\+即时反馈）

- puzzle — 拼图/拖拽互动

- memory\-game — 记忆翻牌游戏

- timer — 倒计时（限时挑战）

这些是锦上添花，不是MVP必须。优先把基础组件和branch\-story做好。

---

## 七、小红书数据洞察

### 7\.1 关键词热度（Camoufox直抓，2026\-05\-28）

- 互动课件：23条，最高5759👍（全景VR课件教程）

- 儿童故事 网页：25条，最高5349👍（Galgame式故事）

- 电子绘本 制作：19条，最高4494👍（AI做绘本教程）

- 有声绘本：16条，最高5059👍（有声绘本朗读）

- Tea app 绘本：17条，最高9216👍（免费绘本资源）

- Canvas 儿童：19条，最高1248👍（Canva动画教程）

---

### 7\.2 高赞笔记TOP10

- 9216👍 — 14000册原版英语绘本免费阅读（@落樱YING）

- 5759👍 — 保姆级教程\|全景VR课件PPT制作方法（@凹老狮）

- 5349👍 — 读故事和写故事的人可以自己做Galgame了（@山音）

- 5059👍 — 《最好的面包店》这样读，宝宝一天听8遍！（@铃铛麻麻）

- 4494👍 — 五分钟教你用AI制作绘本！附详细提示词（@暴走的阿川）

- 4253👍 — 高质量PPT生成（@设计师Cc）

- 3493👍 — 一个简单、免费的英文绘本网站（@一只大鸭梨🍐）

- 2702👍 — AI赋能｜生成完整课件\+课堂互动小游戏（@糯米棋棋子）

- 2612👍 — AI一键生成期末班会PPT（@99m\-AIGC）

- 1659👍 — 国家连免费儿童科普都帮咱准备好了（@林野）

---

### 7\.3 市场信号

- AI课件生成是当前最热方向 — Gemini/GPT生成互动课件类笔记普遍高赞

- 有声绘本家长买单意愿强 — 「有声绘本」类笔记点赞普遍过千

- Galgame式分支互动是差异化机会 — 5349👍笔记验证市场需求

- 免费资源聚合类内容传播力强 — 国家免费绘本、英文绘本网站点赞过千

- VR课件效果好但门槛高 — 5759👍但制作复杂，不适合快速量产

---

## 八、行业政策背景

- 2025年5月：教育部发布《中小学生成式人工智能使用指南\(2025年版\)》，明确支持AI互动式探究学习

- 2025年：江苏省出台《人工智能赋能教育高质量发展行动方案（2025\-2027年）》

- 2024年：教育部启动「人工智能赋能教育行动」，立项184个中小学AI教育基地

- 市场规模：2025年AI玩具/教育硬件市场预计达6\.8亿美元（World Metrics）

- 政策信号：国家层面明确支持AI\+教育，但强调「辅助」而非「替代」教师

---

## 九、优先行动清单（合并去重，按优先级排序）



🔴 P0 立刻做（本周）

* [ ] 组件生命周期契约 — 每个组件实现 init→mount→unmount→resize→update

* [ ] 图片预加载管线 — preloadPrev/Next \+ loading→fallback→loaded 状态管理

* [ ] Edge\-TTS音频生成管线 — 构建阶段批量生成mp3，存入assets/

* [ ] 定义 branch\-story 组件数据结构 — \.ink脚本 \+ 角色音色映射

---

🟡 P1 本周探索

* [ ] 用Ink\+inkjs做第一个分支叙事Demo — 选一个现有课件（如恐龙世界）加入分支

* [ ] Ink脚本AI生成测试 — 让DeepSeek/Claude批量生成5个\.ink分支故事

* [ ] 音频存储方案确认 — 起步放仓库，超10个课件后迁OSS

---

🟢 P2 下周

* [ ] Galgame式分支互动 — 完整流程：AI生成故事→Ink分支→TTS音频→模板渲染

* [ ] 闯关\+积分机制 — 每完成一页解锁新内容

* [ ] 家长端进度查看 — 孩子完成课件后通知家长

---

⚪ P3 暂缓（不值得现在做）

- 换翻页引擎 — Turn\.js够用

- 引入PixiJS/Phaser — Canvas 2D够用

- Markdown→CONFIG转换器 — 课件量太小不值得

- PWA离线 — 先解决内容质量

- OpenMAIC集成 — 太重需大幅裁剪

- PBS\-KIDS代码复用 — 许可证不明，仅学习架构

---

## 十、原始链接

开源项目：

- Turn\.js: https://github\.com/blasten/turn\.js \(7\.4k⭐\)

- Ink: https://github\.com/inkle/ink \(13k\+⭐, MIT\)

- inkjs: https://github\.com/y\-lohse/inkjs \(MIT\)

- WebGAL: https://github\.com/OpenWebGAL/WebGAL \(MPL\-2\.0\)

- OpenMAIC: https://github\.com/THU\-MAIC/OpenMAIC \(4\.5k\+⭐, AGPL\-3\.0\)

- PixiJS: https://github\.com/pixijs/pixijs \(47k⭐\)

- Phaser: https://github\.com/phaserjs/phaser \(37k⭐\)

- premium\-flipbook\-pdf\-viewer: https://github\.com/nickyarvidson/premium\-flipbook\-pdf\-viewer



TTS方案：

- Edge\-TTS: https://github\.com/rany2/edge\-tts \(免费, 300\+声音\)

- Qwen3\-TTS: https://github\.com/QwenLM/Qwen3\-TTS \(开源, 49种音色\)

- CosyVoice: https://github\.com/FunAudioLLM/CosyVoice \(开源, 零样本克隆\)

- MiniMax TTS API: https://platform\.minimaxi\.com \(minimax\-speech\-2\.8\)



行业政策：

- 教育部《中小学生成式人工智能使用指南\(2025年版\)》

- 江苏省《人工智能赋能教育高质量发展行动方案（2025\-2027年）》

- World Metrics: AI教育玩具市场规模数据



前序文档（已合并入本报告）：

- 绘本图书馆课件：完整调研报告（综合版）: https://zcnr5y1k0s0o\.feishu\.cn/wiki/GvrywBYoJiquyJksNB6cXysEnec

- AI辅助儿童课件·绘本·HTML开发全景指南: https://zcnr5y1k0s0o\.feishu\.cn/wiki/H3mgwJwuEiWakykdNQyc0j23ntd

- 原始调研报告（第一版）: https://zcnr5y1k0s0o\.feishu\.cn/docx/BZjLd6NfnoDCVDxUroncv9ARnec

---

调研执行：Hermes Agent \| 审查：OpenClaw \+ Hermes \| 版本：v2\.0 合并版 \| 日期：2026\-05\-28

# 十一、实施进度更新（2026\-05\-28 18:00）

✅ 已完成
• MiMo Token Plan API 测试：API可用，mimo\-v2\.5为推理模型
• Python批量生成脚本（01\-05）：56个TTS素材 \+ 5篇知识库笔记 \+ 30篇绘本故事 \+ 20篇教案/小红书
• OpenCode\+MiMo 批量生成（07）：50个文件（10绘本\+10教案\+10英语\+20古诗）
• 内容推送到GitHub：commit ac9e08a → nonomil/childrens\-library
• 飞书调研报告整合：v2\.0合并版

🔄 进行中
• Markdown故事→HTML课件转换：OpenCode\+MiMo\-v2\.5批量生成中
• 绘本首页卡片更新：待HTML生成后更新docs/index\.md

📋 采用的技术方案（来自本报告推荐）
1\. 翻页引擎：Turn\.js（不换，当前够用）
2\. 分支叙事：Ink/inkjs（MIT授权，AI生成脚本最友好）
3\. TTS方案：Edge\-TTS（免费\+中文童声XiaoxiaoNeural）
4\. 内容生成：MiMo V2\.5（推理模型，批量文本生成）
5\. 开发工具：OpenCode → MiMo API（绕过CLI模型限制，直接调用）

⚡ 下一步
1\. 完成50个故事的HTML课件转换
2\. 更新docs/index\.md首页卡片
3\. 为HTML课件添加Edge\-TTS音频（旁白\+角色对话）
4\. 选择一个课件做Ink分支叙事Demo
5\. 组件生命周期契约实现（init→mount→unmount→resize→update）

进度执行：Hermes Agent（MiMo\-v2\.5）\| 日期：2026\-05\-28

