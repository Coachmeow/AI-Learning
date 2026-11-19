---
title: "ความน่าจะเป็นและการแจกแจง (Probability and Distributions)"
description: "ความน่าจะเป็นคือภาษาที่ AI ใช้บอกความไม่แน่นอน"
sidebar:
  label: "06 · ความน่าจะเป็นและการแจกแจง"
  order: 6
upstream_path: "phases/01-math-foundations/06-probability-and-distributions"
upstream_commit: "6a63ddb066207fca854ece311da0289295c2a313"
source_hash: "a07e78b85e86e435d4afea907e6c8fdf06c004bcc76869e0dce20d7ab3ad52ed"
---
> ความน่าจะเป็นคือภาษาที่ AI ใช้บอกความไม่แน่นอน

**ประเภท:** เรียนรู้ (Learn)
**ภาษา:** Python
**ความรู้ที่ควรมีก่อน:** Phase 1 บทที่ 01-04
**เวลา:** ~75 นาที

## สิ่งที่จะได้เรียนรู้

- เขียน PMF และ PDF ตั้งแต่ศูนย์สำหรับการแจกแจงแบบ Bernoulli, categorical, Poisson, uniform และ normal
- คำนวณค่าคาดหมายและความแปรปรวน และใช้ทฤษฎีบทลิมิตสู่ส่วนกลาง (Central Limit Theorem) อธิบายว่าทำไมการแจกแจงแบบเกาส์จึงพบได้ทั่วไป
- สร้างฟังก์ชัน softmax และ log-softmax พร้อมเทคนิคเพื่อเสถียรภาพเชิงตัวเลข (ลบ logit ที่มากที่สุดออกก่อน)
- คำนวณ cross-entropy loss จาก logits และเชื่อมโยงกับ negative log-likelihood

## ปัญหา

ตัวจำแนกให้ผลลัพธ์ `[0.03, 0.91, 0.06]` โมเดลภาษาเลือกคำถัดไปจากผู้สมัคร 50,000 คำ โมเดล diffusion สร้างภาพด้วยการสุ่มจากการแจกแจงที่เรียนรู้มา ทั้งหมดนี้คือความน่าจะเป็นที่กำลังทำงาน

ทุกคำทำนายของโมเดลคือการแจกแจงความน่าจะเป็น ทุกฟังก์ชันความสูญเสียวัดว่าการแจกแจงที่ทำนายห่างจากการแจกแจงจริงแค่ไหน ทุกก้าวของการเทรนปรับพารามิเตอร์ให้การแจกแจงหนึ่งคล้ายอีกการแจกแจงหนึ่งมากขึ้น ถ้าไม่เข้าใจความน่าจะเป็น คุณจะอ่านเปเปอร์ ML ไม่ออกสักฉบับ ดีบักโมเดลไม่ได้สักตัว และไม่เข้าใจว่าทำไม loss ของคุณกลายเป็น NaN

## แนวคิด

### เหตุการณ์ ปริภูมิตัวอย่าง และความน่าจะเป็น

ปริภูมิตัวอย่าง (sample space) $S$ คือเซตของผลลัพธ์ที่เป็นไปได้ทั้งหมด เหตุการณ์ (event) คือเซตย่อยของปริภูมิตัวอย่าง ความน่าจะเป็นจับคู่เหตุการณ์กับตัวเลขระหว่าง 0 ถึง 1

```
โยนเหรียญ:
  S = {H, T}
  P(H) = 0.5,  P(T) = 0.5

ทอยลูกเต๋าหนึ่งลูก:
  S = {1, 2, 3, 4, 5, 6}
  P(ออกเลขคู่) = P({2, 4, 6}) = 3/6 = 0.5
```

สัจพจน์สามข้อนิยามความน่าจะเป็นทั้งหมด:
1. $P(A) \ge 0$ สำหรับเหตุการณ์ $A$ ใด ๆ
2. $P(S) = 1$ (ต้องมีอะไรสักอย่างเกิดขึ้นเสมอ)
3. $P(A \text{ or } B) = P(A) + P(B)$ เมื่อ $A$ และ $B$ เกิดพร้อมกันไม่ได้

ที่เหลือทั้งหมด (ทฤษฎีบทของเบย์ ค่าคาดหมาย การแจกแจง) ตามมาจากกฎสามข้อนี้

### ความน่าจะเป็นแบบมีเงื่อนไขและความเป็นอิสระ

$P(A \mid B)$ คือความน่าจะเป็นของ $A$ เมื่อรู้ว่า $B$ เกิดขึ้นแล้ว

```
P(A|B) = P(A and B) / P(B)

ตัวอย่าง: สำรับไพ่
  P(King | ไพ่หน้าคน) = P(King และ ไพ่หน้าคน) / P(ไพ่หน้าคน)
                      = (4/52) / (12/52)
                      = 4/12 = 1/3
```

เหตุการณ์สองอย่างเป็นอิสระต่อกันเมื่อการรู้อย่างหนึ่งไม่ได้บอกอะไรเกี่ยวกับอีกอย่างเลย:

```math
\begin{aligned}
\text{Independent:} \quad & P(A \mid B) = P(A) \\
\text{Equivalent to:} \quad & P(A \text{ and } B) = P(A) \cdot P(B)
\end{aligned}
```

(บรรทัดแรกคือนิยามของความเป็นอิสระ บรรทัดที่สองคือเงื่อนไขที่สมมูลกัน)

การโยนเหรียญแต่ละครั้งเป็นอิสระต่อกัน การจั่วไพ่โดยไม่ใส่คืนไม่เป็นอิสระ

### ฟังก์ชันมวลความน่าจะเป็น (PMF) กับฟังก์ชันความหนาแน่นความน่าจะเป็น (PDF)

ตัวแปรสุ่มไม่ต่อเนื่องมีฟังก์ชันมวลความน่าจะเป็น (probability mass function, PMF) ผลลัพธ์แต่ละแบบมีความน่าจะเป็นเฉพาะตัวที่อ่านได้ตรง ๆ

```
PMF: P(X = k)

ลูกเต๋าที่เที่ยงตรง:
  P(X = 1) = 1/6
  P(X = 2) = 1/6
  ...
  P(X = 6) = 1/6

  ผลรวมของความน่าจะเป็นทั้งหมด = 1
```

ตัวแปรสุ่มต่อเนื่องมีฟังก์ชันความหนาแน่นความน่าจะเป็น (probability density function, PDF) ความหนาแน่นที่จุดเดียวไม่ใช่ความน่าจะเป็น ความน่าจะเป็นได้จากการหาปริพันธ์ของความหนาแน่นบนช่วงหนึ่ง

```
PDF: f(x)

P(a <= X <= b) = ปริพันธ์ของ f(x) จาก a ถึง b

f(x) มากกว่า 1 ได้ (เป็นความหนาแน่น ไม่ใช่ความน่าจะเป็น)
ปริพันธ์ของ f(x) dx จาก -inf ถึง +inf = 1
```

ความต่างนี้สำคัญใน ML ผลลัพธ์ของการจำแนกเป็น PMF (ตัวเลือกไม่ต่อเนื่อง) ส่วน latent space ของ VAE ใช้ PDF (ต่อเนื่อง)

### การแจกแจงที่พบบ่อย

**Bernoulli:** ทดลองครั้งเดียว มีสองผลลัพธ์ ใช้แทนการจำแนกสองกลุ่ม (binary classification)

```math
\begin{aligned}
P(X = 1) &= p \\
P(X = 0) &= 1 - p \\
\text{Mean} = p, &\quad \text{Variance} = p(1-p)
\end{aligned}
```

**Categorical:** ทดลองครั้งเดียว มี $k$ ผลลัพธ์ ใช้แทนการจำแนกหลายกลุ่ม (ผลลัพธ์ของ softmax)

```math
\begin{aligned}
& P(X = i) = p_i, \quad \text{where } \textstyle\sum_i p_i = 1 \\
& \text{Example: } P(\text{cat}) = 0.7, \quad P(\text{dog}) = 0.2, \quad P(\text{bird}) = 0.1
\end{aligned}
```

**Uniform (สม่ำเสมอ):** ทุกผลลัพธ์มีโอกาสเท่ากัน ใช้ในการกำหนดค่าเริ่มต้นแบบสุ่ม

```math
\begin{aligned}
\text{Discrete:} \quad & P(X = k) = 1/n \text{ for } k \in \lbrace 1, \ldots, n \rbrace \\
\text{Continuous:} \quad & f(x) = 1/(b-a) \text{ for } x \in [a, b]
\end{aligned}
```

**Normal (ปกติ หรือแบบเกาส์):** เส้นโค้งรูประฆัง กำหนดด้วยค่าเฉลี่ย ($\mu$) และความแปรปรวน ($\sigma^2$)

```
f(x) = (1 / sqrt(2*pi*sigma^2)) * exp(-(x - mu)^2 / (2*sigma^2))

การแจกแจงปกติมาตรฐาน: mu = 0, sigma = 1
  ข้อมูล 68% อยู่ภายใน 1 sigma
  95% อยู่ภายใน 2 sigma
  99.7% อยู่ภายใน 3 sigma
```

**Poisson:** จำนวนครั้งของเหตุการณ์ที่เกิดน้อยในช่วงเวลาคงที่ ใช้แทนอัตราการเกิดเหตุการณ์

```math
\begin{aligned}
P(X = k) &= \frac{\lambda^k e^{-\lambda}}{k!} \\
\text{Mean} = \lambda, &\quad \text{Variance} = \lambda
\end{aligned}
```

### ค่าคาดหมายและความแปรปรวน

ค่าคาดหมาย (expected value) คือค่าเฉลี่ยของผลลัพธ์ที่ถ่วงน้ำหนักด้วยความน่าจะเป็น

```math
\begin{aligned}
\text{Discrete:} \quad & \mathbb{E}[X] = \sum_i x_i \, P(X = x_i) \\
\text{Continuous:} \quad & \mathbb{E}[X] = \int x \, f(x) \, dx
\end{aligned}
```

ความแปรปรวน (variance) วัดการกระจายรอบค่าเฉลี่ย

```math
\begin{aligned}
\mathrm{Var}(X) &= \mathbb{E}[(X - \mathbb{E}[X])^2] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 \\
\text{Standard deviation} &= \sqrt{\mathrm{Var}(X)}
\end{aligned}
```

(Standard deviation คือส่วนเบี่ยงเบนมาตรฐาน)

ใน ML ค่าคาดหมายปรากฏในรูปฟังก์ชันความสูญเสีย (loss เฉลี่ยบนการแจกแจงของข้อมูล) ความแปรปรวนบอกเรื่องเสถียรภาพของโมเดล gradient ที่ความแปรปรวนสูงแปลว่าการเทรนมีสัญญาณรบกวนมาก

### การแจกแจงร่วมและการแจกแจงส่วนขอบ

การแจกแจงร่วม (joint distribution) $P(X, Y)$ บรรยายตัวแปรสุ่มสองตัวไปพร้อมกัน

ตัวอย่าง PMF ร่วม ($X$ = สภาพอากาศ, $Y$ = ร่ม):

| | $Y=0$ (ไม่พกร่ม) | $Y=1$ (พกร่ม) | ส่วนขอบ $P(X)$ |
|---|---|---|---|
| $X=0$ (แดดออก) | 0.40 | 0.10 | $P(X=0) = 0.50$ |
| $X=1$ (ฝนตก) | 0.05 | 0.45 | $P(X=1) = 0.50$ |
| **ส่วนขอบ $P(Y)$** | $P(Y=0) = 0.45$ | $P(Y=1) = 0.55$ | 1.00 |

การแจกแจงส่วนขอบ (marginal distribution) ได้จากการรวมตัวแปรอีกตัวออกไป:

```math
P(X = x) = \sum_{y} P(X = x, Y = y)
```

ผลรวมแถวและคอลัมน์ในตารางด้านบนคือการแจกแจงส่วนขอบ

### ทำไมการแจกแจงปกติจึงโผล่มาทุกที่

ทฤษฎีบทลิมิตสู่ส่วนกลาง (Central Limit Theorem): ค่าเฉลี่ยของตัวแปรสุ่มอิสระจำนวนมากจากการแจกแจงเดียวกัน เมื่อนำมาจัดให้อยู่กึ่งกลางและปรับสเกลด้วย $\sqrt{n}$ จะเข้าใกล้การแจกแจงปกติ ไม่ว่าการแจกแจงตั้งต้นจะมีรูปร่างอย่างไร ขอแค่ความแปรปรวนมีค่าจำกัด ผลรวมที่จัดให้อยู่กึ่งกลางและปรับสเกลแล้วก็เป็นแบบเดียวกัน

```
ทอยลูกเต๋า 1 ลูก:  การแจกแจงสม่ำเสมอ (แบนราบ)
ค่าเฉลี่ยของลูกเต๋า 2 ลูก:  รูปสามเหลี่ยม (มียอด)
ค่าเฉลี่ยของลูกเต๋า 30 ลูก: เกือบเป็นระฆังสมบูรณ์

ใช้ได้กับการแจกแจงตั้งต้นทุกแบบที่ความแปรปรวนมีค่าจำกัด
```

นี่คือเหตุผลที่:
- ความคลาดเคลื่อนของการวัดมีการแจกแจงใกล้เคียงปกติ (มาจากแหล่งเล็ก ๆ อิสระจำนวนมาก)
- การกำหนดค่าเริ่มต้นของน้ำหนักในโครงข่ายประสาทเทียมใช้การแจกแจงปกติ
- สัญญาณรบกวนของ gradient ใน SGD ใกล้เคียงการแจกแจงปกติ (เป็นผลรวมของ gradient จากตัวอย่างจำนวนมาก)
- การแจกแจงปกติเป็นการแจกแจงที่มีเอนโทรปีสูงสุดเมื่อกำหนดค่าเฉลี่ยและความแปรปรวน

### ลอการิทึมของความน่าจะเป็น (Log Probabilities)

ความน่าจะเป็นดิบ ๆ ก่อปัญหาเชิงตัวเลข การคูณความน่าจะเป็นเล็ก ๆ หลายตัวเข้าด้วยกันทำให้ค่าลดลงจนกลายเป็นศูนย์ (underflow) อย่างรวดเร็ว

```math
\begin{aligned}
P(\text{sentence}) &= P(\text{word}_1) \cdot P(\text{word}_2) \cdot \ldots \cdot P(\text{word}_n) \\
&= 0.01 \cdot 0.003 \cdot 0.02 \cdot \ldots \\
&\to 0.0 \quad \text{(underflow after } \sim 30 \text{ terms)}
\end{aligned}
```

(ค่าจะ underflow กลายเป็นศูนย์หลังผ่านไปราว 30 พจน์)

ลอการิทึมของความน่าจะเป็นแก้ปัญหานี้ได้ การคูณกลายเป็นการบวก

```math
\begin{aligned}
\log P(\text{sentence}) &= \log P(\text{word}_1) + \log P(\text{word}_2) + \ldots + \log P(\text{word}_n) \\
&= -4.6 + -5.8 + -3.9 + \ldots \\
&\to \text{finite number (no underflow)}
\end{aligned}
```

(ผลลัพธ์เป็นตัวเลขจำกัด ไม่ underflow)

กฎ:
- $\log(a \cdot b) = \log(a) + \log(b)$
- log ของความน่าจะเป็นมีค่า $\le 0$ เสมอ (เพราะ $0 < P \le 1$)
- ยิ่งติดลบมาก ยิ่งมีโอกาสน้อย
- Cross-entropy loss คือค่าลบของ log ความน่าจะเป็นของคลาสที่ถูกต้อง

### Softmax ในฐานะการแจกแจงความน่าจะเป็น

โครงข่ายประสาทเทียมให้คะแนนดิบ (logits) ออกมา softmax แปลงคะแนนเหล่านั้นให้เป็นการแจกแจงความน่าจะเป็นที่ถูกต้อง

```
softmax(z_i) = exp(z_i) / sum(exp(z_j) for all j)

สมบัติ:
  - ผลลัพธ์ทุกตัวอยู่ในช่วง (0, 1)
  - ผลลัพธ์ทั้งหมดรวมกันได้ 1
  - รักษาลำดับเดิมของขาเข้า
  - exp() ขยายความต่างระหว่าง logits
```

เทคนิคของ softmax: ลบ logit ที่มากที่สุดออกก่อนยกกำลัง exp เพื่อป้องกันการล้น (overflow)

```
z = [100, 101, 102]
exp(102) = ล้น

z_shifted = z - max(z) = [-2, -1, 0]
exp(0) = 1  (ปลอดภัย)

ได้ผลเท่าเดิม และไม่ล้น
```

Log-softmax รวม softmax กับ log เข้าด้วยกันเพื่อเสถียรภาพเชิงตัวเลข PyTorch ใช้สิ่งนี้ภายใน cross-entropy loss

### การสุ่มตัวอย่าง (Sampling)

การสุ่มตัวอย่างคือการดึงค่าสุ่มจากการแจกแจง ใน ML:
- Dropout สุ่มเลือกว่านิวรอนตัวไหนจะถูกตั้งเป็นศูนย์
- Data augmentation สุ่มการแปลงต่าง ๆ
- โมเดลภาษาสุ่มโทเค็นถัดไปจากการแจกแจงที่ทำนาย
- โมเดล diffusion สุ่มสัญญาณรบกวนแล้วค่อย ๆ ลดสัญญาณรบกวนออก

การสุ่มจากการแจกแจงใด ๆ ต้องใช้เทคนิคอย่าง inverse transform sampling, rejection sampling หรือ reparameterization trick (ใช้ใน VAE)

```figure
gaussian-pdf
```

## ลงมือสร้าง (Build It)

### ขั้นที่ 1: พื้นฐานความน่าจะเป็น

```python
import math
import random

def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def combinations(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def conditional_probability(p_a_and_b, p_b):
    return p_a_and_b / p_b

p_king_given_face = conditional_probability(4/52, 12/52)
print(f"P(King | Face card) = {p_king_given_face:.4f}")
```

### ขั้นที่ 2: PMF และ PDF ตั้งแต่ศูนย์

```python
def bernoulli_pmf(k, p):
    return p if k == 1 else (1 - p)

def categorical_pmf(k, probs):
    return probs[k]

def poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / factorial(k)

def uniform_pdf(x, a, b):
    if a <= x <= b:
        return 1.0 / (b - a)
    return 0.0

def normal_pdf(x, mu, sigma):
    coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)
```

### ขั้นที่ 3: ค่าคาดหมายและความแปรปรวน

```python
def expected_value(values, probabilities):
    return sum(v * p for v, p in zip(values, probabilities))

def variance(values, probabilities):
    mu = expected_value(values, probabilities)
    return sum(p * (v - mu) ** 2 for v, p in zip(values, probabilities))

die_values = [1, 2, 3, 4, 5, 6]
die_probs = [1/6] * 6
mu = expected_value(die_values, die_probs)
var = variance(die_values, die_probs)
print(f"Die: E[X] = {mu:.4f}, Var(X) = {var:.4f}, SD = {var**0.5:.4f}")
```

### ขั้นที่ 4: สุ่มตัวอย่างจากการแจกแจง

```python
def sample_bernoulli(p, n=1):
    return [1 if random.random() < p else 0 for _ in range(n)]

def sample_categorical(probs, n=1):
    cumulative = []
    total = 0
    for p in probs:
        total += p
        cumulative.append(total)
    samples = []
    for _ in range(n):
        r = random.random()
        for i, c in enumerate(cumulative):
            if r <= c:
                samples.append(i)
                break
    return samples

def sample_normal_box_muller(mu, sigma, n=1):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mu + sigma * z)
    return samples
```

### ขั้นที่ 5: Softmax และ log ของความน่าจะเป็น

```python
def softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    exps = [math.exp(z) for z in shifted]
    total = sum(exps)
    return [e / total for e in exps]

def log_softmax(logits):
    max_logit = max(logits)
    shifted = [z - max_logit for z in logits]
    log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
    return [z - log_sum_exp for z in logits]

def cross_entropy_loss(logits, target_index):
    log_probs = log_softmax(logits)
    return -log_probs[target_index]
```

### ขั้นที่ 6: สาธิตทฤษฎีบทลิมิตสู่ส่วนกลาง

```python
def demonstrate_clt(dist_fn, n_samples, n_averages):
    averages = []
    for _ in range(n_averages):
        samples = [dist_fn() for _ in range(n_samples)]
        averages.append(sum(samples) / len(samples))
    return averages
```

### ขั้นที่ 7: แสดงผลเป็นภาพ

```python
import matplotlib.pyplot as plt

xs = [mu + sigma * (i - 500) / 100 for i in range(1001)]
ys = [normal_pdf(x, mu, sigma) for x, mu, sigma in ...]
plt.plot(xs, ys)
```

โค้ดเต็มพร้อมภาพทั้งหมดอยู่ใน `code/probability.py`

## นำไปใช้ (Use It)

ด้วย NumPy และ SciPy ทุกอย่างข้างบนเหลือแค่บรรทัดเดียว:

```python
import numpy as np
from scipy import stats

normal = stats.norm(loc=0, scale=1)
samples = normal.rvs(size=10000)
print(f"Mean: {np.mean(samples):.4f}, Std: {np.std(samples):.4f}")
print(f"P(X < 1.96) = {normal.cdf(1.96):.4f}")

logits = np.array([2.0, 1.0, 0.1])
from scipy.special import softmax, log_softmax
probs = softmax(logits)
log_probs = log_softmax(logits)
print(f"Softmax: {probs}")
print(f"Log-softmax: {log_probs}")
```

คุณสร้างสิ่งเหล่านี้เองตั้งแต่ศูนย์แล้ว ตอนนี้คุณรู้ว่าฟังก์ชันในไลบรารีทำอะไรอยู่

## แบบฝึกหัด

1. เขียน inverse transform sampling สำหรับการแจกแจงแบบเลขชี้กำลัง (exponential) ตรวจโดยสุ่ม 10,000 ค่าแล้วเทียบฮิสโทแกรมกับ PDF จริง

2. สร้างตารางการแจกแจงร่วมของลูกเต๋าถ่วงน้ำหนักสองลูก คำนวณการแจกแจงส่วนขอบ และตรวจว่าลูกเต๋าทั้งสองเป็นอิสระต่อกันหรือไม่

3. คำนวณ cross-entropy loss ของตัวจำแนก 5 คลาสที่ให้ logits `[2.0, 0.5, -1.0, 3.0, 0.1]` เมื่อคลาสที่ถูกต้องคือ index 3 แล้วตรวจคำตอบด้วย `nn.CrossEntropyLoss` ของ PyTorch

4. เขียนฟังก์ชันที่รับรายการ log ของความน่าจะเป็น แล้วคืนลำดับที่มีโอกาสมากที่สุด log ความน่าจะเป็นรวม และความน่าจะเป็นดิบที่เทียบเท่า ทดสอบกับประโยค 50 คำที่แต่ละคำมีความน่าจะเป็น 0.01

### คำใบ้

**แบบฝึกหัดที่ 1** สุ่ม `u` จากการแจกแจงสม่ำเสมอแล้วคืน $-\ln(1 - u) / \lambda$ ตรวจว่าค่าเฉลี่ยของตัวอย่างใกล้ $1/\lambda$ และแท่งฮิสโทแกรมเป็นไปตาม $\lambda e^{-\lambda x}$

**แบบฝึกหัดที่ 2** เติมตาราง 6x6 ที่ทุกช่องเป็นความน่าจะเป็นและผลรวมทุกช่องเท่ากับ 1 แล้วเรียก `joint_to_marginals` ใช้ `check_independence`: ลูกเต๋าเป็นอิสระต่อกันก็ต่อเมื่อทุกช่องเท่ากับผลคูณของส่วนขอบทั้งสองของช่องนั้น

**แบบฝึกหัดที่ 3** ใส่ `softmax` ให้ logits แล้วหา $-\ln$ ของความน่าจะเป็นที่ index 3 ผลลัพธ์ต้องใกล้ 0.421 ซึ่งเป็นค่าที่ `nn.CrossEntropyLoss` ให้สำหรับ logits และ target เดียวกัน

**แบบฝึกหัดที่ 4** บวก log ของความน่าจะเป็นเข้าด้วยกัน อย่าคูณความน่าจะเป็นดิบ สำหรับ 50 คำที่ความน่าจะเป็น 0.01 ผลรวมต้องเป็น $50 \ln(0.01) \approx -230.26$ และความน่าจะเป็นดิบคือ $10^{-100}$

## คำศัพท์สำคัญ

| คำศัพท์ | ที่คนมักพูด | ความหมายจริง |
|------|----------------|----------------------|
| Sample space (ปริภูมิตัวอย่าง) | "ความเป็นไปได้ทั้งหมด" | เซต $S$ ของผลลัพธ์ที่เป็นไปได้ทุกแบบของการทดลอง |
| PMF | "ฟังก์ชันความน่าจะเป็น" | ฟังก์ชันที่ให้ความน่าจะเป็นที่แน่นอนของผลลัพธ์ไม่ต่อเนื่องแต่ละแบบ รวมกันได้ 1 |
| PDF | "เส้นโค้งความน่าจะเป็น" | ฟังก์ชันความหนาแน่นสำหรับตัวแปรต่อเนื่อง ต้องหาปริพันธ์บนช่วงหนึ่งจึงจะได้ความน่าจะเป็น |
| Conditional probability (ความน่าจะเป็นแบบมีเงื่อนไข) | "ความน่าจะเป็นเมื่อรู้อะไรบางอย่าง" | $P(A \mid B) = P(A \text{ and } B) / P(B)$ เป็นรากฐานของการคิดแบบเบย์และทฤษฎีบทของเบย์ |
| Independence (ความเป็นอิสระ) | "ไม่ส่งผลต่อกัน" | $P(A \text{ and } B) = P(A) \cdot P(B)$ การรู้เหตุการณ์หนึ่งไม่ได้บอกอะไรเกี่ยวกับอีกเหตุการณ์ |
| Expected value (ค่าคาดหมาย) | "ค่าเฉลี่ย" | ผลรวมของผลลัพธ์ทั้งหมดที่ถ่วงน้ำหนักด้วยความน่าจะเป็น ฟังก์ชันความสูญเสียก็คือค่าคาดหมาย |
| Variance (ความแปรปรวน) | "กระจายแค่ไหน" | ค่าคาดหมายของกำลังสองของระยะห่างจากค่าเฉลี่ย ความแปรปรวนสูง = ค่าประมาณมีสัญญาณรบกวนและไม่เสถียร |
| Normal distribution (การแจกแจงปกติ) | "เส้นโค้งระฆัง" | $f(x) = (1/\sqrt{2\pi\sigma^2}) \cdot \exp(-(x-\mu)^2/(2\sigma^2))$ ปรากฏทุกที่เพราะ CLT |
| Central Limit Theorem (ทฤษฎีบทลิมิตสู่ส่วนกลาง) | "ค่าเฉลี่ยกลายเป็นการแจกแจงปกติ" | ค่าเฉลี่ยของตัวอย่างอิสระจำนวนมากที่จัดให้อยู่กึ่งกลางและปรับสเกลแล้ว ลู่เข้าสู่การแจกแจงปกติ สำหรับแหล่งใดก็ได้ที่ความแปรปรวนมีค่าจำกัด |
| Joint distribution (การแจกแจงร่วม) | "ตัวแปรสองตัวพร้อมกัน" | $P(X, Y)$ บรรยายความน่าจะเป็นของผลลัพธ์ $X$ และ $Y$ ทุกคู่ |
| Marginal distribution (การแจกแจงส่วนขอบ) | "รวมตัวแปรอีกตัวออกไป" | $P(X) = \sum_y P(X, Y)$ ได้การแจกแจงของตัวแปรตัวเดียวกลับมาจากการแจกแจงร่วม |
| Log probability | "log ของความน่าจะเป็น" | $\log P(x)$ เปลี่ยนผลคูณเป็นผลบวก ป้องกัน underflow เชิงตัวเลขในลำดับยาว ๆ |
| Softmax | "เปลี่ยนคะแนนเป็นความน่าจะเป็น" | $\text{softmax}(z_i) = \exp(z_i) / \sum_j \exp(z_j)$ จับคู่ logits ที่เป็นจำนวนจริงไปเป็นการแจกแจงความน่าจะเป็นที่ถูกต้อง |
| Cross-entropy | "ฟังก์ชันความสูญเสีย" | $-\sum p_{\text{true}} \cdot \log(p_{\text{predicted}})$ วัดว่าการแจกแจงสองแบบต่างกันแค่ไหน ยิ่งต่ำยิ่งดี |
| Logits | "ผลลัพธ์ดิบของโมเดล" | คะแนนที่ยังไม่ทำให้เป็นมาตรฐานก่อนเข้า softmax ตั้งชื่อตามฟังก์ชัน logistic |
| Sampling (การสุ่มตัวอย่าง) | "ดึงค่าสุ่ม" | การสร้างค่าตามการแจกแจงความน่าจะเป็น เป็นวิธีที่โมเดลสร้างผลลัพธ์ |

## อ่านเพิ่มเติม

- [3Blue1Brown: But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) - พิสูจน์เชิงภาพว่าทำไมค่าเฉลี่ยจึงกลายเป็นการแจกแจงปกติ
- [Stanford CS229 Probability Review](https://cs229.stanford.edu/section/cs229-prob.pdf) - สรุปกระชับที่ครอบคลุมทุกเรื่องในบทนี้และมากกว่านั้น
- [The Log-Sum-Exp Trick](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/) - ทำไมเสถียรภาพเชิงตัวเลขจึงสำคัญ และทำได้อย่างไร
