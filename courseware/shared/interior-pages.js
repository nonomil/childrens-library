(function() {
  var INTERIOR_PAGES = {
    stories: {
      title: '绘本故事屋',
      kicker: 'Story House',
      subtitle: '左右滑动卡片墙，选一本故事就能直接开始阅读。',
      background: 'assets/interiors/stories-house.png',
      toolbar: {
        icon: '📚',
        label: 'Story House',
        title: '今日故事台',
        hint: '先选一本，再沿着书墙继续逛。',
        status: '建议先开《好饿的小蛇》，再顺着冒险和海底主题往下滑。',
        actions: [
          { icon: '▶️', label: '马上开读', note: '好饿的小蛇', zone: 'stories', file: 'story-hungry-snake.html' },
          { icon: '🌟', label: '冒险精选', note: '定位星球大战', action: 'focus', zone: 'stories', file: 'story-star-wars.html' },
          { icon: '🌊', label: '海底主题', note: '定位海底大冒险', action: 'focus', zone: 'stories', file: 'story-ocean-adventure.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: '今日主推',
        title: '好饿的小蛇',
        desc: '从一口一口的节奏里认识水果和故事推进。',
        note: '先读这本，再往右滑到星球大战和海底大冒险。'
      },
      hotspots: [
        { zone: 'stories', file: 'story-hungry-snake.html', title: '好饿的小蛇', x: 18, y: 21.5, w: 15, h: 21.5 },
        { zone: 'stories', file: 'story-brave-pea-shooter.html', title: '勇敢的豌豆射手', x: 35.6, y: 21.5, w: 15, h: 21.5 },
        { zone: 'stories', file: 'story-star-wars.html', title: '星球大战', x: 53.2, y: 21.5, w: 15, h: 21.5 },
        { zone: 'stories', file: 'story-ocean-adventure.html', title: '海底大冒险', x: 70.8, y: 21.5, w: 15, h: 21.5 }
      ],
      secondaryHotspots: [
        { href: 'stories-index.html', title: '故事索引', x: 2.2, y: 30.2, w: 12.2, h: 22.4 },
        { zone: 'stories', file: 'story-block-battle.html', title: '创意想象', x: 84.2, y: 34.8, w: 11.6, h: 25.5 }
      ],
      quickLinks: [
        { label: '故事索引', href: 'stories-index.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { zone: 'stories', file: 'story-hungry-snake.html', title: '好饿的小蛇', desc: '从一口一口的节奏里认识水果和故事推进。', emoji: '🐍', chip: '绘本故事', duration: '8分钟', color: 'linear-gradient(135deg,#ffe8a3,#ffb55a)' },
        { zone: 'stories', file: 'story-brave-pea-shooter.html', title: '勇敢的豌豆射手', desc: '跟着冒险主角体验守护与合作。', emoji: '🌱', chip: '热门', duration: '8分钟', color: 'linear-gradient(135deg,#d9f5c4,#79d37c)' },
        { zone: 'stories', file: 'story-block-battle.html', title: '方块大战', desc: '方块角色的冲突与策略，节奏很带感。', emoji: '⚔️', chip: '动作故事', duration: '10分钟', color: 'linear-gradient(135deg,#d7e7ff,#7cb0ff)' },
        { zone: 'stories', file: 'story-star-wars.html', title: '星球大战', desc: '星际主题的大场面故事，适合沉浸阅读。', emoji: '🌟', chip: '太空冒险', duration: '10分钟', color: 'linear-gradient(135deg,#d8d4ff,#8378ff)' },
        { zone: 'stories', file: 'story-robot-battle.html', title: '家务机器人大战', desc: '机器人碰撞出幽默剧情，也藏着生活想象。', emoji: '🤖', chip: '脑洞篇', duration: '10分钟', color: 'linear-gradient(135deg,#d8f6ff,#75d9f5)' },
        { zone: 'stories', file: 'story-ocean-adventure.html', title: '海底大冒险', desc: '下潜到海底世界，和新朋友一起闯关。', emoji: '🐙', chip: '海洋主题', duration: '10分钟', color: 'linear-gradient(135deg,#c6f1ff,#65c8f4)' },
        { zone: 'stories', file: 'story-space-d1.html', title: '太空冒险·飞行平台', desc: '轻科幻故事，画面和节奏都很有探索感。', emoji: '🚀', chip: '太空系列', duration: '10分钟', color: 'linear-gradient(135deg,#d6ddff,#7f90ff)' },
        { zone: 'stories', file: 'story-brave-tank.html', title: '勇敢的小坦克', desc: '小坦克一路升级打怪，很适合男孩向故事阅读。', emoji: '🛡️', chip: '冒险篇', duration: '10分钟', color: 'linear-gradient(135deg,#d8f0d1,#88c866)' }
      ]
    },
    science: {
      title: '自然探索实验室',
      kicker: 'Science Lab',
      subtitle: '把自然、机械和英语启蒙混在一起，像逛展一样向右浏览。',
      background: 'assets/interiors/science-house.png',
      toolbar: {
        icon: '🔬',
        label: 'Science Lab',
        title: '实验控制带',
        hint: '机械、自然、观察主题都能从这里快进。',
        status: '先做齿轮传动，再切到雨林和昆虫观察，最后补上苹果和英语彩蛋。',
        actions: [
          { icon: '⚙️', label: '机械实验', note: '直达齿轮传动', zone: 'science', file: 'gears-transmission.html' },
          { icon: '🌴', label: '雨林探索', note: '定位雨林大冒险', action: 'focus', zone: 'science', file: 'rainforest-adventure.html' },
          { icon: '🦋', label: '昆虫观察', note: '定位自然课', action: 'focus', zone: 'science', file: 'nature-lesson-4.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: '观察焦点',
        title: '齿轮传动',
        desc: '观察机械如何带动彼此，适合做启蒙小实验。',
        note: '做完机械实验，再切到雨林和昆虫主题。'
      },
      hotspots: [
        { zone: 'science', file: 'gears-transmission.html', title: '齿轮传动', x: 15.8, y: 23, w: 14, h: 18.5 },
        { zone: 'science', file: 'rainforest-adventure.html', title: '雨林大冒险', x: 32.4, y: 23, w: 14, h: 18.5 },
        { zone: 'science', file: 'nature-lesson-4.html', title: '昆虫观察', x: 49, y: 23, w: 14, h: 18.5 },
        { zone: 'science', file: 'i-am-an-apple.html', title: '我是一只苹果', x: 65.6, y: 23, w: 14, h: 18.5 }
      ],
      secondaryHotspots: [
        { zone: 'science', file: 'gears-transmission.html', title: '探索记录', x: 1.8, y: 34, w: 14.6, h: 26.6 },
        { zone: 'science', file: 'nature-lesson-4.html', title: '今日任务', x: 82.4, y: 34.6, w: 14.2, h: 28.5 }
      ],
      quickLinks: [
        { label: '自然探索', href: 'science/gears-transmission.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { zone: 'science', file: 'gears-transmission.html', title: '齿轮传动', desc: '观察机械如何带动彼此，适合做启蒙小实验。', emoji: '⚙️', chip: '机械', duration: '15分钟', color: 'linear-gradient(135deg,#e8dcff,#b58cff)' },
        { zone: 'science', file: 'rainforest-adventure.html', title: '雨林大冒险', desc: '进入热带雨林场景，认识自然生态。', emoji: '🌴', chip: '自然', duration: '15分钟', color: 'linear-gradient(135deg,#d7f5d8,#7dd47d)' },
        { zone: 'science', file: 'nature-lesson-4.html', title: '自然课·昆虫观察', desc: '在观察和提问里建立科学好奇心。', emoji: '🦋', chip: '观察', duration: '12分钟', color: 'linear-gradient(135deg,#daf7d5,#8cd670)' },
        { zone: 'science', file: 'i-am-an-apple.html', title: '我是一只苹果', desc: '从食物生长过程理解自然循环。', emoji: '🍎', chip: '植物', duration: '10分钟', color: 'linear-gradient(135deg,#ffe0d5,#ff8a65)' },
        { zone: 'science', file: 'phonics-fat-cat.html', title: '胖猫自然拼读', desc: '把科学屋里的趣味阅读也接进来。', emoji: '🐱', chip: '趣味读物', duration: '10分钟', color: 'linear-gradient(135deg,#ffe1ef,#f48fb1)' },
        { zone: 'science', file: 'sight-word-tales-can-we-get-a-pet.html', title: '我们可以养宠物吗', desc: '围绕动物与照顾主题做轻阅读。', emoji: '🐶', chip: '动物主题', duration: '10分钟', color: 'linear-gradient(135deg,#fff0c7,#ffcb63)' },
        { zone: 'science', file: 'sight-word-tales-come-to-the-party.html', title: '来参加派对吧', desc: '场景阅读更轻松，适合过渡到英语内容。', emoji: '🎉', chip: '场景阅读', duration: '10分钟', color: 'linear-gradient(135deg,#ffe0ba,#ff9f68)' },
        { zone: 'science', file: 'elephant-piggie-surprise.html', title: '大象小猪惊喜日', desc: '故事味更足的一节，适合作为实验室彩蛋。', emoji: '🐘', chip: '彩蛋故事', duration: '10分钟', color: 'linear-gradient(135deg,#fde1ef,#e9a4cb)' }
      ]
    },
    chinese: {
      title: '语文学堂',
      kicker: 'Chinese Class',
      subtitle: '识字、拼音、阅读都排成了一面卡片墙，想学哪张就点哪张。',
      background: 'assets/interiors/chinese-house.png',
      toolbar: {
        icon: '🀄',
        label: 'Chinese Class',
        title: '语文学习台',
        hint: '先起步，再从卡片墙里挑今天的主练习。',
        status: '先从汉字和拼音起步，再往阅读和古诗顺着滑过去。',
        actions: [
          { icon: '🔤', label: '拼音起步', note: '直达第7课', zone: 'chinese', file: 'chinese-07-pinyin.html' },
          { icon: '📖', label: '识字练习', note: '定位汉字课', action: 'focus', zone: 'chinese', file: 'chinese-01-characters.html' },
          { icon: '📚', label: '阅读进阶', note: '定位阅读课', action: 'focus', zone: 'chinese', file: 'chinese-20-reading.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: '拼音起步',
        title: '第7课 拼音',
        desc: '正式进入拼音世界，适合做系统启蒙。',
        note: '先把拼音打底，再顺着去看汉字和阅读。'
      },
      hotspots: [
        { zone: 'chinese', file: 'chinese-01-characters.html', title: '汉字', x: 15.8, y: 24, w: 14.5, h: 18.3 },
        { zone: 'chinese', file: 'chinese-07-pinyin.html', title: '拼音', x: 33.1, y: 24, w: 14.5, h: 18.3 },
        { zone: 'chinese', file: 'chinese-18-animals.html', title: '动物', x: 50.4, y: 24, w: 14.5, h: 18.3 },
        { zone: 'chinese', file: 'chinese-20-reading.html', title: '阅读', x: 67.7, y: 24, w: 14.5, h: 18.3 }
      ],
      secondaryHotspots: [
        { zone: 'chinese', file: 'chinese-01-characters.html', title: '读万卷书', x: 1.4, y: 31, w: 12.4, h: 34.2 },
        { zone: 'chinese', file: 'chinese-20-reading.html', title: '行万里路', x: 86, y: 31, w: 12.4, h: 34.2 }
      ],
      quickLinks: [
        { label: '拼音起步', href: 'chinese/chinese-07-pinyin.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { zone: 'chinese', file: 'chinese-01-characters.html', title: '第1课 汉字', desc: '从最基础的字形和字义开始认识汉字。', emoji: '📖', chip: '识字', duration: '10分钟', color: 'linear-gradient(135deg,#ffe2db,#ff9776)' },
        { zone: 'chinese', file: 'chinese-02-strokes.html', title: '第2课 笔画', desc: '跟着笔顺练基本功，后面识字会更轻松。', emoji: '✒️', chip: '基础', duration: '12分钟', color: 'linear-gradient(135deg,#ffdfe7,#ff9cb7)' },
        { zone: 'chinese', file: 'chinese-07-pinyin.html', title: '第7课 拼音', desc: '正式进入拼音世界，适合做系统启蒙。', emoji: '🔤', chip: '拼音', duration: '12分钟', color: 'linear-gradient(135deg,#eadfff,#b68fff)' },
        { zone: 'chinese', file: 'chinese-08-pinyin2.html', title: '第8课 拼音2', desc: '继续巩固发音和拼读感。', emoji: '🗣️', chip: '进阶', duration: '12分钟', color: 'linear-gradient(135deg,#ece1ff,#b892ff)' },
        { zone: 'chinese', file: 'chinese-12-yunmu.html', title: '第12课 韵母', desc: '把拼读的关键部分单独拿出来练一练。', emoji: '🎵', chip: '发音', duration: '12分钟', color: 'linear-gradient(135deg,#f4deff,#c885ff)' },
        { zone: 'chinese', file: 'chinese-18-animals.html', title: '第18课 动物', desc: '在熟悉的动物主题里练字词和阅读。', emoji: '🐾', chip: '主题课', duration: '10分钟', color: 'linear-gradient(135deg,#dff6db,#9ad67c)' },
        { zone: 'chinese', file: 'chinese-20-reading.html', title: '第20课 阅读', desc: '从识字走向完整阅读，节奏更像小故事。', emoji: '📚', chip: '阅读', duration: '12分钟', color: 'linear-gradient(135deg,#ffe4c9,#ffb276)' },
        { zone: 'chinese', file: 'chinese-23-poems.html', title: '第23课 古诗', desc: '进入带节奏和韵律感的中文审美。', emoji: '📜', chip: '古诗', duration: '12分钟', color: 'linear-gradient(135deg,#ffe6d7,#ff9f70)' }
      ]
    },
    math: {
      title: '数学学堂',
      kicker: 'Math House',
      subtitle: '从数数到应用题，整排卡片可以左右滑，做题路线更清楚。',
      background: 'assets/interiors/math-house.png',
      toolbar: {
        icon: '🧮',
        label: 'Math House',
        title: '数学出题台',
        hint: '数字、运算、图形可以直接从底部切换。',
        status: '先数数，再进加减法，最后把图形和应用题接起来。',
        actions: [
          { icon: '🔢', label: '数字起步', note: '直达第1课', zone: 'math', file: 'math-01-counting.html' },
          { icon: '➕', label: '加法练习', note: '定位加法课', action: 'focus', zone: 'math', file: 'math-04-addition.html' },
          { icon: '🔷', label: '图形观察', note: '定位图形课', action: 'focus', zone: 'math', file: 'math-10-shapes.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: '运算主线',
        title: '第4课 加法',
        desc: '进入真正的运算启蒙，适合配合实物数。',
        note: '先把加法打稳，再回头看图形和应用题。'
      },
      hotspots: [
        { zone: 'math', file: 'math-01-counting.html', title: '数数', x: 16, y: 24, w: 14.4, h: 18.2 },
        { zone: 'math', file: 'math-04-addition.html', title: '加法', x: 33.2, y: 24, w: 14.4, h: 18.2 },
        { zone: 'math', file: 'math-10-shapes.html', title: '图形', x: 50.4, y: 24, w: 14.4, h: 18.2 },
        { zone: 'math', file: 'math-23-word-problems.html', title: '应用题', x: 67.6, y: 24, w: 14.4, h: 18.2 }
      ],
      secondaryHotspots: [
        { zone: 'math', file: 'math-04-addition.html', title: '加号入口', x: 4.6, y: 5.4, w: 10.2, h: 14.4 },
        { zone: 'math', file: 'math-06-subtraction5.html', title: '减号入口', x: 4.2, y: 17.2, w: 10.4, h: 13.2 },
        { zone: 'math', file: 'math-10-shapes.html', title: '乘号入口', x: 82, y: 5.4, w: 10.4, h: 14.4 },
        { zone: 'math', file: 'math-23-word-problems.html', title: '除号入口', x: 81.8, y: 17.2, w: 10.6, h: 13.2 }
      ],
      quickLinks: [
        { label: '数字起步', href: 'math/math-01-counting.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { zone: 'math', file: 'math-01-counting.html', title: '第1课 数数', desc: '先把数字感建立起来，再进加减法会很顺。', emoji: '🔢', chip: '数字', duration: '10分钟', color: 'linear-gradient(135deg,#e0efff,#85baff)' },
        { zone: 'math', file: 'math-03-compare.html', title: '第3课 比较', desc: '大小、多少、长短这些概念都在这里。', emoji: '⚖️', chip: '比较', duration: '10分钟', color: 'linear-gradient(135deg,#d9ebff,#7db8ff)' },
        { zone: 'math', file: 'math-04-addition.html', title: '第4课 加法', desc: '进入真正的运算启蒙，适合配合实物数。', emoji: '➕', chip: '运算', duration: '12分钟', color: 'linear-gradient(135deg,#e1f8d9,#8fd67d)' },
        { zone: 'math', file: 'math-06-subtraction5.html', title: '第6课 减法5', desc: '从小范围减法开始建立减法直觉。', emoji: '➖', chip: '减法', duration: '12分钟', color: 'linear-gradient(135deg,#ffe4d7,#ffab7d)' },
        { zone: 'math', file: 'math-10-shapes.html', title: '第10课 图形', desc: '把生活里的形状都变成可识别的数学对象。', emoji: '🔷', chip: '图形', duration: '10分钟', color: 'linear-gradient(135deg,#eee0ff,#c195ff)' },
        { zone: 'math', file: 'math-15-money.html', title: '第15课 钱', desc: '把数学搬进真实生活场景，更容易理解。', emoji: '💰', chip: '生活数学', duration: '12分钟', color: 'linear-gradient(135deg,#fff1ca,#ffcf68)' },
        { zone: 'math', file: 'math-16-clock.html', title: '第16课 时钟', desc: '时间概念是幼小衔接里很实用的一块。', emoji: '🕐', chip: '时间', duration: '10分钟', color: 'linear-gradient(135deg,#dfeeff,#8ab9ff)' },
        { zone: 'math', file: 'math-23-word-problems.html', title: '第23课 应用题', desc: '把前面学过的能力串起来做综合练习。', emoji: '📝', chip: '综合', duration: '15分钟', color: 'linear-gradient(135deg,#ffe4ba,#ffb16b)' }
      ]
    },
    pets: {
      title: '萌宠小屋',
      kicker: 'Pet House',
      subtitle: '这里先放一面可以滑动的宠物卡片墙，挑一个主题就继续往里玩。',
      background: 'assets/interiors/pets-house.png',
      toolbar: {
        icon: '🐾',
        label: 'Pet House',
        title: '萌宠照看台',
        hint: '主入口、收藏馆和跨主题内容都压在这里。',
        status: '先去宠物中心，再补收藏馆和动物英语，右侧还有几处彩蛋可以点。',
        actions: [
          { icon: '🐶', label: '宠物中心', note: '进入主入口', href: 'pet-hub.html' },
          { icon: '🧸', label: '收藏馆', note: '去看图鉴', href: 'collection-hub.html', tone: 'soft' },
          { icon: '🦊', label: '动物英语', note: '定位 Animals', action: 'focus', zone: 'english', file: 'english-07-animals.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: '主入口',
        title: '宠物中心',
        desc: '照顾、互动、升级都从这里进入。',
        note: '先开主入口，再去收藏馆和动物英语。'
      },
      hotspots: [
        { href: 'pet-hub.html', title: '宠物中心', x: 16, y: 22.5, w: 13.5, h: 17.4 },
        { href: 'collection-hub.html', title: '宠物收藏馆', x: 32.2, y: 22.5, w: 13.5, h: 17.4 },
        { zone: 'english', file: 'english-07-animals.html', title: 'Animals', x: 48.4, y: 22.5, w: 13.5, h: 17.4 },
        { zone: 'science', file: 'sight-word-tales-can-we-get-a-pet.html', title: '养宠物吗', x: 64.6, y: 22.5, w: 13.5, h: 17.4 }
      ],
      secondaryHotspots: [
        { href: 'pet-hub.html', title: '宠物档案', x: 1.8, y: 29, w: 14.2, h: 27 },
        { href: 'collection-hub.html', title: '爱心小贴士', x: 80.5, y: 34.4, w: 15.2, h: 27.2 }
      ],
      quickLinks: [
        { label: '宠物中心', href: 'pet-hub.html' },
        { label: '收藏馆', href: 'collection-hub.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { href: 'pet-hub.html', title: '宠物中心', desc: '照顾、互动、升级都从这里进入。', emoji: '🐾', chip: '主入口', duration: '正在营业', color: 'linear-gradient(135deg,#ffe4cc,#ffb074)' },
        { href: 'collection-hub.html', title: '宠物收藏馆', desc: '看看已经收集到的小伙伴和图鉴。', emoji: '🧸', chip: '图鉴', duration: '随时查看', color: 'linear-gradient(135deg,#ffe1f0,#f6a0c6)' },
        { zone: 'english', file: 'english-07-animals.html', title: 'Animals 动物', desc: '顺手接进英语动物主题，学玩连起来。', emoji: '🦊', chip: '英语', duration: '12分钟', color: 'linear-gradient(135deg,#dff6db,#97d37a)' },
        { zone: 'science', file: 'sight-word-tales-can-we-get-a-pet.html', title: '我们可以养宠物吗', desc: '围绕养宠物展开的趣味阅读。', emoji: '🐶', chip: '阅读', duration: '10分钟', color: 'linear-gradient(135deg,#fff2c9,#ffd46a)' },
        { zone: 'stories', file: 'story-hungry-snake.html', title: '好饿的小蛇', desc: '把小动物故事也接进萌宠小屋的氛围里。', emoji: '🐍', chip: '故事', duration: '8分钟', color: 'linear-gradient(135deg,#ffe7a8,#ffbf6b)' },
        { zone: 'science', file: 'elephant-piggie-surprise.html', title: '大象小猪惊喜日', desc: '朋友主题的小故事，适合轻松切换。', emoji: '🐘', chip: '伙伴', duration: '10分钟', color: 'linear-gradient(135deg,#fee0ee,#e5a7ca)' }
      ]
    },
    english: {
      title: 'ABC 英语之家',
      kicker: 'English House',
      subtitle: '把英语课件排成可滑动卡片墙，孩子一眼就能看到今天学什么。',
      background: 'assets/interiors/english-house.png',
      toolbar: {
        icon: '🔤',
        label: 'English House',
        title: '英语启动台',
        hint: '字母、动物、场景主题可以直接点开或定位。',
        status: '先从 ABC 起步，再补动物、颜色和生日场景，整条卡墙都能横向滑。',
        actions: [
          { icon: '🅰️', label: 'ABC 起步', note: '直达 Lesson 2', zone: 'english', file: 'english-02-abc.html' },
          { icon: '🐾', label: '动物词汇', note: '定位 Animals', action: 'focus', zone: 'english', file: 'english-07-animals.html' },
          { icon: '🎂', label: '生日场景', note: '定位 Birthday', action: 'focus', zone: 'english', file: 'english-21-birthday.html' },
          { icon: '🏘️', label: '回到村庄', note: '切回总地图', href: 'village.html', tone: 'ghost' }
        ]
      },
      featured: {
        badge: 'ABC 起步',
        title: 'Lesson 2 ABC',
        desc: '最核心的字母课，适合作为起步入口。',
        note: '先学字母，再补动物和生日场景。'
      },
      hotspots: [
        { zone: 'english', file: 'english-02-abc.html', title: 'ABC', x: 16, y: 24, w: 14.4, h: 18.2 },
        { zone: 'english', file: 'english-07-animals.html', title: 'Animals', x: 33.2, y: 24, w: 14.4, h: 18.2 },
        { zone: 'english', file: 'english-09-food.html', title: 'Food', x: 50.4, y: 24, w: 14.4, h: 18.2 },
        { zone: 'english', file: 'english-21-birthday.html', title: 'Birthday', x: 67.6, y: 24, w: 14.4, h: 18.2 }
      ],
      secondaryHotspots: [
        { zone: 'english', file: 'english-02-abc.html', title: '学习榜单', x: 1.8, y: 26.2, w: 14.4, h: 28 },
        { zone: 'english', file: 'english-21-birthday.html', title: 'Let’s Learn English', x: 83.8, y: 32, w: 13.4, h: 30.4 }
      ],
      quickLinks: [
        { label: 'ABC 起步', href: 'english/english-02-abc.html' },
        { label: '返回村庄', href: 'village.html' }
      ],
      cards: [
        { zone: 'english', file: 'english-01-hello.html', title: 'Lesson 1 Hello', desc: '先用问候打开英语耳朵，进场很轻松。', emoji: '👋', chip: '口语启蒙', duration: '10分钟', color: 'linear-gradient(135deg,#dff5d8,#8ed47f)' },
        { zone: 'english', file: 'english-02-abc.html', title: 'Lesson 2 ABC', desc: '最核心的字母课，适合作为起步入口。', emoji: '🅰️', chip: '字母', duration: '12分钟', color: 'linear-gradient(135deg,#dcebff,#83b6ff)' },
        { zone: 'english', file: 'english-04-colors.html', title: 'Lesson 4 Colors', desc: '颜色主题非常直观，适合低龄孩子。', emoji: '🌈', chip: '主题词汇', duration: '10分钟', color: 'linear-gradient(135deg,#ffe7a9,#ffb165)' },
        { zone: 'english', file: 'english-05-numbers.html', title: 'Lesson 5 Numbers', desc: '把英语和数字认知顺手串在一起。', emoji: '🔢', chip: '数字', duration: '10分钟', color: 'linear-gradient(135deg,#dbe9ff,#7eaefe)' },
        { zone: 'english', file: 'english-07-animals.html', title: 'Lesson 7 Animals', desc: '动物词汇天生讨喜，也方便配图记忆。', emoji: '🐾', chip: '热门', duration: '12分钟', color: 'linear-gradient(135deg,#dbf5da,#90d57e)' },
        { zone: 'english', file: 'english-09-food.html', title: 'Lesson 9 Food', desc: '吃的最容易带入生活场景，孩子会很有参与感。', emoji: '🍕', chip: '生活词汇', duration: '10分钟', color: 'linear-gradient(135deg,#ffe4c8,#ffa96c)' },
        { zone: 'english', file: 'english-10-toys.html', title: 'Lesson 10 Toys', desc: '玩具主题很适合把单词练成主动表达。', emoji: '🧸', chip: '兴趣主题', duration: '10分钟', color: 'linear-gradient(135deg,#f0e0ff,#bf95ff)' },
        { zone: 'english', file: 'english-21-birthday.html', title: 'Lesson 21 Birthday', desc: '场景感很强的一课，孩子通常很愿意点开。', emoji: '🎂', chip: '场景对话', duration: '12分钟', color: 'linear-gradient(135deg,#ffe5d4,#ff9f73)' }
      ]
    }
  };

  var ZONE_DIR = {
    stories: 'stories',
    science: 'science',
    chinese: 'chinese',
    math: 'math',
    english: 'english'
  };

  function resolveHref(card) {
    if (card.href) return card.href;
    var dir = ZONE_DIR[card.zone] || '';
    return dir ? dir + '/' + card.file : card.file;
  }

  function getFeaturedCourse(page) {
    return page && page.featured ? page.featured : null;
  }

  function appendHotspots(container, items, kind) {
    if (!container || !items || !items.length) return;
    items.forEach(function(item) {
      container.appendChild(createHotspot(item, kind));
    });
  }

  function buildToolbarStats(page) {
    var stats = [];
    var toolbar = page.toolbar || {};
    var featured = getFeaturedCourse(page);
    var actionCount = (toolbar.actions && toolbar.actions.length) || (page.quickLinks && page.quickLinks.length) || 0;
    var hotspotCount = ((page.hotspots && page.hotspots.length) || 0) + ((page.secondaryHotspots && page.secondaryHotspots.length) || 0);

    if (page.cards && page.cards.length) {
      stats.push(page.cards.length + ' 节内容');
    }
    if (actionCount) {
      stats.push(actionCount + ' 个快捷入口');
    }
    if (hotspotCount) {
      stats.push(hotspotCount + ' 个墙面入口');
    }
    if (featured && featured.badge) {
      stats.push(featured.badge);
    }

    return stats;
  }

  function createToolbarStatus(page) {
    var toolbar = page.toolbar || {};
    var featured = getFeaturedCourse(page);
    var stats = buildToolbarStats(page);
    var pills = '';
    stats.forEach(function(item) {
      pills += '<span class="bottom-status-pill">' + item + '</span>';
    });

    var featuredBlock = '';
    if (featured) {
      featuredBlock =
        '<div class="bottom-status-featured">' +
          '<span class="bottom-status-featured-tag">' + (featured.badge || '今日主推') + '</span>' +
          '<div class="bottom-status-featured-copy">' +
            '<span class="bottom-status-featured-title">' + (featured.title || '推荐课程') + '</span>' +
            '<span class="bottom-status-featured-desc">' + (featured.desc || featured.note || '点开就能继续往下逛。') + '</span>' +
          '</div>' +
        '</div>';
    }

    var line = toolbar.status || toolbar.hint || '快捷入口已就绪';
    if (featured && featured.note) {
      line += ' ' + featured.note;
    }

    var status = document.createElement('div');
    status.className = 'bottom-status';
    status.innerHTML =
      '<div class="bottom-status-head">' +
        '<div class="bottom-status-icon">' + (toolbar.icon || '✨') + '</div>' +
        '<div class="bottom-status-copy">' +
          '<div class="bottom-status-kicker">' + (toolbar.label || page.kicker || 'Learning Hub') + '</div>' +
          '<div class="bottom-status-title">' + (toolbar.title || '快速入口') + '</div>' +
        '</div>' +
      '</div>' +
      featuredBlock +
      '<p class="bottom-status-line">' + line + '</p>' +
      '<div class="bottom-status-pills">' + pills + '</div>';
    return status;
  }

  function createCard(card) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'course-card';
    button.style.setProperty('--card-bg', card.color || 'rgba(255,255,255,.9)');
    button.innerHTML =
      '<div>' +
        '<div class="course-card-top">' +
          '<div class="course-emoji">' + (card.emoji || '📘') + '</div>' +
          '<div class="course-chip">' + (card.chip || '课程') + '</div>' +
        '</div>' +
        '<h2 class="course-title">' + card.title + '</h2>' +
        '<p class="course-desc">' + card.desc + '</p>' +
      '</div>' +
      '<div class="course-meta"><span>' + (card.zone ? card.zone.toUpperCase() : 'HUB') + '</span><span>' + (card.duration || '进入') + '</span></div>';
    button.addEventListener('click', function() {
      window.location.href = resolveHref(card);
    });
    return button;
  }

  function createQuickLink(item, onClick, index) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'quick-link' + (item.tone ? ' is-' + item.tone : index === 0 ? ' is-primary' : '');
    button.setAttribute('aria-label', item.note ? item.label + '，' + item.note : item.label);
    button.innerHTML =
      '<span class="quick-link-icon">' + (item.icon || '✨') + '</span>' +
      '<span class="quick-link-main">' +
        '<span class="quick-link-label">' + item.label + '</span>' +
        '<span class="quick-link-note">' + (item.note || '快速入口') + '</span>' +
      '</span>' +
      '<span class="quick-link-arrow" aria-hidden="true">' + (item.arrow || '›') + '</span>';
    button.addEventListener('click', onClick);
    return button;
  }

  function createHotspot(item, kind) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'painted-hotspot' + (kind === 'secondary' ? ' is-secondary' : '');
    button.setAttribute('aria-label', item.title);
    button.title = item.title;
    button.style.left = item.x + '%';
    button.style.top = item.y + '%';
    button.style.width = item.w + '%';
    button.style.height = item.h + '%';
    button.addEventListener('click', function() {
      window.location.href = resolveHref(item);
    });
    return button;
  }

  function focusCard(strip, targetHref) {
    if (!strip || !targetHref) return false;
    var cards = strip.querySelectorAll('.course-card');
    for (var i = 0; i < cards.length; i += 1) {
      if (cards[i].dataset.href === targetHref) {
        cards[i].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        cards[i].classList.remove('is-spotlit');
        void cards[i].offsetWidth;
        cards[i].classList.add('is-spotlit');
        window.setTimeout(function(card) {
          return function() {
            card.classList.remove('is-spotlit');
          };
        }(cards[i]), 1400);
        return true;
      }
    }
    return false;
  }

  function createToolbarActions(page, strip, step) {
    var toolbar = page.toolbar || {};
    var actions = [
      { icon: '◀', label: '上一组卡墙', note: '向左浏览卡墙', arrow: '←', action: 'scroll', direction: -1, tone: 'nav' },
      { icon: '▶', label: '下一组卡墙', note: '向右浏览卡墙', arrow: '→', action: 'scroll', direction: 1, tone: 'nav' }
    ].concat(toolbar.actions || page.quickLinks || []);
    var wrap = document.createElement('div');
    wrap.className = 'bottom-actions';

    actions.forEach(function(item, index) {
      wrap.appendChild(createQuickLink(item, function() {
        if (item.action === 'scroll') {
          step(item.direction || 1);
          return;
        }

        if (item.action === 'focus') {
          var targetHref = resolveHref(item);
          if (focusCard(strip, targetHref)) return;
        }

        window.location.href = resolveHref(item);
      }, index));
    });

    return wrap;
  }

  function mountInteriorPage() {
    var root = document.getElementById('interiorPage');
    if (!root || !window.INTERIOR_PAGE_KEY) return;
    var page = INTERIOR_PAGES[window.INTERIOR_PAGE_KEY];
    if (!page) return;

    document.title = page.title;
    root.style.backgroundImage = 'url("' + page.background + '")';

    var hero = document.getElementById('heroCopy');
    hero.innerHTML =
      '<p class="hero-kicker">' + page.kicker + '</p>' +
      '<h1 class="hero-title">' + page.title + '</h1>' +
      '<p class="hero-subtitle">' + page.subtitle + '</p>';

    var strip = document.getElementById('cardStrip');
    page.cards.forEach(function(card) {
      var cardNode = createCard(card);
      cardNode.dataset.href = resolveHref(card);
      strip.appendChild(cardNode);
    });

    var hotspots = document.getElementById('paintedHotspots');
    appendHotspots(hotspots, page.hotspots, 'primary');
    appendHotspots(hotspots, page.secondaryHotspots, 'secondary');

    var step = function(direction) {
      strip.scrollBy({ left: direction * Math.min(strip.clientWidth * 0.82, 340), behavior: 'smooth' });
    };

    var bottomBar = root.querySelector('.bottom-bar');
    if (bottomBar) {
      bottomBar.innerHTML = '';
      bottomBar.appendChild(createToolbarStatus(page));
      bottomBar.appendChild(createToolbarActions(page, strip, step));
    }

    var navPrev = document.getElementById('navPrev');
    var navNext = document.getElementById('navNext');
    if (navPrev) {
      navPrev.innerHTML = '<span class="nav-button-arrow" aria-hidden="true">‹</span><span class="nav-button-label">上一组卡墙</span>';
      navPrev.addEventListener('click', function() { step(-1); });
    }
    if (navNext) {
      navNext.innerHTML = '<span class="nav-button-label">下一组卡墙</span><span class="nav-button-arrow" aria-hidden="true">›</span>';
      navNext.addEventListener('click', function() { step(1); });
    }
    document.getElementById('backButton').addEventListener('click', function() {
      window.location.href = 'village.html';
    });
  }

  document.addEventListener('DOMContentLoaded', mountInteriorPage);
})();
