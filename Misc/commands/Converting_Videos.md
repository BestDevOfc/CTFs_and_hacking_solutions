```bash
ffmpeg -i input.mov -c:v copy -c:a copy output.mp4
ffmpeg -i input.mov -vcodec libx264 -crf 23 -preset medium -acodec aac -b:a 128k output.mp4
```


sips -s format png input.heic --out output.png
for f in *.heic; do sips -s format png "$f" --out "${f%.heic}.png"; done
