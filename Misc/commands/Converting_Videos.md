```bash
ffmpeg -i input.mov -c:v copy -c:a copy output.mp4
ffmpeg -i input.mov -vcodec libx264 -crf 23 -preset medium -acodec aac -b:a 128k output.mp4
```
