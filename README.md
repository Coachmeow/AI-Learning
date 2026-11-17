# AI-Learning

เว็บไซต์สำหรับเรียน AI ฉบับภาษาไทย อังกฤษ

เรียนวิศวกรรม AI ด้วยการลงมือสร้างเอง อ่านได้ทั้งภาษาไทยและอังกฤษ รันโค้ด Python ในเบราว์เซอร์ได้ และมีแบบทดสอบท้ายบท 2 แบบ (เลือกตอบ / ลงมือเขียนโค้ด) ให้เลือกระดับ ง่าย กลาง ยาก ใช้งานได้แม้ไม่ต่ออินเทอร์เน็ต

> สถานะ: **รุ่นนำร่อง** มีบทเรียนครบชุด 1 บท คือ Phase 01 · การหาค่าเหมาะที่สุด (Optimization)
> แผนงานทั้งหมดอยู่ใน [docs/DESIGN.md](docs/DESIGN.md)

## เปิดเว็บบนเครื่อง

ต้องมี [Node.js](https://nodejs.org/) 22 ขึ้นไป และ Python 3 (สำหรับสคริปต์เปิดเว็บแบบ offline)

```bash
npm install        # ติดตั้งครั้งแรก (ต้องต่อเน็ต)
npm run build      # สร้างเว็บไว้ในโฟลเดอร์ dist/
./start.sh         # macOS / Linux: เปิดเว็บที่ http://localhost:4321
```

บน Windows ให้ดับเบิลคลิก `start.bat` แทน `./start.sh`

หลังจาก build แล้ว ใช้งานได้โดยไม่ต้องต่อเน็ต เพราะฟอนต์, Python (Pyodide), สูตรคณิต และแผนภาพทั้งหมดอยู่ในโฟลเดอร์ `dist/` แล้ว

ระหว่างพัฒนาใช้ `npm run dev` (โหลดหน้าใหม่อัตโนมัติเมื่อแก้ไฟล์)

> เปิดไฟล์ `dist/index.html` ตรงๆ ไม่ได้ เพราะเบราว์เซอร์ไม่ยอมรัน Python (WebAssembly) จากไฟล์ในเครื่อง ต้องเปิดผ่าน `start.sh` / `start.bat` / `npm run preview`

## โครงสร้าง

```text
src/content/docs/en/   บทเรียนภาษาอังกฤษ (นำเข้าอัตโนมัติจากต้นฉบับ ห้ามแก้ด้วยมือ)
src/content/docs/th/   บทเรียนภาษาไทย (คำแปล)
src/data/quizzes/      แบบทดสอบเลือกตอบสองภาษา แบ่ง 3 ระดับ
src/data/exercises/    โจทย์ลงมือเขียนโค้ด 3 ระดับ (starter, solution, tests, คำตอบผิดแบบจงใจ)
src/components/        ส่วนเสริมของหน้าบทเรียน (แถบแจ้งการแปล, แบบทดสอบ)
src/scripts/           โค้ดฝั่งเบราว์เซอร์ (รัน Python, แบบทดสอบ, ช่องเขียนโค้ด)
scripts/               สคริปต์นำเข้าเนื้อหาและตรวจโจทย์
glossary/th.json       คำศัพท์ไทยที่ใช้ร่วมกันทุกบท
```

## งานที่ทำซ้ำได้

```bash
node scripts/sync-upstream.mjs                                          # ดึงต้นฉบับล่าสุดมาไว้ที่ .upstream/
node scripts/import-content.mjs --lesson 01-math-foundations/08-optimization   # นำเข้าบท (หรือ --phase / --all)
npm run test:exercises                                                  # ตรวจว่าเฉลยผ่าน โค้ดเริ่มต้นไม่ผ่าน และจับคำตอบผิดได้
```

## ที่มาของเนื้อหา

เนื้อหาบทเรียน โค้ด คำถามเดิม และแผนภาพ interactive มาจาก [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) โดย Rohit Ghumare ใช้ภายใต้สัญญาอนุญาต MIT (ดู [NOTICE-UPSTREAM.md](NOTICE-UPSTREAM.md))
คำแปลภาษาไทย คำถามที่แต่งเพิ่ม และโจทย์ลงมือทำ เป็นงานของโปรเจกต์นี้
