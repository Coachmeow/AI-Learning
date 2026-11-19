---
title: "เสถียรภาพเชิงตัวเลข (Numerical Stability)"
description: "เลขทศนิยมแบบ floating point เป็นนามธรรมที่รั่ว มันจะกัดคุณระหว่างเทรน และคุณจะไม่ทันเห็นมันมา"
sidebar:
  label: "13 · เสถียรภาพเชิงตัวเลข"
  order: 13
upstream_path: "phases/01-math-foundations/13-numerical-stability"
upstream_commit: "6a63ddb066207fca854ece311da0289295c2a313"
source_hash: "611df7b0a07db308dad6e0e7830ab796c2f9801964a3a1aeb88c9f40526b3752"
---
> เลขทศนิยมแบบ floating point เป็นนามธรรมที่รั่ว มันจะกัดคุณระหว่างเทรน และคุณจะไม่ทันเห็นมันมา

**ประเภท:** ลงมือสร้าง (Build)
**ภาษา:** Python, TypeScript
**ความรู้ที่ควรมีก่อน:** Phase 1 บทที่ 01-04
**เวลา:** ~120 นาที

## สิ่งที่จะได้เรียนรู้

- เขียน softmax และ log-sum-exp ที่เสถียรเชิงตัวเลขด้วยเทคนิคลบค่ามากสุด
- ระบุการล้น (overflow) underflow และการหักล้างแบบหายนะ (catastrophic cancellation) ในการคำนวณเลขทศนิยม
- ตรวจ gradient เชิงวิเคราะห์เทียบกับ gradient เชิงตัวเลขด้วยผลต่างจำกัดแบบกลาง
- อธิบายว่าทำไม bfloat16 จึงนิยมกว่า float16 สำหรับการเทรน และ loss scaling ป้องกัน gradient underflow ได้อย่างไร

## ปัญหา

โมเดลของคุณเทรนไปสามชั่วโมง แล้ว loss ก็กลายเป็น NaN คุณเพิ่มคำสั่ง print logits ยังปกติดีที่ step 9,000 พอ step 9,001 มันเป็น `inf` พอถึง step 9,002 gradient ทุกตัวเป็น `nan` และการเทรนก็ตายไปแล้ว

หรือ: โมเดลเทรนจนจบ แต่ความแม่นยำต่ำกว่าที่เปเปอร์อ้างไว้ 2% คุณตรวจทุกอย่าง สถาปัตยกรรมตรง hyperparameter ตรง ข้อมูลตรง ปัญหาคือเปเปอร์ใช้ float32 แต่คุณใช้ float16 โดยไม่ได้ปรับสเกลให้ถูก ความคลาดเคลื่อนจากการปัดเศษที่สะสมมาค่อย ๆ กินความแม่นยำของคุณไปอย่างเงียบ ๆ

หรือ: คุณเขียน cross-entropy loss เองตั้งแต่ศูนย์ มันใช้ได้กับ logits เล็ก ๆ พอ logits เกิน 100 มันคืน `inf` softmax ล้นเพราะ `exp(100)` ใหญ่เกินกว่าที่ float32 จะเก็บได้ เฟรมเวิร์ก ML ทุกตัวรับมือเรื่องนี้ด้วยเทคนิคสองบรรทัด แต่คุณไม่รู้ว่ามีเทคนิคนี้อยู่

เสถียรภาพเชิงตัวเลขไม่ใช่เรื่องทางทฤษฎี มันคือความต่างระหว่างการเทรนที่สำเร็จกับการเทรนที่ล้มเหลวอย่างเงียบ ๆ บั๊ก ML ที่จริงจังทุกตัวที่คุณจะดีบัก สุดท้ายแล้วจะวนกลับมาที่เลขทศนิยม

## แนวคิด

### IEEE 754: คอมพิวเตอร์เก็บจำนวนจริงอย่างไร

คอมพิวเตอร์เก็บจำนวนจริงเป็นค่า floating point ตามมาตรฐาน IEEE 754 เลขทศนิยมหนึ่งตัวมีสามส่วน: บิตเครื่องหมาย (sign) เลขชี้กำลัง (exponent) และแมนทิสซา (mantissa หรือ significand)

```
Float32 layout (32 bits total):
[1 sign] [8 exponent] [23 mantissa]

Value = (-1)^sign * 2^(exponent - 127) * 1.mantissa
```

แมนทิสซากำหนดความแม่นยำ (มีเลขนัยสำคัญกี่หลัก) เลขชี้กำลังกำหนดช่วง (ตัวเลขใหญ่หรือเล็กได้แค่ไหน)

```
รูปแบบ      บิต    เลขชี้กำลัง  แมนทิสซา  หลักทศนิยม  ช่วง (โดยประมาณ)
float64    64     11        52        ~15-16      +/- 1.8e308
float32    32     8         23        ~7-8        +/- 3.4e38
float16    16     5         10        ~3-4        +/- 65,504
bfloat16   16     8         7         ~2-3        +/- 3.4e38
```

float32 ให้ความแม่นยำราว 7 หลักทศนิยม แปลว่ามันแยก 1.0000001 กับ 1.0000002 ได้ แต่แยก 1.00000001 กับ 1.00000002 ไม่ได้ หลังจาก 7 หลัก ทุกอย่างคือสัญญาณรบกวนจากการปัดเศษ

float16 ให้ราว 3 หลัก ค่าที่ใหญ่ที่สุดที่มันเก็บได้คือ 65,504 ซึ่งเล็กจนน่าตกใจสำหรับ ML ที่ logits, gradient และ activation มักเกินค่านี้เป็นประจำ

bfloat16 คือคำตอบของ Google ต่อปัญหาช่วงของ float16 มันมีเลขชี้กำลัง 8 บิตเท่ากับ float32 (ช่วงเท่ากัน ถึง 3.4e38) แต่มีแมนทิสซาแค่ 7 บิต (แม่นยำน้อยกว่า float16) สำหรับการเทรนโครงข่ายประสาทเทียม ช่วงสำคัญกว่าความแม่นยำ bfloat16 จึงมักชนะ

### ทำไม 0.1 + 0.2 != 0.3

ตัวเลข 0.1 แทนด้วยเลขทศนิยมฐานสองได้ไม่ตรงพอดี ในฐาน 2 มันเป็นเศษส่วนที่ซ้ำไม่รู้จบ:

```
0.1 in binary = 0.0001100110011001100110011... (repeating forever)
```

Float32 ตัดให้เหลือแมนทิสซา 23 บิต ค่าที่เก็บจริงประมาณ 0.100000001490116 ในทำนองเดียวกัน 0.2 ถูกเก็บเป็นประมาณ 0.200000002980232 ผลบวกของมันคือ 0.300000004470348 ไม่ใช่ 0.3

```
In Python:
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

เรื่องนี้สำคัญกับ ML เพราะ:

1. การเทียบ loss แบบ `if loss < threshold` อาจให้คำตอบผิด
2. การสะสมค่าเล็ก ๆ จำนวนมาก (การอัปเดต gradient หลายพันก้าว) จะค่อย ๆ เบี่ยงออกจากผลรวมจริง
3. checksum และการทดสอบว่าผลซ้ำได้ (reproducibility) จะล้มเหลวถ้าเทียบเลขทศนิยมด้วย `==`

วิธีแก้: อย่าเทียบเลขทศนิยมด้วย `==` ให้ใช้ `abs(a - b) < epsilon` หรือ `math.isclose()`

### การหักล้างแบบหายนะ (Catastrophic Cancellation)

เมื่อคุณลบเลขทศนิยมสองตัวที่เกือบเท่ากัน หลักนัยสำคัญจะหักล้างกันหมด แล้วเหลือแต่สัญญาณรบกวนจากการปัดเศษที่ถูกยกขึ้นมาเป็นหลักนำ

```
a = 1.0000001    (เก็บเป็น 1.00000011920929 ใน float32)
b = 1.0000000    (เก็บเป็น 1.00000000000000 ใน float32)

ผลต่างจริง:      0.0000001
ที่คำนวณได้:      0.00000011920929

ความคลาดเคลื่อนสัมพัทธ์: 19.2%
```

นั่นคือความคลาดเคลื่อนสัมพัทธ์ 19% จากการลบครั้งเดียว ใน ML เรื่องนี้เกิดเมื่อใดก็ตามที่คุณ:

- คำนวณความแปรปรวนของข้อมูลที่ค่าเฉลี่ยใหญ่: $\mathbb{E}[x^2] - \mathbb{E}[x]^2$ เมื่อ $\mathbb{E}[x]$ มีค่ามาก
- ลบ log ของความน่าจะเป็นที่เกือบเท่ากัน
- คำนวณ gradient แบบผลต่างจำกัดด้วย epsilon ที่เล็กเกินไป

วิธีแก้: จัดสูตรใหม่ให้เลี่ยงการลบตัวเลขใหญ่ที่เกือบเท่ากัน สำหรับความแปรปรวน ใช้อัลกอริทึมของ Welford หรือจัดข้อมูลให้อยู่กึ่งกลางก่อน สำหรับ log ของความน่าจะเป็น ให้ทำงานในปริภูมิ log ตลอด

### Overflow และ Underflow

การล้น (overflow) เกิดเมื่อผลลัพธ์ใหญ่เกินกว่าจะเก็บได้ underflow เกิดเมื่อมันเล็กเกินไป (ใกล้ศูนย์กว่าจำนวนบวกที่เล็กที่สุดที่เก็บได้)

```
ขอบเขตของ float32:
  ค่ามากสุด:  3.4028235e+38
  จำนวนบวกที่เล็กที่สุด (normal): 1.175e-38
  จำนวนบวกที่เล็กที่สุด (denorm): 1.401e-45
  Overflow:  อะไรที่ > 3.4e38 กลายเป็น inf
  Underflow: อะไรที่ < 1.4e-45 กลายเป็น 0.0
```

ฟังก์ชัน `exp()` คือต้นเหตุหลักของการล้นใน ML:

```
exp(88.7)  = 3.40e+38   (barely fits in float32)
exp(89.0)  = inf         (overflow)
exp(-87.3) = 1.18e-38   (barely above underflow)
exp(-104)  = 0.0         (underflow to zero)
```

ฟังก์ชัน `log()` เจอปัญหาในทิศตรงข้าม:

```
log(0.0)   = -inf
log(-1.0)  = nan
log(1e-45) = -103.3      (fine)
log(1e-46) = -inf        (input underflowed to 0, then log(0) = -inf)
```

ใน ML `exp()` ปรากฏใน softmax, sigmoid และการคำนวณความน่าจะเป็น `log()` ปรากฏใน cross-entropy, log-likelihood และ KL divergence การรวม `log(exp(x))` เป็นทุ่งระเบิดถ้าไม่มีเทคนิคที่ถูกต้อง

### เทคนิค Log-Sum-Exp

การคำนวณ `log(sum(exp(x_i)))` ตรง ๆ อันตรายเชิงตัวเลข ถ้า `x_i` ตัวใดใหญ่ `exp(x_i)` จะล้น ถ้า `x_i` ทุกตัวติดลบมาก `exp(x_i)` ทุกตัวจะ underflow เป็นศูนย์ แล้ว `log(0)` คือ `-inf`

เทคนิค: ลบค่ามากสุดออกก่อนยกกำลัง exp

```math
\log\left(\sum_i \exp(x_i)\right) = \max(x) + \log\left(\sum_i \exp(x_i - \max(x))\right)
```

ทำไมจึงได้ผล: หลังลบ `max(x)` เลขชี้กำลังที่ใหญ่ที่สุดคือ `exp(0) = 1` จึงล้นไม่ได้ มีอย่างน้อยหนึ่งพจน์ในผลรวมที่เป็น 1 ผลรวมจึงอย่างน้อย 1 และ `log(1) = 0` จึง underflow ไปเป็น `-inf` ไม่ได้

พิสูจน์:

```math
\begin{aligned}
& \log\left(\sum_i \exp(x_i)\right) \\
&= \log\left(\sum_i \exp(x_i - c + c)\right) && \text{(add and subtract } c\text{)} \\
&= \log\left(\sum_i \exp(x_i - c) \cdot \exp(c)\right) && (\exp(a+b) = \exp(a) \cdot \exp(b)) \\
&= \log\left(\exp(c) \cdot \sum_i \exp(x_i - c)\right) && \text{(factor out } \exp(c)\text{)} \\
&= c + \log\left(\sum_i \exp(x_i - c)\right) && (\log(a \cdot b) = \log(a) + \log(b))
\end{aligned}
```

(บวกและลบ $c$, ใช้ $\exp(a+b) = \exp(a) \cdot \exp(b)$, ดึง $\exp(c)$ ออกมา แล้วใช้ $\log(a \cdot b) = \log(a) + \log(b)$)

ตั้ง `c = max(x)` แล้วการล้นก็หายไป

เทคนิคนี้ปรากฏทุกที่ใน ML:
- การทำให้เป็นมาตรฐานของ softmax
- การคำนวณ cross-entropy loss
- การรวม log ของความน่าจะเป็นในโมเดลลำดับ
- Mixture of Gaussians
- Variational inference

### ทำไม softmax จึงต้องใช้เทคนิคลบค่ามากสุด

Softmax แปลง logits เป็นความน่าจะเป็น:

```math
\mathop{\mathrm{softmax}}(x_i) = \frac{\exp(x_i)}{\sum_j \exp(x_j)}
```

ถ้าไม่ใช้เทคนิคนี้ logits [100, 101, 102] จะทำให้ล้น:

```
exp(100) = 2.69e43
exp(101) = 7.31e43
exp(102) = 1.99e44
sum      = 2.99e44

2.69e43 > 3.4e38 ซึ่งเป็นค่ามากสุดของ float32 ทุกพจน์จึงล้น
exp(88.7) ก็ชนขีดจำกัดของ float32 แล้ว
exp(100) = inf ใน float32
```

เมื่อใช้เทคนิคนี้ ลบ max(x) = 102:

```
exp(100 - 102) = exp(-2) = 0.135
exp(101 - 102) = exp(-1) = 0.368
exp(102 - 102) = exp(0)  = 1.000
sum = 1.503

softmax = [0.090, 0.245, 0.665]
```

ความน่าจะเป็นเหมือนเดิมทุกประการ การคำนวณปลอดภัย นี่ไม่ใช่การปรับให้เร็วขึ้น มันคือสิ่งจำเป็นเพื่อให้ได้ผลที่ถูกต้อง

### NaN และ Inf: การตรวจจับและการป้องกัน

`nan` (Not a Number) และ `inf` (อนันต์) แพร่ต่อไปในการคำนวณเหมือนไวรัส `nan` ตัวเดียวในการอัปเดต gradient ทำให้น้ำหนักเป็น `nan` แล้วผลลัพธ์ทุกตัวหลังจากนั้นก็เป็น `nan` การเทรนตายภายในก้าวเดียว

`inf` เกิดจาก:
- `exp()` ของจำนวนบวกที่ใหญ่
- การหารด้วยศูนย์: `1.0 / 0.0`
- การล้นของ `float32` ในการสะสมค่า

`nan` เกิดจาก:
- `0.0 / 0.0`
- `inf - inf`
- `inf * 0`
- `sqrt()` ของจำนวนลบ
- `log()` ของจำนวนลบ
- การคำนวณใด ๆ ที่มี `nan` อยู่แล้ว

การตรวจจับ:

```python
import math

math.isnan(x)       # True if x is nan
math.isinf(x)       # True if x is +inf or -inf
math.isfinite(x)    # True if x is neither nan nor inf
```

กลยุทธ์การป้องกัน:

1. จำกัดขาเข้าของ `exp()`: `exp(clamp(x, -80, 80))`
2. บวก epsilon ให้ตัวส่วน: `x / (y + 1e-8)`
3. บวก epsilon ภายใน `log()`: `log(x + 1e-8)`
4. ใช้ implementation ที่เสถียร (log-sum-exp, softmax ที่เสถียร)
5. ตัด gradient (gradient clipping) เพื่อป้องกันน้ำหนักระเบิด
6. ตรวจหา `nan`/`inf` หลังทุก forward pass ระหว่างดีบัก

### การตรวจ gradient เชิงตัวเลข

gradient เชิงวิเคราะห์ (จาก backpropagation) อาจมีบั๊ก การตรวจ gradient เชิงตัวเลขยืนยันความถูกต้องโดยคำนวณ gradient ด้วยผลต่างจำกัด

สูตรผลต่างกลาง:

```math
\frac{df}{dx} \approx \frac{f(x + h) - f(x - h)}{2h}
```

สูตรนี้แม่นในระดับ $O(h^2)$ ดีกว่าผลต่างไปข้างหน้า $(f(x+h) - f(x)) / h$ มาก ซึ่งแม่นแค่ $O(h)$

การเลือก $h$: ใหญ่เกินไปการประมาณก็ผิด เล็กเกินไปการหักล้างแบบหายนะก็ทำลายคำตอบ ค่าทั่วไปคือ `h = 1e-5` ถึง `1e-7`

การตรวจ: คำนวณผลต่างสัมพัทธ์ระหว่าง gradient เชิงวิเคราะห์กับเชิงตัวเลข

```math
\text{relative\_error} = \frac{\lvert \text{grad}_{\text{analytical}} - \text{grad}_{\text{numerical}} \rvert}{\max(\lvert \text{grad}_{\text{analytical}} \rvert, \lvert \text{grad}_{\text{numerical}} \rvert, 10^{-8})}
```

หลักคร่าว ๆ:
- relative_error < 1e-7: สมบูรณ์แบบ gradient ถูกต้อง
- relative_error < 1e-5: ยอมรับได้ น่าจะถูก
- relative_error > 1e-3: มีอะไรผิดแน่
- relative_error > 1: gradient ผิดโดยสิ้นเชิง

ตรวจ gradient ทุกครั้งที่เขียนชั้นหรือฟังก์ชันความสูญเสียใหม่ PyTorch มี `torch.autograd.gradcheck()` สำหรับเรื่องนี้

### การเทรนแบบ mixed precision

GPU สมัยใหม่มีฮาร์ดแวร์เฉพาะ (Tensor Cores) ที่คูณเมทริกซ์ float16 เร็วกว่า float32 2-8 เท่า การเทรนแบบ mixed precision ใช้ประโยชน์จากสิ่งนี้:

```
1. เก็บสำเนาหลักของน้ำหนักเป็น float32
2. Forward pass ด้วย float16 (เร็ว)
3. คำนวณ loss ด้วย float32 (ป้องกันการล้น)
4. Backward pass ด้วย float16 (เร็ว)
5. ปรับสเกล gradient เป็น float32
6. อัปเดตน้ำหนักหลักที่เป็น float32
```

ปัญหาของการเทรนด้วย float16 ล้วน: gradient มักเล็กมาก (1e-8 หรือเล็กกว่า) float16 ทำให้ค่าที่ต่ำกว่าราว 6e-8 underflow เป็นศูนย์ โมเดลหยุดเรียนรู้เพราะการอัปเดต gradient ทุกครั้งเป็นศูนย์

วิธีแก้คือ loss scaling:

```
1. คูณ loss ด้วยตัวคูณสเกลขนาดใหญ่ (เช่น 1024)
2. Backward pass คำนวณ gradient ของ (loss * 1024)
3. gradient ทุกตัวใหญ่ขึ้น 1024 เท่า (ถูกดันให้พ้นจุด underflow ของ float16)
4. หาร gradient ด้วย 1024 ก่อนอัปเดตน้ำหนัก
5. ผลสุทธิ: อัปเดตเท่าเดิม แต่ไม่มี underflow
```

Dynamic loss scaling ปรับตัวคูณสเกลให้อัตโนมัติ เริ่มจากค่าใหญ่ (65536) ถ้า gradient ล้นเป็น `inf` ให้ลดครึ่ง ถ้าผ่านไป $N$ ก้าวโดยไม่ล้น ให้เพิ่มเป็นสองเท่า

### bfloat16 กับ float16: ทำไม bfloat16 จึงชนะในการเทรน

```
float16:   [1 sign] [5 exponent]  [10 mantissa]
bfloat16:  [1 sign] [8 exponent]  [7 mantissa]
```

float16 แม่นยำกว่า (แมนทิสซา 10 บิตเทียบกับ 7) แต่ช่วงจำกัด (มากสุดราว 65,504) bfloat16 แม่นยำน้อยกว่าแต่มีช่วงเท่ากับ float32 (มากสุดราว 3.4e38)

สำหรับการเทรนโครงข่ายประสาทเทียม:

- activation และ logits มักเกิน 65,504 ช่วงที่การเทรนพุ่งขึ้นชั่วคราว float16 ล้น แต่ bfloat16 รับได้
- float16 ต้องใช้ loss scaling แต่ bfloat16 มักไม่ต้อง เพราะช่วงของมันครอบคลุมขนาดของ gradient ได้ทั้งหมด
- bfloat16 คือการตัด float32 แบบง่าย ๆ: ทิ้งแมนทิสซา 16 บิตล่าง การแปลงจึงง่ายมากและไม่เสียอะไรในส่วนเลขชี้กำลัง

float16 นิยมใช้ตอน inference ที่ค่ามีขอบเขตและความแม่นยำสำคัญกว่า bfloat16 นิยมใช้ตอนเทรนที่ช่วงสำคัญกว่า นี่คือเหตุผลที่ TPU และ GPU ของ NVIDIA รุ่นใหม่ (A100, H100) รองรับ bfloat16 ในตัว

### การตัด gradient (Gradient Clipping)

gradient ระเบิดเกิดเมื่อ gradient โตแบบเลขชี้กำลังผ่านหลายชั้น (พบบ่อยใน RNN โครงข่ายลึก และ transformer) gradient ใหญ่ ๆ ตัวเดียวทำลายน้ำหนักทั้งหมดได้ในก้าวเดียว

การตัดมีสองแบบ:

**ตัดตามค่า (clip by value):** จำกัดแต่ละสมาชิกของ gradient แยกกัน

```
grad = clamp(grad, -max_val, max_val)
```

ง่าย แต่อาจเปลี่ยนทิศของเวกเตอร์ gradient

**ตัดตามนอร์ม (clip by norm):** ปรับสเกลเวกเตอร์ gradient ทั้งตัวให้นอร์มไม่เกินเกณฑ์

```
if ||grad|| > max_norm:
    grad = grad * (max_norm / ||grad||)
```

รักษาทิศของ gradient ไว้ นี่คือสิ่งที่ `torch.nn.utils.clip_grad_norm_()` ทำ และเป็นตัวเลือกมาตรฐาน

ค่าทั่วไป: `max_norm=1.0` สำหรับ transformer, `max_norm=0.5` สำหรับ RL, `max_norm=5.0` สำหรับโครงข่ายที่ง่ายกว่า

การตัด gradient ไม่ใช่การแก้ขัด มันคือกลไกความปลอดภัย ถ้าไม่มีมัน batch ผิดปกติ batch เดียวอาจสร้าง gradient ที่ใหญ่พอจะทำลายการเทรนหลายสัปดาห์

### ชั้น normalization ในฐานะตัวสร้างเสถียรภาพเชิงตัวเลข

Batch normalization, layer normalization และ RMS normalization มักถูกนำเสนอว่าเป็น regularizer ที่ช่วยให้การเทรนลู่เข้า มันยังเป็นตัวสร้างเสถียรภาพเชิงตัวเลขด้วย

ถ้าไม่มี normalization activation อาจโตหรือหดแบบเลขชี้กำลังผ่านชั้นต่าง ๆ:

```
ชั้นที่ 1: ค่าอยู่ใน [0, 1]
ชั้นที่ 5: ค่าอยู่ใน [0, 100]
ชั้นที่ 10: ค่าอยู่ใน [0, 10,000]
ชั้นที่ 50: ค่าอยู่ใน [0, inf]
```

Normalization จัดให้อยู่กึ่งกลางและปรับสเกล activation ใหม่ในทุกชั้น:

```math
\mathop{\mathrm{LayerNorm}}(x) = \frac{x - \mathop{\mathrm{mean}}(x)}{\mathop{\mathrm{std}}(x) + \epsilon} \cdot \gamma + \beta
```

`epsilon` (ปกติ 1e-5) ป้องกันการหารด้วยศูนย์เมื่อ activation ทุกตัวเท่ากัน พารามิเตอร์ที่เรียนรู้ได้ `gamma` และ `beta` ทำให้โครงข่ายคืนสเกลที่ต้องการได้

สิ่งนี้รักษาค่าให้อยู่ในช่วงที่ปลอดภัยเชิงตัวเลขตลอดทั้งโครงข่าย ป้องกันทั้งการล้นใน forward pass และ gradient ระเบิดใน backward pass

### บั๊กเชิงตัวเลขที่พบบ่อยใน ML

**บั๊ก: loss เป็น NaN หลังผ่านไปไม่กี่ epoch**
สาเหตุ: logits โตเกินไป softmax ล้น หรือ learning rate สูงเกินไปจนน้ำหนักลู่ออก
วิธีแก้: ใช้ softmax ที่เสถียร (ลบค่ามากสุด) ลด learning rate และเพิ่มการตัด gradient

**บั๊ก: loss ค้างอยู่ที่ log(num_classes)**
สาเหตุ: ผลลัพธ์ของโมเดลเป็นความน่าจะเป็นที่เกือบสม่ำเสมอ มักแปลว่า gradient หายไป หรือโมเดลไม่ได้เรียนรู้อะไรเลย
วิธีแก้: ตรวจว่า label ของข้อมูลถูก ตรวจฟังก์ชันความสูญเสีย และตรวจหา ReLU ที่ตายแล้ว

**บั๊ก: ความแม่นยำบน validation ต่ำกว่าที่คาด 1-3%**
สาเหตุ: ใช้ mixed precision โดยไม่มี loss scaling ที่เหมาะสม gradient underflow ทำให้การอัปเดตเล็ก ๆ กลายเป็นศูนย์อย่างเงียบ ๆ
วิธีแก้: เปิด dynamic loss scaling หรือเปลี่ยนไปใช้ bfloat16

**บั๊ก: นอร์มของ gradient เป็น 0.0 ในบางชั้น**
สาเหตุ: นิวรอน ReLU ที่ตายแล้ว (ขาเข้าเป็นลบทั้งหมด) หรือ float16 underflow
วิธีแก้: ใช้ LeakyReLU หรือ GELU ใช้ gradient scaling และตรวจการกำหนดค่าเริ่มต้นของน้ำหนัก

**บั๊ก: โมเดลทำงานบน GPU ตัวหนึ่ง แต่ให้ผลต่างกันบนอีกตัว**
สาเหตุ: ลำดับการสะสมเลขทศนิยมไม่แน่นอน การรวมแบบขนานบน GPU บวกในลำดับต่างกันบนฮาร์ดแวร์ต่างกัน และการบวกเลขทศนิยมไม่มีสมบัติการเปลี่ยนกลุ่ม
วิธีแก้: ยอมรับความต่างเล็กน้อย (1e-6) หรือตั้ง `torch.use_deterministic_algorithms(True)` และยอมรับว่าจะช้าลง

**บั๊ก: `exp()` คืน `inf` ในการคำนวณ loss**
สาเหตุ: ส่ง logits ดิบเข้า `exp()` โดยไม่ใช้เทคนิคลบค่ามากสุด
วิธีแก้: ใช้ `torch.nn.functional.log_softmax()` ซึ่งใช้ log-sum-exp ภายใน

**บั๊ก: การเทรนลู่ออกหลังเปลี่ยนจาก float32 เป็น float16**
สาเหตุ: float16 เก็บขนาด gradient ที่ต่ำกว่า 6e-8 หรือ activation ที่เกิน 65,504 ไม่ได้
วิธีแก้: ใช้ mixed precision พร้อม loss scaling (AMP) หรือใช้ bfloat16 แทน

```figure
logsumexp-stability
```

## ลงมือสร้าง (Build It)

### ขั้นที่ 1: สาธิตขีดจำกัดความแม่นยำของเลขทศนิยม

```python
print("=== Floating Point Precision ===")
print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
print(f"Difference: {(0.1 + 0.2) - 0.3:.2e}")
```

### ขั้นที่ 2: softmax แบบตรง ๆ กับแบบเสถียร

```python
import math

def softmax_naive(logits):
    exps = [math.exp(z) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

def softmax_stable(logits):
    max_logit = max(logits)
    exps = [math.exp(z - max_logit) for z in logits]
    total = sum(exps)
    return [e / total for e in exps]

safe_logits = [2.0, 1.0, 0.1]
print(f"Naive:  {softmax_naive(safe_logits)}")
print(f"Stable: {softmax_stable(safe_logits)}")

dangerous_logits = [100.0, 101.0, 102.0]
print(f"Stable: {softmax_stable(dangerous_logits)}")
# softmax_naive(dangerous_logits) would return [nan, nan, nan]
```

### ขั้นที่ 3: log-sum-exp ที่เสถียร

```python
def logsumexp_naive(values):
    return math.log(sum(math.exp(v) for v in values))

def logsumexp_stable(values):
    c = max(values)
    return c + math.log(sum(math.exp(v - c) for v in values))

safe = [1.0, 2.0, 3.0]
print(f"Naive:  {logsumexp_naive(safe):.6f}")
print(f"Stable: {logsumexp_stable(safe):.6f}")

large = [500.0, 501.0, 502.0]
print(f"Stable: {logsumexp_stable(large):.6f}")
# logsumexp_naive(large) returns inf
```

### ขั้นที่ 4: cross-entropy ที่เสถียร

```python
def cross_entropy_naive(true_class, logits):
    probs = softmax_naive(logits)
    return -math.log(probs[true_class])

def cross_entropy_stable(true_class, logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = math.log(sum(math.exp(s) for s in shifted))
    log_prob = shifted[true_class] - log_sum_exp
    return -log_prob

logits = [2.0, 5.0, 1.0]
true_class = 1
print(f"Naive:  {cross_entropy_naive(true_class, logits):.6f}")
print(f"Stable: {cross_entropy_stable(true_class, logits):.6f}")
```

### ขั้นที่ 5: การตรวจ gradient

```python
def numerical_gradient(f, x, h=1e-5):
    grad = []
    for i in range(len(x)):
        x_plus = x[:]
        x_minus = x[:]
        x_plus[i] += h
        x_minus[i] -= h
        grad.append((f(x_plus) - f(x_minus)) / (2 * h))
    return grad

def check_gradient(analytical, numerical, tolerance=1e-5):
    for i, (a, n) in enumerate(zip(analytical, numerical)):
        denom = max(abs(a), abs(n), 1e-8)
        rel_error = abs(a - n) / denom
        status = "OK" if rel_error < tolerance else "FAIL"
        print(f"  param {i}: analytical={a:.8f} numerical={n:.8f} "
              f"rel_error={rel_error:.2e} [{status}]")

def f(params):
    x, y = params
    return x**2 + 3*x*y + y**3

def f_grad(params):
    x, y = params
    return [2*x + 3*y, 3*x + 3*y**2]

point = [2.0, 1.0]
analytical = f_grad(point)
numerical = numerical_gradient(f, point)
check_gradient(analytical, numerical)
```

## นำไปใช้ (Use It)

### จำลอง mixed precision

```python
import struct

def float32_to_float16_round(x):
    packed = struct.pack('f', x)
    f32 = struct.unpack('f', packed)[0]
    packed16 = struct.pack('e', f32)
    return struct.unpack('e', packed16)[0]

def simulate_bfloat16(x):
    packed = struct.pack('f', x)
    as_int = int.from_bytes(packed, 'little')
    truncated = as_int & 0xFFFF0000
    repacked = truncated.to_bytes(4, 'little')
    return struct.unpack('f', repacked)[0]
```

### การตัด gradient

```python
def clip_by_norm(gradients, max_norm):
    total_norm = math.sqrt(sum(g**2 for g in gradients))
    if total_norm > max_norm:
        scale = max_norm / total_norm
        return [g * scale for g in gradients]
    return gradients

grads = [10.0, 20.0, 30.0]
clipped = clip_by_norm(grads, max_norm=5.0)
print(f"Original norm: {math.sqrt(sum(g**2 for g in grads)):.2f}")
print(f"Clipped norm:  {math.sqrt(sum(g**2 for g in clipped)):.2f}")
print(f"Direction preserved: {[c/clipped[0] for c in clipped]} == {[g/grads[0] for g in grads]}")
```

### การตรวจจับ NaN/Inf

```python
def check_tensor(name, values):
    has_nan = any(math.isnan(v) for v in values)
    has_inf = any(math.isinf(v) for v in values)
    if has_nan or has_inf:
        print(f"WARNING {name}: nan={has_nan} inf={has_inf}")
        return False
    return True

check_tensor("good", [1.0, 2.0, 3.0])
check_tensor("bad",  [1.0, float('nan'), 3.0])
check_tensor("ugly", [1.0, float('inf'), 3.0])
```

ดู `code/numerical.py` สำหรับโค้ดเต็มที่สาธิตทุกกรณีขอบ ไฟล์ `code/numerical.ts` คือเวอร์ชัน TypeScript ที่มีฟังก์ชันและเดโมเหมือนกัน

## ส่งมอบ (Ship It)

บทนี้สร้าง:
- `code/numerical.py` ที่มี softmax, log-sum-exp และ cross-entropy แบบเสถียร การตรวจ gradient และการจำลอง mixed precision
- `outputs/prompt-numerical-debugger.md` สำหรับวินิจฉัย NaN/Inf และปัญหาเชิงตัวเลขในการเทรน

implementation ที่เสถียรเหล่านี้จะกลับมาอีกใน Phase 3 ตอนสร้างลูปการเทรน และใน Phase 4 ตอนเขียนกลไก attention

## แบบฝึกหัด

1. **การหักล้างแบบหายนะ** คำนวณความแปรปรวนของ [1000000.0, 1000001.0, 1000002.0] ด้วยสูตรตรง ๆ $\mathbb{E}[x^2] - \mathbb{E}[x]^2$ ใน float32 แล้วคำนวณอีกครั้งด้วยอัลกอริทึมแบบออนไลน์ของ Welford เทียบความคลาดเคลื่อนกับความแปรปรวนจริง (0.6667)

2. **ล่าความแม่นยำ** หาค่า float32 บวกที่เล็กที่สุด `x` ที่ทำให้ `1.0 + x == 1.0` ใน Python นี่คือ machine epsilon ตรวจว่าตรงกับ `numpy.finfo(numpy.float32).eps`

3. **กรณีขอบของ log-sum-exp** ทดสอบฟังก์ชัน `logsumexp_stable` ของคุณกับ: (a) ค่าเท่ากันทั้งหมด (b) ค่าหนึ่งใหญ่กว่าที่เหลือมาก (c) ค่าติดลบมากทั้งหมด (-1000) ตรวจว่ามันให้ผลถูกต้องในกรณีที่เวอร์ชันตรง ๆ ล้มเหลว

4. **ตรวจ gradient ของชั้นหนึ่งในโครงข่ายประสาทเทียม** เขียนชั้นเชิงเส้น `y = Wx + b` หนึ่งชั้นพร้อม backward pass เชิงวิเคราะห์ ใช้ `numerical_gradient` ตรวจความถูกต้องสำหรับเมทริกซ์น้ำหนักขนาด 3x2

5. **ทดลอง loss scaling** จำลองการเทรนด้วย float16: สร้าง gradient สุ่มในช่วง [1e-9, 1e-3] แปลงเป็น float16 แล้ววัดว่ากี่สัดส่วนกลายเป็นศูนย์ จากนั้นใช้ loss scaling (คูณด้วย 1024) แปลงเป็น float16 ปรับสเกลกลับ แล้ววัดสัดส่วนที่เป็นศูนย์อีกครั้ง

### คำใบ้

**แบบฝึกหัดที่ 1** แปลงค่าทั้งสามด้วย `np.float32` ก่อนยกกำลังสอง แล้วเรียก `variance_naive` และ `welford_variance` ค่าที่ใกล้ $10^{12}$ ใน float32 มีระยะห่างระหว่างค่าที่เก็บได้มากกว่า 1 มาก คาดว่าผลแบบตรง ๆ จะห่างจาก 0.6667 มาก และผลแบบ Welford จะใกล้

**แบบฝึกหัดที่ 2** เริ่มที่ `x = np.float32(1.0)` แล้วลดครึ่งไปเรื่อย ๆ ขณะที่ `np.float32(1.0) + x != np.float32(1.0)` เก็บทุกค่าเป็น float32 แล้วเทียบค่าสุดท้ายที่ยังเปลี่ยนผลรวมได้กับ `numpy.finfo(numpy.float32).eps` ซึ่งคือ $2^{-23}$

**แบบฝึกหัดที่ 3** ทายคำตอบแต่ละข้อก่อน สำหรับค่าที่เท่ากัน $n$ ตัวที่มีค่า $c$ ผลคือ $c + \ln n$ สำหรับค่าใหญ่ค่าเดียว ผลใกล้ค่านั้น สำหรับค่าใกล้ -1000 ผลใกล้ $-1000 + \ln n$ ขณะที่ `logsumexp_naive` คืน `-inf` เพราะ exp ทุกตัว underflow เป็น 0

**แบบฝึกหัดที่ 4** สำหรับ $y = Wx + b$ ที่มี loss $L$ gradient ของ $W$ คือผลคูณภายนอกของ gradient ที่ไหลมาจากด้านบนกับ $x$ ห่อ loss ให้เป็นฟังก์ชันของ $W$ ที่ทำให้แบนแล้ว เรียก `numerical_gradient` แล้วส่งผลทั้งสองเข้า `check_gradient`

**แบบฝึกหัดที่ 5** สุ่มขนาดบนสเกล log ด้วย `10 ** np.random.uniform(-9, -3, n)` แล้วแปลงด้วย `np.float16` float16 เก็บค่าที่ต่ำกว่าราว $6 \times 10^{-8}$ ไม่ได้ คาดว่าราวหนึ่งในสี่ของค่าจะกลายเป็นศูนย์ก่อนปรับสเกล และแทบไม่มีเลยหลังคูณด้วย 1024

## คำศัพท์สำคัญ

| คำศัพท์ | ที่คนมักพูด | ความหมายจริง |
|------|----------------|----------------------|
| IEEE 754 | "มาตรฐานของ float" | มาตรฐานสากลที่นิยามรูปแบบเลขทศนิยมฐานสอง กฎการปัดเศษ และค่าพิเศษ (inf, nan) CPU และ GPU สมัยใหม่ทุกตัวใช้มาตรฐานนี้ |
| Machine epsilon | "ขีดจำกัดความแม่นยำ" | ค่า $e$ ที่เล็กที่สุดที่ทำให้ $1.0 + e \ne 1.0$ ในรูปแบบเลขทศนิยมหนึ่ง สำหรับ float32 ประมาณ 1.19e-7 |
| Catastrophic cancellation (การหักล้างแบบหายนะ) | "เสียความแม่นยำจากการลบ" | เมื่อลบเลขทศนิยมที่เกือบเท่ากัน หลักนัยสำคัญหักล้างกัน และสัญญาณรบกวนจากการปัดเศษครอบงำผลลัพธ์ |
| Overflow (การล้น) | "ตัวเลขใหญ่เกิน" | ผลลัพธ์เกินค่ามากสุดที่เก็บได้และกลายเป็น inf exp(89) ล้น float32 |
| Underflow | "ตัวเลขเล็กเกิน" | ผลลัพธ์ใกล้ศูนย์กว่าจำนวนบวกที่เล็กที่สุดที่เก็บได้และกลายเป็น 0.0 exp(-104) underflow ใน float32 |
| Log-sum-exp trick | "ลบค่ามากสุดก่อน" | คำนวณ $\log(\sum \exp(x))$ โดยดึง $\exp(\max(x))$ ออกมาเพื่อป้องกันการล้นและ underflow ใช้ใน softmax, cross-entropy และการคำนวณ log ของความน่าจะเป็น |
| Stable softmax (softmax ที่เสถียร) | "softmax ที่ไม่ระเบิด" | ลบ $\max(\text{logits})$ ก่อนยกกำลัง exp ได้ผลเท่าเดิมเชิงตัวเลข และไม่มีทางล้น |
| Gradient checking | "ตรวจ backprop ของคุณ" | เทียบ gradient เชิงวิเคราะห์จาก backpropagation กับ gradient เชิงตัวเลขจากผลต่างจำกัดเพื่อจับบั๊กในการเขียนโค้ด |
| Mixed precision | "float16 ไปข้างหน้า float32 ย้อนกลับ" | ใช้เลขทศนิยมความแม่นยำต่ำกับการดำเนินการที่ความเร็วสำคัญ และความแม่นยำสูงกับการดำเนินการที่อ่อนไหวเชิงตัวเลข ปกติเร็วขึ้น 2-3 เท่า |
| Loss scaling | "ป้องกัน gradient underflow" | คูณ loss ด้วยค่าคงที่ขนาดใหญ่ก่อน backprop เพื่อให้ gradient อยู่ในช่วงที่ float16 เก็บได้ แล้วหารด้วยค่าคงที่เดียวกันก่อนอัปเดตน้ำหนัก |
| bfloat16 | "Brain floating point" | รูปแบบ 16 บิตของ Google ที่มีเลขชี้กำลัง 8 บิต (ช่วงเท่ากับ float32) และแมนทิสซา 7 บิต (แม่นยำน้อยกว่า float16) นิยมใช้ในการเทรน |
| Gradient clipping (การตัด gradient) | "จำกัดนอร์มของ gradient" | ปรับสเกลเวกเตอร์ gradient ให้นอร์มไม่เกินเกณฑ์ ป้องกันไม่ให้ gradient ระเบิดทำลายน้ำหนัก |
| NaN | "Not a Number" | ค่าเลขทศนิยมพิเศษจากการดำเนินการที่ไม่นิยาม (0/0, inf-inf, sqrt(-1)) แพร่ต่อไปในการคำนวณทุกครั้งหลังจากนั้น |
| Inf | "อนันต์" | ค่าเลขทศนิยมพิเศษจากการล้นหรือการหารด้วยศูนย์ รวมกันแล้วกลายเป็น NaN ได้ (inf - inf, inf * 0) |
| Numerical gradient (gradient เชิงตัวเลข) | "อนุพันธ์แบบใช้แรง" | ประมาณอนุพันธ์โดยคำนวณ $f(x+h)$ และ $f(x-h)$ แล้วหารด้วย $2h$ ช้าแต่เชื่อถือได้สำหรับการตรวจสอบ |

## อ่านเพิ่มเติม

- [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) -- เอกสารอ้างอิงที่สมบูรณ์ที่สุด อ่านยากแต่ครบถ้วน
- [Mixed Precision Training (Micikevicius et al., 2018)](https://arxiv.org/abs/1710.03740) -- เปเปอร์ของ NVIDIA ที่เสนอ loss scaling สำหรับการเทรนด้วย float16
- [AMP: Automatic Mixed Precision (PyTorch docs)](https://pytorch.org/docs/stable/amp.html) -- คู่มือใช้งานจริงเรื่อง mixed precision ใน PyTorch
- [bfloat16 format (Google Cloud TPU docs)](https://cloud.google.com/tpu/docs/bfloat16) -- ทำไม Google จึงเลือกรูปแบบนี้สำหรับ TPU
- [Kahan Summation (Wikipedia)](https://en.wikipedia.org/wiki/Kahan_summation_algorithm) -- อัลกอริทึมสำหรับลดความคลาดเคลื่อนจากการปัดเศษในการบวกเลขทศนิยม
