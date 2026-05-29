> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw)

上周发了给 Agent 用的 [superpowers 插件](https://mp.weixin.qq.com/s?__biz=MzIyMzA5NjEyMA==&mid=2647681025&idx=1&sn=442177fc00306f3ce79d7438f5adccbc&scene=21#wechat_redirect)那篇文章。

没想到反馈还不错，Skills 这块的信息差，比我想的还要大一些 = =

然后评论区里就有人问了，还是一个叫 tim 的朋友，问还有什么必装的 Skills。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXvrwDvFqs8Aukmh6w8ChzdZibCOueJCLiciaPnPdTE7LZkCehKdeicc0TqLDsPvJOmibdH3QZicepL7VBpOSTpGB1YuCavcVgjnXzqQ/640?wx_fmt=png&from=appmsg#imgIndex=0)

我寻思着，确实可以再出一期。

于是周末就盘了盘我觉得真的对大家有用的，就又肝了一篇。

也不搞什么大而全的几百个的推荐榜单，那个我觉得没有啥的意义，我自己就调了几个我真的常用的，而且觉得对大家都有用的。

真的，Skills 不是装的越多就越好，反而其实越精简越科学，效果才越好。

文章里推荐的这些 skills，你想安装，更是简单，直接把我这篇文章，复制粘贴给你的 Claude code、OpenClaw、Codex 等等就行，这些 Agent，也就能一口气帮你全部都装上了。

接下来，我们正式开始。

**一. Frontend Design**

大名鼎鼎的 Frontend Design Skills，在 Claude 的官方插件网站中，超过了 Superpowers，排名第一。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqV7u7Q8ECiagx1YmGJanWy0espRcRWyMP4F1SSdwVqg0pAd9NUicMiaO0a3jcXNACxBic27ZAZL4x8kEdpUS7eghVnwrnlbbeyPnLY/640?wx_fmt=png&from=appmsg#imgIndex=1)

链接：https://github.com/anthropics/skills/tree/main/skills/frontend-design

他的一个很有用的东西就是，解决绝大多数 AI 做前端的品味问题。

能力越差的模型，效果越好。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqVMhIMcK9EFtaCAMBNOzBnaPYaFVK6Ey0pq9ibUoJmfK6iaHN4ro9L8X3UiascIXzicTs7BEFcvPklo4W4rs9Ms8ziaaliabp0FoPdjE/640?wx_fmt=png&from=appmsg#imgIndex=2)

就是很多 AI 做的前端页面，真的，那个 AI 味浓郁的让人抠脚。

大家肯定都见过，千篇一律的 tailwindcss 蓝紫色渐变，系统默认字体，十个人生成十个网页，八个长一个样。

当然，这没办法，毕竟 AI 就是个统计学。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqUSsuvYRzrtgBrZHY5ypJKmIvOTcXuVicynSUIxadZeiaIjsYU6Hq7ibrdFcTiaI5ribiaKfN6JmR6eWOuU3pJV0aL4y2x5GSetMlMfY/640?wx_fmt=png&from=appmsg#imgIndex=3)

比如我直接让 Claude 直出一个我们公众号数据的可视化网页。

真的就是直出，不加任何 skill 和 Prompt，虽然已经比很多模型效果好多了，但是吧，这个 AI 味，还在有点浓。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/2jjfQoZLoqXtIte4MfNbeEjgNLEM2NrzZ1J1l3a6mLXl0wxzsEsibqwqicF45tl8jQV9rlQCYlrN8yAqxort8nFynfUkSGTXdx9KszQPW3ypk/640?wx_fmt=gif&from=appmsg#imgIndex=4)

我当然可以画一个原型图扔给它，或者用嘴说一段 UI 设计的 Prompt，但是不是 UI 设计师的人呢，就像我根本想象不到，音乐的 Prompt 怎么写一样，对于很多人来说，怎么去优化网页的审美，也是一个难事。

那这个时候，Frontend Design 来了，这个 Skills 出自 Anthropic 官方，有一说一，Anthropic 在促进 Skills 生态上，真的做了非常多的人事。

可以看一下他们的 SKILL.md，也就是 skill 的描述文档。

![](https://mmbiz.qpic.cn/mmbiz_jpg/2jjfQoZLoqU4xcTbTia6KK9v5XJfjM9UdQicLOkRz4c4TnSibn7icrU6hrQwpgH8m90pmeSNDtCrhIG4Q00cudzibpnevjcQa3bK9YzBeBXRTYKQ/640?wx_fmt=jpeg&from=appmsg#imgIndex=5)

里面的设计思路还挺有意思的。

它要求 AI 在写代码之前，先想清楚一个大胆的美学方向，极简主义、复古未来风、什么都行，然后所有的排版、留白比例、字体选择、动效，都要围绕这个方向来。

而且它有一些硬性规定，比如禁止使用 Inter、Roboto、Arial 这些烂大街的字体，禁止紫色渐变配白底的经典 AI 审美。

![](https://mmbiz.qpic.cn/sz_mmbiz_jpg/2jjfQoZLoqXK8XicjfDCooODOVj5VkV0CvppicClKr3eTBKZbd2gCGxeFOfdzveUXdagYae57NOZfFSPjBPJVu1u6Z1W46ucjib7FSnjz8nUSY/640?wx_fmt=jpeg&from=appmsg#imgIndex=6)

装上之后，同样的需求，出来的东西就完全不一样了。

还是我们公众号举例子。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqUDkvlXGjMDCYXLpBS8lvoAvwMF1FcsDye2GTnaM5BLyicdhJ1icyMyuJoNyw1kLbxS04Ul3a3uBpJSRY691BicaeonjndjTqfNnE/640?wx_fmt=png&from=appmsg#imgIndex=7)

这个排版一下子就舒服了好多。

![](https://mmbiz.qpic.cn/sz_mmbiz_gif/2jjfQoZLoqUXdY4KpAk8wjsrQS1EjESPRLcb9yRmtPiamTHfYN3nBmDGmOjR7WxVFWwgPic8GrpWUTkvgqg6pGADX9NXh5bTNia8zB5MuX13xo/640?wx_fmt=gif&from=appmsg#imgIndex=8)

如果你经常用 Agent 生成前端页面、做小工具的 UI 或者做数据可视化分析，相信我，这个，真的必装。

**二. 办公必备四件套**

没想到吧，第二个，其实是 4 个 Skills。。。

分别是，docx、xlsx、pdf、pptx。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqUABzTXcLzahOLJYYoYQ77qcAcl7R712DJn2wbzjrQQkMsiccWuEuCBjapMfbeevtC9mwpHy0t3viaFbcuB8p3eyXGJdazYzfBFE/640?wx_fmt=png&from=appmsg#imgIndex=9)

还是来自 Anthropic 官方的办公牛马必备四件套。

链接：https://github.com/anthropics/skills/tree/main/skills

有了它，你的 AI 就能读取你各种格式的文件了。

word、ppt、excel、PDF 全都能读，全都能写，全都能改。

如果你用的是 Cowork，这些能力是内置的，开箱即用。

但如果你是用终端的 Claude Code 或者小龙虾啥的，就需要自己装一下。

你可能会说，不对啊，我不装这几个 skills，不是也可以读 PDF，也能生成 Word 啊。

对的，确实可以，但是吧，你不装，那每次 Agent 处理这几个格式的文件的时候，都是自己现写代码，从零开始摸索怎么排版、怎么生成表格，运气好出来的还行，运气不好的时候，出来的真的就是一坨。

而且，能力越低的模型，效果越一坨。

而装上了这四件套 skills 之后呢，里面它自带了一整套文档处理流程和代码模板。

比如页面大小、宽度、需要的图片类型等等等等。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXG5bEnFhicgjGYibeSt3jV1ibESib7K78WcUiaTv2FYIuppbs4CianPKBEdop4ebJzN1A9L9icSWWZYtGF1ERNicLDicRG3sZiby46yyJg8/640?wx_fmt=png&from=appmsg#imgIndex=10)

相当于给它一本操作手册，它可以照着做就，就不用自己每次从零瞎在那搞了。

我来给大家实际对比一下装与不装的区别。

就拿 Kimi 最近发布的那篇比较热的论文《Attention Residuals》举个例子，21 页，全英文，密密麻麻的公式和图表。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXXCjoZD5MLjURuO9iaBUO2RvJx74P23WbMmyXEmC8aaCCtuobY9qoaYGpe8xpicr8Db8l3gpiaGCEIWzaQmTawaeSwJic5E486ibZ8/640?wx_fmt=png&from=appmsg#imgIndex=11)

我们用 Claude code 不调用任何 skills，帮我做一份中文笔记，把重点总结出来。

它做出来的东西是这样的。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqVMCeCmnicwFA0sRswqAngCRtnKkgJahFlaVCJHPicfDZvibAwJXficZHWJYkLBGL9iaKrLeHBel75SfhFMBEUaokQ1iazbdB8NFhqxk/640?wx_fmt=png&from=appmsg#imgIndex=12)

一坨，真就是一大坨。

而你装上了四件套的 Skills 之后，同样的需求，出来的是这样的。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqVNg137c5POzrib6vMINNUrT4jiajNwG9O0gJp2Msn7PvaPfv0ia4QAgJEjT5lhKXtThkskanjOQsicfibv0PYEDv0B6KdpRbwr3hRo/640?wx_fmt=png&from=appmsg#imgIndex=13)

全篇统一色调，页眉页脚都有，至少是个格式完整的、没有 BUG 的文档了，看起来就很专业。

你也完全可以，把你的自己的论文模板啥的扔给 Agent，再叠加这个 skill 一起用，效果出奇的好。

PPT 也是一样的道理。

没装的时候让它做 PPT，出来的东西就非常简单，毫无亮点。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqV6x1icqApicwQicMu76ZsSVZ2YUzUEKzy5VULicXSJWu5jc6JOg98rXuq7gI9y97QE76liayYwmtgkGjibTzHlnQlDWTXrBU9FL7o5Q/640?wx_fmt=png&from=appmsg#imgIndex=14)

装上之后，它就还能给你输出一个排版还不错的 PPT。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqWtXHo9KdYoJWVts7RT5mS6eyiaqGlAB2QF4gnUpnNTqOmcDqY055gNzzPCpbv646Y6rB3ObxjNlz4jGsF7Uywuft0qIgQUH52w/640?wx_fmt=png&from=appmsg#imgIndex=15)

而且如果你把上面说到的 Frontend Design 那个 skill 也装上，叠加一起组合用，那 PPT 的颜值还能再上一个台阶。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqVpzduwPEb2WhA8umFiadfUmoSCibIP4Sn0WZsukibIQTflgU1HIxHkWiaq4VdTHaAuJO0V1Qr43QYFDMEfzpO4MIQHXDBV8kPsiaP4/640?wx_fmt=png&from=appmsg#imgIndex=16)

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqWzWaJCyRA0niaYnicJAqJoEfbvtWdz59j6cq55QwVa4a44P5iaTc1waxS2zFSh019Hkd9AicuGibllneGRJDEElJcpZJX0RdJibW0kg/640?wx_fmt=png&from=appmsg#imgIndex=17)

相信我，这个四件套，真的是几乎每个人都用得上的 skills。

**三. Web Access Skill**

来自 @一泽开发的一个联网 Skill，非常好用。

名叫 Web Access skill。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqW1CpWm2ia9CRg4eHaU97XpLKh1PuMia3dY97PPdbNZjMibn5nWiaw56SfyJdyhPq5Ttribc9zbb2ss60Km4yVk0QYNdVMLbPgITpOw/640?wx_fmt=png&from=appmsg#imgIndex=18)

链接：https://github.com/eze-is/web-access

上周一刚发，已经有两千多的 star 了。

也是少有的，将联网搜索和浏览器操控结合到一起的 skill，也是我自己现在默认的联网 skill 了。

Claude code 本身自带的搜索工具，并不能够搜到非公开的站内信息，碰到小红书、B 站这种站内内容，基本搜不到什么有用的东西。

但装上这个 skill 之后，搜索能力就完全不一样了。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXFTEGN3t8037x0g9rTeicCf2QAWoaWiceGK4px9Of3pzEJXDY0F1H4dRkfA4qd516RCGSsLKQ3SGSo3Ck0UVic2I92HCbIuJ3gicU/640?wx_fmt=png&from=appmsg#imgIndex=19)

可以通过 Chrome DevTools Protocol 直接连你本地的 Chrome 进程，带着你的登录状态，所以其实你平时登录过的微博、小红书、B 站、飞书，它都能直接用，不需要重新登录。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXo5nPEoQJ4UC24rf7EB1b2SCRZdEb888heiaEBt9f50loT3SkvDXnlO8h5ZbTl61r1QhL8zYfJLjWceTibYTED2fZX3H3qSqLCI/640?wx_fmt=png&from=appmsg#imgIndex=20)

甚至贴心的出于节省 token 考虑，还选择了 Jina 作为一个可选中间层，可以和 WebFetch、Curl 组合使用，能把网页正文预先转成干净的 Markdown 再读，大幅节省 token 消耗。

设计的相当优雅。

不过有一个前提条件是需要 Chrome 更新到最新版。

并且还需要允许远程调试，可以在地址栏输入 chrome://inspect/[#remote](javascript:;)-debugging，进行勾选。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqWrWb1QGhQnPricqQAj3dOZrc1C5LrC7Nl8Ged8nBG8KE1stjZWiaa36uzAPD31H8Mia0JxxdomzuyVwgIqCaiacxRHNywZYty3c7c/640?wx_fmt=png&from=appmsg#imgIndex=21)

举个简单的例子，比如，我让他帮我从小红书上找望京附近的好吃的，最好还能配上图片。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXCBCtN9Sg5cU20xCTjDvndH3TgWT4IBVl74n3DoysIjWKAfiaGgXibIRmsGricpmdfkVSNE9YncyMSaj7deQVvKmFO2ichib7S6CwY/640?wx_fmt=png&from=appmsg#imgIndex=22)

它派出了一堆 Agent 去提取笔记内容。

对，是并行的，多个 Agent 各干各的，同时操作不同的浏览器标签页，互不干扰。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXWPNvcnSxOCzJtDiccgvOwsY7kyyadxERzyD0lTickk5uR2hiaLH73jiae8G1RJbYia9R0Bf59nUPOSMwqNS1Mqoup8Zkg0SILMIb0/640?wx_fmt=png&from=appmsg#imgIndex=23)

然后，就图文并茂的都整理出来了。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqV3hwmKIvZEicgswoI19MaH38Hn2wPYR7WvHeLBGs8ky0BhMxvJBaNxXsQBpatfFSbogAL6Zs8DWriarRBsQoEeAibVHdmhRzr87U/640?wx_fmt=png&from=appmsg#imgIndex=24)

读取公众号链接也没啥问题。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXIHyRktXUicR7rgtoZa9xCwLQ3tORVTiah0MjoByAY91RYSAiadjXtjaXF8qK7iakUVq6QjnggEF3v31DCG3Or7Sic0n0gIdWkQl8Q/640?wx_fmt=png&from=appmsg#imgIndex=25)

然后这个还有个很有意思的设计。

就是，它会自动沉淀每个网站的操作经验。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqUjauyX1DKUKR0Ha1I8egqJ1ibcOY2eyz8YZdohggibn7MticQd0gbQeiaqkRhA3OMJOlrE3lFjfXa7zrSicgQlkzeIBZQtbZWZgKTY/640?wx_fmt=png&from=appmsg#imgIndex=26)

它会自己在本地按域名存一份操作记录，哪些选择器好使、哪些路径走得通、哪些坑要避开，会全都记下来。

第一次访问可能慢一点，但之后再去同一个网站就快得多了，越用越顺，像是 Agent 自己在攒工作经验。

非常方便，目前也是我自己用下来，通用联网做的最好的 skill。

**四. PUA**

曾几何时，我以为这个 PUA Skill，是在搞抽象。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXa46kf8Tsib20s8NQo0yaWN3Qs3wJ2DzsVtNNfic0sj53BBIIcJXV7oWNc5CG85XjmRWww8ZhBG3qgicRfYy9icSyTlCLcpTg1Hsg/640?wx_fmt=png&from=appmsg#imgIndex=27)

直到我自己用了之后，真香。。。

链接：https://github.com/tanweai/pua

它的项目简介是这么写的。

你是一个曾经被寄予厚望的 P8 级工程师。Anthropic 当初给你定级的时候，对你的期望是很高的。

这味冲的梦回互联网厂子牛马生涯。。。

不过有一说一，这个 skill 解决的是一个很多人都体感过但不太好描述的问题，那就是 AI 摆烂。

你让它修个 bug，它试了两三次没搞定，就开始跟你说 “建议您手动检查一下”“这个问题可能需要更多上下文”。

翻译成人话就是，你大爷的我不想干了，你丫自己来吧。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXWy9oDslABVGHvW7dXpgWnSGicYIflpooKwZiaDbccIC9lO6FLg77BIFCyoTr7ROHXUH6VNd2ub0icWml3giaC0t0e61F9dazibBns/640?wx_fmt=png&from=appmsg#imgIndex=28)

PUA 这个 skill，就是专治这种摆烂的。

我其实不太建议开默认模式，在实在解决不了的时候，再手动 PUA 一下，可能会比较好。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXkibpvO7GK2MBG0RvibgTJvBGicpyXwCD3dyx9fE9thPlqibl3D46qMdNWjLtxNqd7NngF6E4hI0StkBFBIB9b4Q0KraVmnLYscFs/640?wx_fmt=png&from=appmsg#imgIndex=29)

当比如你的项目，改来改去实在改不好的时候，直接 / pua，开干。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqXibenO9Pib7GtUkTsY1ZppbRk3UllsGkbSRedW2GyPOnRQY2714mplWQz5G0fRia5Ezo9icUETyHV8GURYibIxqG9ziamicSQpsGsEicg/640?wx_fmt=png&from=appmsg#imgIndex=30)

然后它就会开始找原因了。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXLl3VCu4hiccib9bTUzNY580qm4ricv683aPFlXoCDC9YHNzDWhZgcutYhP0JFVoaicsHMLhumlqoVyx27kp3UHMpP3Pq3pWagU0I/640?wx_fmt=png&from=appmsg#imgIndex=31)

最后直接解决。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqUgc1gBamT7guibdoI6jibAQbjwLf4N7vA50FQJLpUW6icuXnfXzoyLlIzTOsNbibaoMM5ukqEHTeArPS8xcmmTNYBzBVZfdFFwOys/640?wx_fmt=png&from=appmsg#imgIndex=32)

它会有四级压力升级，如果 Agent 在同一个思路上原地打转，PUA 会强制打断它，让它执行一个 7 项检查清单，逼它换思路。

而它的 v3 版本更离谱了，会根据任务类型自动选方法论。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqWfbiaUMTugWrIoraAJWpPdZACJ0rnOr9Z20L6EnnECFfMibpyL8LBJhvzG38vwXibGJTeX4LWdwA6W80xuewhxibiapib0qzC9be1lg/640?wx_fmt=png&from=appmsg#imgIndex=33)

阿里、字节、华为、腾讯、美团、拼多多、百度、Netflix、Apple、X，十几家公司的方法论，全都给你塞进去了。

太残忍了，但太好用了。

真的，效果立竿见影。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqU33SuWbwV4ia4EfZ7hxicMZyY8BqKHdl7sZSXd31rPUxbzMUNRicPtHjEXeO97WgeA27waia7JtNFKqs5FnPVFmrpvbwHYZHibqwsY/640?wx_fmt=png&from=appmsg#imgIndex=34)

非常推荐大家装上，当你某一个 BUG 它死活改不明白的时候，直接开启 PUA 模式。

**五. Claude-mem**

很多人觉得，OpenClaw 比 Claude Code 越用越聪明，其实本质上就是记忆机制，OpenClaw 直接把 Memory 给封装了。

而 Claude Code 或者 Codex，一直都没这套东西。

所以咧，就有大佬专门做了个。

名字就叫 Claude-mem。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqVRDHaKBHrhm9THv6Szic4EKylZ2JGbmc9bQK2coPgdY0HXRvSo67bOHpZ4E2w41ibLpHiaqRhWcDe1dMicpldLONoEV7jw0Q7qSHg/640?wx_fmt=png&from=appmsg#imgIndex=35)

链接：https://github.com/thedotmack/claude-mem

解决的就是记忆持久化问题。

![](https://mmbiz.qpic.cn/mmbiz_jpg/2jjfQoZLoqUnpycuA93TzKbhqYRUIvSIQmHfT7tgibuL0GWj0LRpleu7LnKbTECAgG8bPJcx6z1csmia0InZFWHYbcJRzwBIT3TjymXp2nNiaU/640?wx_fmt=jpeg&from=appmsg#imgIndex=36)

它会自动记录你每次对话里的关键信息，压缩存下来，下次开新会话的时候自动注入相关的上下文。

非常简单的说就是，给你的 Claude Code 装了一个类似于小龙虾那样的长期记忆。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqX6QkOg9SricD83zwIFcmYyD4y2xX9obtgicNztSgKIP1wQOqKLMJecwRo7FntAyraz12WUnDc96JLbcFywZp5rBq8MGtn2zYgEo/640?wx_fmt=png&from=appmsg#imgIndex=37)

用的也是渐进式呈现的方案，也就是三层检索的机制，先拉一个索引，大概看看有没有相关的内容，有的话再看时间线上下文，最后才把完整的细节拿出来，这样基本上是标配了，因为省 Token。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXAnnSAe1FtAXBctmBJg057Knf98NRp2V5pSJxLKUuUl06ib9tdGN8VicwRibzkVHOicpsGgIT1cfSynqOYDWibgM8iah4ia3oZQ7icAB4/640?wx_fmt=png&from=appmsg#imgIndex=38)

它也自带了一个本地的 Web 界面，跑在 localhost:37777，你可以直接在浏览器里看它到底记住了什么、什么时候记的，非常的一目了然。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqXTjYPyhGXupYPHVK31wrS4PHrBGBZibZHYhTbowU2p5BO6gLPtuFnOxyeNTv3suGMfNeHMOaE7dicgiaghm920o2P85SIfpIz0Ck/640?wx_fmt=png&from=appmsg#imgIndex=39)

还有一个隐私控制的设计，如果你有些内容不想被记住，比如你的密码、密钥这种隐私数据，加个 <private> 标签就行，它会自动跳过。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqVIoY6ErsyQkAiaLHd6R4dRPkgCc6qHt5x6znISrDWysQ3MmF9Q8ddFMWtPYFSzbDNZaGgTxoSuO0V0Re7hSv2g5OvgM3yYTN48/640?wx_fmt=png&from=appmsg#imgIndex=40)

就像这样，<private> 内容 </private>。

不过坦率的讲，这种写法我自己是真的很少很少用，因为我觉得这样写真的很呆逼。。。

**六. Skill-Creator**

这是我认为最重要的 Skill，没有之一。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqUnlMX4jFDnMMVTU6BKxgyfId4fhkzbrmeOT4Eqia3bkVyvbZibTKmZSY4DSgSe1uLxPLZwKDwvrkv5REoSYPmdxxKu8MfHu3kNs/640?wx_fmt=png&from=appmsg#imgIndex=41)

链接：https://claude.com/plugins/skill-creator

我也特意写过文章来介绍它：

[Claude 悄悄更新了 Skills 生成器，这绝对是一次史诗级升级。](https://mp.weixin.qq.com/s?__biz=MzIyMzA5NjEyMA==&mid=2647680550&idx=1&sn=61057f16c042c8ffda4e6e2ebee0def6&scene=21#wechat_redirect)

我就不过多赘述了，一句话总结，帮你自己构建一切属于你自己 Skills 的 Skill。

之所以把这个最重要的放在最后一个，是因为，我一直觉得，Skill 的真正的正确用法，是把你自己的需求和经验，封装、沉淀成 Skills。

只有属于你自己的 Skills，才是那个真正的、必装的 Skill。

就像，我不是开发，但是我自己有一个服务器，是给我自己部署用的，我根本管理不明白服务器，就把整个服务器的管理权限，直接搓成了一个 Skill，让 Agent 来替我管。

而前几天，因为公司同事 Vibe Coding 越发炉火纯青，也有了很多把开发好的项目部署在服务器上的需求，大家都是自己租服务器用的，我就想着，那不如把我自己的服务器升级一下，然后搞一下权限管理，让大家一起用，这样就都能省点钱，还方便。

于是，又花了十几分钟时间，就搞定了。。。

![](https://mmbiz.qpic.cn/mmbiz_png/2jjfQoZLoqW6Buc9jnvrvkxRT3axwqvQIPDHdsFsdNgG4N6BCgUfYiaia8FW9KCCITnbtqqDbvWREmnHQW943uZyxKTIfMDcQQDA1qlI80b28/640?wx_fmt=png&from=appmsg#imgIndex=42)

同事拿到手，流程是这样的。

![](https://mmbiz.qpic.cn/sz_mmbiz_png/2jjfQoZLoqWdjqXICPYzcUyiahiaGKRRLf6CHxNSfOcObdzia4cGdHNslcia28tx6C4aH0iaBwxLwXLKjOo3vpacPTnibIbg2GPVR6bJ3QXwPfHys/640?wx_fmt=png&from=appmsg#imgIndex=43)

现在这个服务器管理 Skill，就是我们的必装 Skill，真的，要不然一群人，真的搞不明白服务器运维，而且我们都是非常个人化的小项目，搞得很复杂也没必要。

现在回头看，我上面推荐的五个 skill，Frontend Design、四件套、Web Access、PUA、Claude-Mem，它们再好用，解决的都是通用问题。

但，很多的需求，没有任何一个 GitHub 仓库会为你解决你自己的个性化问题。

只有你自己可以。

所以我把 Skill Creator 放在最后一个，不是因为它最不重要，恰恰相反。

它是唯一一个，能让你从 Skill 的消费者，变成 Skill 的创造者的东西。

前面五个 skill，是别人替你想好的答案。

Skill Creator，是让你自己拥有创造的能力。

**写在最后**

以前我们说一个人有技能，说的是他身上长着的东西。

一个产品对数据的洞察，一个设计师的审美，一个程序员的 debug 直觉。这些东西可能学十年才能有，而且带不走，只能长在这个人身上。

但现在，技能可以被封装成一个文件，可以被安装，可以被分享，可以被复制。

这听起来好像技能在贬值。

但我觉得，其实不是。

真正贬值的，是那些通用技能。

比如怎么排版一个 Word 文档，怎么写一段前端代码，怎么搜索一个网页。这些东西，skill 已经替你做了。

而真正升值的，是你知道自己需要什么的那个能力。

你知道你们公司的服务器管理流程应该长什么样，你知道你的文章风格里哪些是灵魂哪些是皮毛，你知道你的工作流里哪个环节最痛、最值得自动化。

这些判断，AI 做不了。

因为它不是你。

所以说真的，今天推荐的这六个 skill，你全装上也好，挑几个装也好，都行。

但如果你只记住一件事，我希望是这个，

最牛逼的 skill，永远是下一个，你自己造的那个。

******以上，既然看到这里了，如果觉得不错，随手点个赞、在看、转发三连吧，如果想第一时间收到推送，也可以给我个星标⭐～谢谢你看我的文章，我们，下次再见。******

>/ 作者：卡兹克、可达

>/ 投稿或爆料，请联系邮箱：wzglyay@virxact.com