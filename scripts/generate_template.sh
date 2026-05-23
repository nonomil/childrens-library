#!/bin/bash
# 批量生成童谣课件 - 复制Old MacDonald模板改内容
set -e

TEMPLATE="/home/deploy/childrens-library/courseware/old-macdonald.html"
OUTDIR="/home/deploy/childrens-library/courseware"
AUDIO="/home/deploy/childrens-library/courseware/audio"

# Song data: id|title|mp3|subtitle
SONGS=(
  "wheels-on-bus|🚌 The Wheels on the Bus|wheels.mp3|✏️ 公车的轮子转啊转！"
  "row-your-boat|🚣 Row Row Row Your Boat|rowyourboat.mp3|✏️ 划呀划呀划小船！"
  "itsy-bitsy-spider|🕷️ Itsy Bitsy Spider|itsybitsy.mp3|✏️ 小蜘蛛爬水管！"
  "bingo|🐶 BINGO|bingo.mp3|✏️ 农夫有一只小狗叫BINGO！"
  "head-shoulders|🧍 Head Shoulders Knees Toes|headshoulders.mp3|✏️ 头肩膀膝盖脚趾头！"
  "humpty-dumpty|🥚 Humpty Dumpty|humptydumpty.mp3|✏️ 蛋头先生坐在墙上！"
  "abc-song|🔤 ABC Song|abcsong.mp3|✏️ 一起学字母歌！"
)

for song in "${SONGS[@]}"; do
  IFS='|' read -r id title mp3 subtitle <<< "$song"
  outfile="$OUTDIR/$id.html"
  
  # Copy template
  cp "$TEMPLATE" "$outfile"
  
  # Replace title
  sed -i "s|<title>🚜 Old MacDonald Had a Farm</title>|<title>$title</title>|" "$outfile"
  
  # Replace MP3 reference
  sed -i "s|audio/oldmacdonald.mp3|audio/$mp3|g" "$outfile"
  
  # Replace cover subtitle
  sed -i "s|一首关于农场动物的英语儿歌！|$subtitle|g" "$outfile"
  
  echo "✅ $id.html ($title)"
done

echo ""
echo "🎉 生成了 ${#SONGS[@]} 个课件"
echo "⚠️  还需要手动修改每个文件的歌词、单词和SVG场景"
