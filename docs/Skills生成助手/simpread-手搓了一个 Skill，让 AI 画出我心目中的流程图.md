> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/xeXeeauhZ4qvBqNkZVzDrQ)

最近一直在深度折腾各种 AI Agent 和辅助开发工具。看过无数篇介绍 Skill 的文章后，我终于忍不住动手了。

因为我深刻体会到一件事：想要真正理解一个技术概念，最好的办法永远是亲自下场。去建构、去试错，去看看这东西在你的真实工作流里，到底能翻出什么水花。

所以，我逼着自己手搓了一个 Skill。

这是一个专门用来 “画高颜值流程图” 的外挂技能。大家可以先看看最终的效果图。

关注公众号，回复 “流程图” 可以免费获取这个最终技能。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q0JUfCQ5x6WQEKYaiaQq0zwNjdpmSgxveagwgmjYJkWZ9q3vU8gic5t2YpLYAINxDEdYR0Obicr1icAMpsdxsl3XM08mEuBDd3BNcysvJSy5OUs/640?wx_fmt=png&from=appmsg#imgIndex=0)

  
流程图效果

为什么要专门做一个画流程图的 Skill？
---------------------

你看到这里可能奇怪：画流程图有什么稀奇的？

现在的大模型，直接在对话框里敲几句提示词，不就能出流程图了吗？

确实能画。大模型刚开始流行的时候，我确实试过一些常用的方法。

最简单的就是让 AI 生成 Mermaid 格式的代码，然后再导入到 excalidraw.com 这类软件中渲染成图。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q0JUfCQ5x6VkYhABibQl9XJULyhBOuWRR5Xg5tNGGL5ab51W8EbVwKpsoEAX1RBWWDXJiaySrdAUIdguFokY93dTsAB970lyQT0ej2N3icX23U/640?wx_fmt=png&from=appmsg#imgIndex=1)

  
Mermaid 流程图

如果你对美感毫无要求，只要能看懂就行，那这种方法确实足够了。

但我过不去心里那道坎。我之前写技术文章时，专门研究过流程图的配色和风格，也用 PPT 手工画过很多图。

因此，我一直希望能定制一种个人非常喜欢的视觉风格。

什么样的风格呢？我最近非常沉迷 Anthropic 官方技术博客里的配图，那种极简、克制又极具专业感的画风，简直长在了我的审美点上。

![](https://mmbiz.qpic.cn/mmbiz_png/q0JUfCQ5x6U3U99hjG5KZvAFUwC7EBib7GdN0DDQHK3IBe3Ccu2JfYtH1S5goXJZhYZR2Co2relC5vbEicV1K9l14ScFFbiaKsteZ6H4C6H8Cs/640?wx_fmt=png&from=appmsg#imgIndex=2)

  
Anthropic 官方配图

我就在想，能不能让 AI 直接给我生成这种级别的流程图？

基础模型还不够
-------

最开始，我盯上了 Draw.io。这是一款非常老牌且强大的画图软件，刚好他们官方最近也顺应潮流，推出了自己的 Skill，可以直接在 Claude Code 里通过对话生成 Draw.io 格式的图表。

`https://github.com/jgraph/drawio-mcp/tree/main/skill-cli/drawio`

满心欢喜地接入试了一下，结果有些遗憾：官方的这个技能能把图画出来，但在配色和整体气质上，跟 Anthropic 技术文章的精美配图还是有差距。

这也让我意识到一个问题：**基础模型并不是完全做不到，而是做得不够稳定、不够一致。**

而这种场景，恰恰就是最适合自己做 Skill 的地方。

它不是 “从零创造能力”，而是对已有能力进行定向增强。换句话说，这就是一种能力增强型 Skill。

第一次上手，我是怎么翻车的？
--------------

刚开始的时候，我其实信心满满。

脑子里有个大概的构思，就直接打开控制台对着 AI 一顿疯狂输出，想到哪说到哪，指望它能瞬间领悟我的意思。

结果呢？一个多小时痛苦地折腾下来，几十块钱的 Token 额度就像水一样烧没了，最后做出来的东西根本无法稳定工作。

这感觉，像极了凭空建一座没打地基的房子，一边盖一边改，最后 “轰” 地一下全塌了。

这次彻头彻尾的 “翻车”，一巴掌把我拍醒了：

创建一个好用的 Skill，从来就不是 “陪 AI 聊聊天、写几句提示词” 那么简单！

它本质上是一个极其严谨的软件工程。称之为 “Skill Engineering（技能工程化）” 毫不为过。

想做好 Skill，先拆解 “痛点”
------------------

痛定思痛，我开始用工程化的思维来拆解这盘棋。

第一步，解读核心痛点：我想要的 “Anthropic 风格”，到底是个什么东西？

为了搞清楚这个，我开始在 Draw.io 里纯手动复刻他们的配图，并且喂了几十张原图给 AI，让它帮我逆向分析。最后，我们提炼出了几条规律律：

首先是颜色体系。颜色的分配必须基于 “语义角色”，绝不能是为了好看而瞎填。

从中整理出了十套严格的配色方案，并且定下死规矩：一张图里的颜色绝对不能多，最多保留 2 到 3 种用来起强调作用的主题色。

![](https://mmbiz.qpic.cn/mmbiz_png/q0JUfCQ5x6VKPQ6Oy8UenjZe5SDrxibzlNibPP1WnqNfaWc2YoWelf0e2uiaGTvHNiaF4gQ89Pvg8m2oE9Uf9qHC8IGtXMicias2FzFelGicPyWBpk/640?wx_fmt=png&from=appmsg#imgIndex=3)

  
颜色规范

其次是整体风格。背景画布用什么灰度，层级关系怎么体现？

结论是，层级和重要性要靠排版、字体大小和留白间距来体现，而不是粗暴地用一堆亮瞎眼的颜色去堆砌。

把这些审美标准用机器能看懂的规则沉淀下来，才是我这次开发中最核心的护城河。

固定生成流程
------

标准定好了，接下来就是规范 AI 的工作流。

当用户输入一句 “帮我画个大模型请求流程” 时，AI 第一步该干嘛？

我给它加了一个前置动作：深度思考。

简单说，就是逼着 AI 在动笔画图之前，先用一段纯文本把整个流程图的骨架、逻辑、用什么图表类型，老老实实地在草稿纸上写一遍。

实践证明，加上这一步，AI 生成的成功率直线上升。

紧接着，为了避免模型每次都 “自由发挥”，我在和 ChatGPT 反复讨论之后，把常用图表类型收敛成了几个固定类别：`workflow`、`architecture`、`comparison`、`swimlane`、`venn`、`chart`。

这样一来，模型就不只是 “会选颜色”，而是真正能更稳定地 “画成这种技术文章配图”。

最后，让 AI 严格按照 Draw.io 能够识别的 XML 格式输出代码。

结合 draw.io 官方的 Skill，我们将带有特定样式的 XML 内容输出，并保存为 `.drawio` 文件即可。

用 skill-creator 搭 Skill 
------------------------

整体骨架搭完后，我用上了最新的 `skill-creator` 来辅助生成 Skill，并给它加上了 Evals 评测机制。

[把创建 Skill 当作一个工程来看待](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454611033&idx=1&sn=c482285e4a2e73f1a0cd9c276a8bedd8&scene=21#wechat_redirect)

Evals 是什么？你可以把它理解成给 AI 安排的一套自动化期末考试。

它自动生成几个画图需求，对比一下 “开启我写的 Skill” 和“不开启 Skill”画出来的差距。跑完 A/B 测试一看结果，开启专属技能后的出图质量简直是降维打击。

![](https://mmbiz.qpic.cn/mmbiz_png/q0JUfCQ5x6X59X8XW1w9a9bBF6fnhz8wIibjA8mlOvgDRRdkE37tzhMxiblf2qTAxXQFqd5OA01gkrpwsKwCRjXRjECDktl4oFLZMfdGFe6u8/640?wx_fmt=png&from=appmsg#imgIndex=4)

  
报告

经过这番折腾，我最终的技能文件目录长这样：

anthropic-diagram/ 

├── skill.md （主控大脑） 

├── references/ 

    ├── color-palette.md （视觉标准） 

    └── pattern-library.md （图表的布局规则）

真正有价值的部分，其实是后面的反复调试
-------------------

看着这整齐的代码结构，我以为大功告成了。

万万没想到，真正的磨难才刚刚开始。我算是彻彻底底领悟了那句 “不亲自上手，永远无法理解里面的门道”。

接下来的两天，就是陷入了无休止的 “生成、比对、找茬、修改” 的死循环。

看着生成的图，我开始一点点抠细节：

“连接线的箭头怎么是这种笨重的实心块？不行，去 skill.md 里改规则，必须用开放式的 V 形极简箭头！”

“线条太死板？而改成带柔和圆角的正交连接线。”

“容器里的字太小了，再去调字号参数！”

……

![](https://mmbiz.qpic.cn/sz_mmbiz_png/q0JUfCQ5x6U3YLTiclcoVvVK7JeVtTHYiaJNjKl4caez4OksiausCwISDyRCZtfHLZSHKsM1bpnoZMsAx9IdJb9uJPTJMM0IJ4mtZaNClyMovM/640?wx_fmt=png&from=appmsg#imgIndex=5)

每一次微调，都需要让 AI 重新生成一整坨庞大的 XML 代码，在软件中进行图片比对，没有办法自动进行。这就像以前写代码一行行 Debug 一样熬人。

由于每次测试都需要消耗大量的 Token 上下文，两天折腾下来，肉眼可见地烧掉了大概 100 多块人民币。

强烈建议大家在做这种开发时，能包月就包月，不然心在滴血。

最重要的不是模型，而是你自己的判断标准
-------------------

整个过程中，我越来越强烈地感受到一件事：**模型只是执行者，真正决定上限的，其实是你自己对细节的理解。**

什么样的箭头更合适？ 什么样的颜色更克制？ 什么样的间距更舒服？ 什么情况下该强调，什么情况下不该强调？

这些判断，AI 不会凭空替你建立。你必须自己先有标准，Skill 才能真正被打磨出来。

也正因为如此，我发现：**整个 Skill 里最有价值的部分，恰恰不是主流程，而是这些 “容易翻车的地方” 的积累。**

把模型在画图时最容易犯蠢、最容易逻辑卡壳的地方，一点点收集起来，写成了一条条预防规则，反向补充到了技能文件中。

在一个优秀的 Skill 里，这种针对特定场景的边界处理和经验之谈，才是含金量最高的地方。

![](https://mmbiz.qpic.cn/mmbiz_png/q0JUfCQ5x6UH1H6xU7lyzaa9tr4mliaCSClgvG2LZxkQ8qD66PNZhn8YC4ldiauqZQXFukvJCe4Gn0r6UqecpQ7Gd6S8yO5IN7L3Kzn7WewwE/640?wx_fmt=png&from=appmsg#imgIndex=6)

  
流程图展示

总结
--

回顾这次折腾经历，最大的感触是：

即使 AI 能帮你写代码、做执行，但想完成一个真正好用的产品，你不仅需要掌握 Claude Code 等工具的使用方法，**更重要的是你必须懂行，熟悉业务的整个 SOP 和核心关键点。**

每一个行业、每一个细分岗位，都有自己不外传的 SOP（标准作业程序）、黑话和潜规则。通用的大模型对这些一无所知。

而一个精心打磨的 Skill，就是把你大脑里的行业老兵经验，“强行注射” 注入进 AI 。

停下来想一想：你每天的工作中，有没有哪些让你觉得像机器人一样重复、每天要耗费 30 分钟以上的痛点？你有没有自己一套行之有效的 SOP？

如果有，不要犹豫，去尝试写你的第一个 Skill 吧。

在这个大模型时代，你个人最核心的数字资产，或许就将从这里开始积累。

---

最近文章列表：

[1]  [难怪 Skill 不好用？来看看 Google 总结的 5 种 Skill 设计模式](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454611001&idx=1&sn=20d26ac1546ccc18d68b73f3361016c6&scene=21#wechat_redirect)

[2] [智能体 Skill 入门教程（附下载地址）](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610990&idx=1&sn=8c1feb8161f60cfd0386fa3b84656430&scene=21#wechat_redirect)

[3] [两年踩坑，换来这条 AI 学习路径](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610978&idx=1&sn=cf27b49a588860ec838020c8ddd59cdf&scene=21#wechat_redirect)

[4] [Skill 到底是什么？跟 MCP 有什么区别？](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610951&idx=1&sn=86ee652cfcff4a75c3dc95e29b44d8da&scene=21#wechat_redirect)

[5] [AI 是怎么学会唠嗑的？系统提示词又是什么？](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610935&idx=1&sn=2a3686c3cba50cf4bb870b363faddf89&scene=21#wechat_redirect)

[6] [Claude 控诉中国 AI 组团 “偷家”？到底什么是 “大模型蒸馏”？](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610929&idx=1&sn=8e1149720ce7542220583f0da018436c&scene=21#wechat_redirect)

[7] [价值 3000 元的 AI 内部培训课，今天我把它 “开源” 了](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610924&idx=1&sn=09d10c3dffd5c79e3170095f9bd6635a&scene=21#wechat_redirect)

[8] [拆解 AI 的大脑，看懂谷歌 “弱智” 提示词](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610869&idx=1&sn=c592571fd2e8b31ec0880e89d24f5540&scene=21#wechat_redirect)

[9] [日均 30 万亿！拆解 AI 时代的 “计量单位” Token](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610850&idx=1&sn=e93b394541553a81b8a812607f62e07d&scene=21#wechat_redirect)

[10] [2 分钟讲透：为什么 AI 会胡说八道？（附避坑指南）](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610832&idx=1&sn=692459eb1117ae858b33cac6936e9100&scene=21#wechat_redirect)

[11] [AI 的回复怎么完美转 Word？只要看懂这个格式 Markdown，效率翻倍](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610762&idx=1&sn=59c4ce38e905c4be77b2b817def4bbf5&scene=21#wechat_redirect)

[12] [学习 AI 的最大障碍，不懂大模型背后的灵魂](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610744&idx=1&sn=899778117cbf0ebfeafd5d66a9a34ef0&scene=21#wechat_redirect)

[13] [Vibe Coding 提示词指南（内附编程提示词速查表）](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610692&idx=1&sn=cf4b17933f4f62a861e0157390c55ebb&scene=21#wechat_redirect)

[14] [为什么你的 AI 用得没别人好？AI 真正的核心不是提示词，而是逆向工程](https://mp.weixin.qq.com/s?__biz=MzI5NjA1MDQ4NA==&mid=2454610653&idx=1&sn=3bd8f8fdd17985d7099684c7e3a577f0&scene=21#wechat_redirect)