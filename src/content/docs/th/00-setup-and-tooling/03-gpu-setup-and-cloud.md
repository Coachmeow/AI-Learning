---
title: "ตั้งค่า GPU และคลาวด์ (GPU Setup & Cloud)"
description: "ฝึกโมเดลบน CPU ก็พอสำหรับการเรียน แต่ถ้าจะฝึกจริงต้องใช้ GPU"
sidebar:
  label: "03 · ตั้งค่า GPU และคลาวด์"
  order: 3
upstream_path: "phases/00-setup-and-tooling/03-gpu-setup-and-cloud"
upstream_commit: "6a63ddb066207fca854ece311da0289295c2a313"
source_hash: "913b61e496cff6bba6c95c5121a4fa389793f5ce98ae9b7745c491158428e25a"
---
> ฝึกโมเดลบน CPU ก็พอสำหรับการเรียน แต่ถ้าจะฝึกจริงต้องใช้ GPU

**ประเภท:** ลงมือสร้าง (Build)
**ภาษา:** Python
**ความรู้ที่ควรมีก่อน:** Phase 0 บทที่ 01
**เวลา:** ~45 นาที

## สิ่งที่จะได้เรียนรู้

- ตรวจว่าเครื่องมี GPU ใช้ได้หรือไม่ ด้วย `nvidia-smi` และ CUDA API ของ PyTorch
- ตั้งค่า Google Colab ให้ใช้ GPU รุ่น T4 สำหรับทดลองบนคลาวด์ฟรี
- จับเวลาการคูณเมทริกซ์บน CPU เทียบกับ GPU แล้ววัดว่าเร็วขึ้นกี่เท่า
- ประมาณขนาดโมเดลที่ใหญ่ที่สุดที่ใส่ใน VRAM ได้ ด้วยหลักคร่าวๆ ของ fp16

## ปัญหา

บทส่วนใหญ่ใน phase 1-3 รันบน CPU ได้สบาย แต่เมื่อเริ่มฝึก CNN, transformer หรือ LLM (phase 4 ขึ้นไป) คุณต้องใช้ GPU ช่วยเร่ง การฝึกที่ใช้เวลา 8 ชั่วโมงบน CPU จะเหลือ 10 นาทีบน GPU

คุณมีสามทางเลือก: GPU ในเครื่อง, GPU บนคลาวด์ หรือ Google Colab (ฟรี)

## แนวคิด

```
ตัวเลือกของคุณ:

1. GPU ของ NVIDIA ในเครื่อง
   ค่าใช้จ่าย: $0 (มีอยู่แล้ว)
   การตั้งค่า: ติดตั้ง CUDA + cuDNN
   เหมาะกับ: ใช้งานประจำ, ชุดข้อมูลขนาดใหญ่

2. Google Colab (รุ่นฟรี)
   ค่าใช้จ่าย: $0
   การตั้งค่า: ไม่ต้องทำอะไร
   เหมาะกับ: ทดลองเร็วๆ, ที่บ้านไม่มี GPU

3. GPU บนคลาวด์ (Lambda, RunPod, Vast.ai)
   ค่าใช้จ่าย: $0.20-2.00/ชม.
   การตั้งค่า: SSH + ติดตั้ง
   เหมาะกับ: ฝึกจริงจัง, โมเดลขนาดใหญ่
```

```figure
s0-gpu-dispatch
```

## ลงมือสร้าง (Build It)

### ทางเลือกที่ 1: GPU ของ NVIDIA ในเครื่อง

ตรวจดูว่ามีหรือไม่:

```bash
nvidia-smi
```

ติดตั้ง PyTorch ที่รองรับ CUDA บน Linux wheel ปกติมี CUDA มาให้แล้ว ส่วนบน Windows ให้คัดลอกคำสั่งแบบ CUDA จากตัวเลือกบนเว็บ pytorch.org

```bash
pip install torch torchvision torchaudio
```

จากนั้นตรวจว่า PyTorch มองเห็น GPU:

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```

### ทางเลือกที่ 2: Google Colab

1. ไปที่ [colab.research.google.com](https://colab.research.google.com)
2. Runtime > Change runtime type > T4 GPU
3. รัน `!nvidia-smi` เพื่อตรวจสอบ

อัปโหลด notebook ของหลักสูตรนี้ขึ้น Colab ได้โดยตรง

### ทางเลือกที่ 3: GPU บนคลาวด์

สำหรับ Lambda Labs, RunPod หรือ Vast.ai:

```bash
ssh user@your-gpu-instance

pip install torch torchvision torchaudio
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

### ไม่มี GPU? ไม่เป็นไร

บทส่วนใหญ่ใช้ CPU ได้ บทที่ต้องใช้ GPU จะบอกไว้ และมีลิงก์ Colab ให้

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using: {device}")
```

## ลงมือสร้าง: เทียบความเร็ว GPU กับ CPU

```python
import torch
import time

size = 5000

a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)

start = time.time()
c_cpu = a_cpu @ b_cpu
cpu_time = time.time() - start
print(f"CPU: {cpu_time:.3f}s")

if torch.cuda.is_available():
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU: {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")
```

## แบบฝึกหัด

1. รันโค้ดเทียบความเร็วด้านบน แล้วเทียบเวลาของ CPU กับ GPU
2. ถ้าไม่มี GPU ให้รันบน Google Colab แล้วเทียบดู
3. ดูว่า GPU ของคุณมีหน่วยความจำเท่าไร แล้วประมาณขนาดโมเดลที่ใหญ่ที่สุดที่ใส่ได้ (หลักคร่าวๆ: fp16 ใช้ 2 byte ต่อพารามิเตอร์)

### คำใบ้

**แบบฝึกหัดที่ 1** รันโค้ดจากหัวข้อลงมือสร้างตามที่เขียนไว้ แล้วจดเวลาของ CPU เวลาของ GPU และบรรทัด Speedup จากนั้นรันซ้ำอีกรอบ เพราะการรันบน GPU ครั้งแรกรวมเวลาเตรียมระบบไว้ด้วย ตัวเลขรอบที่สองจึงเป็นตัวที่ควรใช้เทียบ

**แบบฝึกหัดที่ 2** ใน Colab เลือก Runtime > Change runtime type > GPU แล้ววางโค้ดเทียบความเร็วลงใน cell รัน `!nvidia-smi` ในอีก cell ก่อน ต้องเห็นชื่อ GPU ก่อน ผลการเทียบความเร็วถึงจะมีความหมาย

**แบบฝึกหัดที่ 3** อ่านหน่วยความจำทั้งหมดด้วย `torch.cuda.get_device_properties(0).total_memory / 1e9` แบบเดียวกับใน `code/gpu_check.py` นำหน่วยความจำที่เป็น byte หารด้วย 2 จะได้จำนวนพารามิเตอร์สำหรับ fp16 แล้วเผื่อที่ไว้บ้าง เพราะ activation และ CUDA context ก็ใช้หน่วยความจำด้วย

## คำศัพท์สำคัญ

| คำศัพท์ | ที่คนมักพูด | ความหมายจริง |
|------|----------------|----------------------|
| CUDA | "เขียนโปรแกรม GPU" | แพลตฟอร์มคำนวณแบบขนานของ NVIDIA ที่ให้รันโค้ดบน GPU ได้ |
| VRAM | "หน่วยความจำ GPU" | Video RAM บน GPU แยกจาก RAM ของระบบ เป็นตัวจำกัดขนาดโมเดล |
| fp16 | "half precision" | ทศนิยมแบบ floating point 16 บิต ใช้หน่วยความจำครึ่งหนึ่งของ fp32 โดยความแม่นยำลดลงน้อยมาก |
| Tensor Core | "ฮาร์ดแวร์คูณเมทริกซ์เร็วๆ" | คอร์เฉพาะทางบน GPU สำหรับคูณเมทริกซ์ เร็วกว่าคอร์ปกติ 4-8 เท่า |
