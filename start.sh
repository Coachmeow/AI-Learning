#!/usr/bin/env sh
# เปิดเว็บแบบ offline (ไม่ต้องต่อเน็ต) / Open the site offline.
# Serves the built site on http://localhost:4321 using Python 3.
cd "$(dirname "$0")" || exit 1
if [ -f dist/index.html ]; then DIR=dist; elif [ -f index.html ]; then DIR=.; else
  echo "ยังไม่มีเว็บที่ build แล้ว: รัน npm install แล้ว npm run build ก่อน"
  echo "No built site found: run npm install and npm run build first."
  exit 1
fi
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; else
  echo "ต้องติดตั้ง Python 3 ก่อน / Python 3 is required: https://www.python.org/downloads/"
  exit 1
fi
PORT="${PORT:-4321}"
URL="http://localhost:$PORT/"
(sleep 1.5; if command -v open >/dev/null 2>&1; then open "$URL"; elif command -v xdg-open >/dev/null 2>&1; then xdg-open "$URL"; fi) >/dev/null 2>&1 &
echo "AI-Learning: $URL"
echo "กด Ctrl+C เพื่อปิด / Press Ctrl+C to stop."
exec "$PY" -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR"
