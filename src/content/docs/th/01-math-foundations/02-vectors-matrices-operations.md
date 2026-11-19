---
title: "เวกเตอร์ เมทริกซ์ และการดำเนินการ (Vectors, Matrices & Operations)"
description: "โครงข่ายประสาทเทียมทุกตัวก็คือการคูณเมทริกซ์ที่มีขั้นตอนเพิ่มอีกนิด"
sidebar:
  label: "02 · เวกเตอร์ เมทริกซ์ และการดำเนินการ"
  order: 2
upstream_path: "phases/01-math-foundations/02-vectors-matrices-operations"
upstream_commit: "6a63ddb066207fca854ece311da0289295c2a313"
source_hash: "a5849d742948a87e8ef7c6eb919df6acea0a3808ef61fe27414e9618b4dfb8ea"
---
> โครงข่ายประสาทเทียมทุกตัวก็คือการคูณเมทริกซ์ที่มีขั้นตอนเพิ่มอีกนิด

**ประเภท:** ลงมือสร้าง (Build)
**ภาษา:** Python, Julia
**ความรู้ที่ควรมีก่อน:** Phase 1 บทที่ 01 (พีชคณิตเชิงเส้นแบบเข้าใจภาพ)
**เวลา:** ~60 นาที

## สิ่งที่จะได้เรียนรู้

- สร้างคลาส Matrix ที่มีการดำเนินการทีละสมาชิก (element-wise), การคูณเมทริกซ์, transpose, ดีเทอร์มิแนนต์ และเมทริกซ์ผกผัน
- แยกการคูณทีละสมาชิกออกจากการคูณเมทริกซ์ และอธิบายได้ว่าเมื่อไรใช้แบบไหน
- เขียนชั้น dense ของโครงข่ายประสาทเทียมหนึ่งชั้น (`relu(W @ x + b)`) ด้วยคลาส Matrix ที่สร้างเองเท่านั้น
- อธิบายกฎของ broadcasting และการบวก bias ในเฟรมเวิร์กของโครงข่ายประสาทเทียม

## ปัญหา

คุณอยากสร้างโครงข่ายประสาทเทียม เปิดโค้ดมาอ่านแล้วเจอบรรทัดนี้:

```
output = activation(weights @ input + bias)
```

`@` คือการคูณเมทริกซ์ `weights` คือเมทริกซ์ `input` คือเวกเตอร์ ถ้าคุณไม่รู้ว่าการดำเนินการเหล่านี้ทำอะไร บรรทัดนี้ก็เป็นเวทมนตร์ แต่ถ้ารู้ มันคือ forward pass ทั้งหมดของชั้นหนึ่งชั้นในการดำเนินการสามอย่าง

ทุกภาพที่โมเดลของคุณประมวลผลคือเมทริกซ์ของค่าพิกเซล ทุก embedding ของคำคือเวกเตอร์ ทุกชั้นของทุกโครงข่ายประสาทเทียมคือการแปลงด้วยเมทริกซ์ คุณสร้างระบบ AI ไม่ได้ถ้าไม่คล่องการดำเนินการกับเมทริกซ์ เหมือนที่เขียนโค้ดไม่ได้ถ้าไม่เข้าใจตัวแปร

บทนี้สร้างความคล่องนั้นตั้งแต่ศูนย์

## แนวคิด

### เวกเตอร์: รายการตัวเลขที่มีลำดับ

เวกเตอร์คือรายการตัวเลขที่มีทิศทางและขนาด ใน AI เวกเตอร์ใช้แทนจุดข้อมูล feature หรือพารามิเตอร์

```
v = [3, 4]        -- a 2D vector
w = [1, 0, -2]    -- a 3D vector
```

เวกเตอร์ 2 มิติ `[3, 4]` ชี้ไปที่พิกัด (3, 4) บนระนาบ ความยาว (ขนาด) ของมันคือ 5 (สามเหลี่ยม 3-4-5)

### เมทริกซ์: ตารางของตัวเลข

เมทริกซ์คือตาราง 2 มิติ มีแถวและคอลัมน์ เมทริกซ์ขนาด $m \times n$ มี $m$ แถวและ $n$ คอลัมน์

```math
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \quad \text{2x3 matrix (2 rows, 3 columns)}
```

ในโครงข่ายประสาทเทียม เมทริกซ์น้ำหนักแปลงเวกเตอร์ขาเข้าเป็นเวกเตอร์ขาออก ชั้นที่มีข้อมูลขาเข้า 784 ตัวและขาออก 128 ตัวใช้เมทริกซ์น้ำหนักขนาด 128x784

### ทำไม shape จึงสำคัญ

การคูณเมทริกซ์มีกฎเข้มงวด: `(m x n) @ (n x p) = (m x p)` มิติด้านในต้องเท่ากัน

```
(128 x 784) @ (784 x 1) = (128 x 1)
  weights       input       output

Inner dimensions: 784 = 784  -- valid
```

ถ้าคุณเจอ error เรื่อง shape ไม่ตรงกันใน PyTorch นี่คือสาเหตุ

### แผนที่ของการดำเนินการ

| การดำเนินการ | ทำอะไร | ใช้ในโครงข่ายประสาทเทียม |
|-----------|-------------|-------------------|
| การบวก | รวมกันทีละสมาชิก | บวก bias เข้ากับผลลัพธ์ |
| การคูณสเกลาร์ | ปรับขนาดทุกสมาชิก | learning rate * เกรเดียนต์ |
| การคูณเมทริกซ์ | แปลงเวกเตอร์ | forward pass ของชั้น |
| Transpose | สลับแถวกับคอลัมน์ | backpropagation |
| ดีเทอร์มิแนนต์ | ตัวเลขเดียวที่สรุปเมทริกซ์ | ตรวจว่าหาเมทริกซ์ผกผันได้หรือไม่ |
| เมทริกซ์ผกผัน | ย้อนการแปลง | แก้ระบบสมการเชิงเส้น |
| เมทริกซ์เอกลักษณ์ | เมทริกซ์ที่ไม่ทำอะไร | การกำหนดค่าเริ่มต้น, residual connection |

### การคูณทีละสมาชิกกับการคูณเมทริกซ์

ความต่างนี้ทำให้มือใหม่สะดุดอยู่ตลอด

การคูณทีละสมาชิก (element-wise): คูณตำแหน่งที่ตรงกัน เมทริกซ์ทั้งสองต้องมี shape เดียวกัน

```math
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} * \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix} = \begin{bmatrix} 5 & 12 \\ 21 & 32 \end{bmatrix}
```

การคูณเมทริกซ์: dot product ของแถวกับคอลัมน์ มิติด้านในต้องเท่ากัน

```math
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} @ \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix} = \begin{bmatrix} 1 \cdot 5 + 2 \cdot 7 & 1 \cdot 6 + 2 \cdot 8 \\ 3 \cdot 5 + 4 \cdot 7 & 3 \cdot 6 + 4 \cdot 8 \end{bmatrix} = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}
```

การดำเนินการต่างกัน ผลลัพธ์ต่างกัน กฎก็ต่างกัน

### Broadcasting

เมื่อบวกเวกเตอร์ bias เข้ากับเมทริกซ์ของผลลัพธ์ shape จะไม่ตรงกัน broadcasting ยืด array ที่เล็กกว่าให้พอดี

```
| 1  2  3 |   +   [10, 20, 30]
| 4  5  6 |

Broadcasting stretches the vector across rows:

| 1  2  3 |   | 10  20  30 |   | 11  22  33 |
| 4  5  6 | + | 10  20  30 | = | 14  25  36 |
```

(broadcasting ยืดเวกเตอร์ไปตามทุกแถว)

เฟรมเวิร์กสมัยใหม่ทุกตัวทำให้อัตโนมัติ การเข้าใจเรื่องนี้ช่วยไม่ให้งงเวลาที่ shape ดูผิดแต่โค้ดกลับรันได้

```figure
vector-projection
```

## ลงมือสร้าง (Build It)

### ขั้นที่ 1: คลาส Vector

```python
class Vector:
    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __repr__(self):
        return f"Vector({self.data})"

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar):
        return Vector([x * scalar for x in self.data])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.data, other.data))

    def magnitude(self):
        return sum(x ** 2 for x in self.data) ** 0.5
```

### ขั้นที่ 2: คลาส Matrix พร้อมการดำเนินการหลัก

```python
class Matrix:
    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)

    def __repr__(self):
        rows_str = "\n  ".join(str(row) for row in self.data)
        return f"Matrix({self.shape}):\n  {rows_str}"

    def __add__(self, other):
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other):
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scalar_multiply(self, scalar):
        return Matrix([
            [self.data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def element_wise_multiply(self, other):
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def matmul(self, other):
        return Matrix([
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ])

    def transpose(self):
        return Matrix([
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ])

    def determinant(self):
        if self.shape == (1, 1):
            return self.data[0][0]
        if self.shape == (2, 2):
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for j in range(self.cols):
            minor = Matrix([
                [self.data[i][k] for k in range(self.cols) if k != j]
                for i in range(1, self.rows)
            ])
            det += ((-1) ** j) * self.data[0][j] * minor.determinant()
        return det

    def inverse_2x2(self):
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular, no inverse exists")
        return Matrix([
            [self.data[1][1] / det, -self.data[0][1] / det],
            [-self.data[1][0] / det, self.data[0][0] / det]
        ])

    @staticmethod
    def identity(n):
        return Matrix([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])
```

### ขั้นที่ 3: ดูมันทำงาน

```python
A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])

print("A + B =", (A + B).data)
print("A @ B =", A.matmul(B).data)
print("A^T =", A.transpose().data)
print("det(A) =", A.determinant())
print("A^-1 =", A.inverse_2x2().data)

I = Matrix.identity(2)
print("A @ A^-1 =", A.matmul(A.inverse_2x2()).data)
```

### ขั้นที่ 4: เชื่อมกับโครงข่ายประสาทเทียม

```python
import random

inputs = Matrix([[0.5], [0.8], [0.2]])
weights = Matrix([
    [random.uniform(-1, 1) for _ in range(3)]
    for _ in range(2)
])
bias = Matrix([[0.1], [0.1]])

def relu_matrix(m):
    return Matrix([[max(0, val) for val in row] for row in m.data])

pre_activation = weights.matmul(inputs) + bias
output = relu_matrix(pre_activation)

print(f"Input shape: {inputs.shape}")
print(f"Weight shape: {weights.shape}")
print(f"Output shape: {output.shape}")
print(f"Output: {output.data}")
```

นี่คือชั้น dense หนึ่งชั้น: `output = relu(W @ x + b)` ทุกชั้น dense ในทุกโครงข่ายประสาทเทียมทำแบบนี้ทุกประการ

## นำไปใช้ (Use It)

NumPy ทำทุกอย่างข้างบนได้ในโค้ดที่สั้นกว่า และเร็วกว่าหลายระดับ

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A + B =\n", A + B)
print("A * B (element-wise) =\n", A * B)
print("A @ B (matrix multiply) =\n", A @ B)
print("A^T =\n", A.T)
print("det(A) =", np.linalg.det(A))
print("A^-1 =\n", np.linalg.inv(A))
print("I =\n", np.eye(2))

inputs = np.random.randn(3, 1)
weights = np.random.randn(2, 3)
bias = np.array([[0.1], [0.1]])
output = np.maximum(0, weights @ inputs + bias)

print(f"\nNeural network layer: {weights.shape} @ {inputs.shape} = {output.shape}")
print(f"Output:\n{output}")
```

ตัวดำเนินการ `@` ใน Python เรียก `__matmul__` ซึ่ง NumPy ใช้ routine ของ BLAS ที่ปรับแต่งมาแล้ว เขียนด้วย C และ Fortran คณิตศาสตร์เดียวกัน แต่เร็วกว่า 100 เท่า

Broadcasting ใน NumPy:

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
bias = np.array([10, 20, 30])
print(matrix + bias)
```

NumPy broadcast bias แบบ 1 มิติไปทั้งสองแถวให้อัตโนมัติ นี่คือวิธีที่การบวก bias ทำงานในทุกเฟรมเวิร์กของโครงข่ายประสาทเทียม

## ส่งมอบ (Ship It)

บทนี้ได้ prompt สำหรับสอนการดำเนินการกับเมทริกซ์ผ่านความเข้าใจเชิงเรขาคณิต ดู `outputs/prompt-matrix-operations.md`

คลาส Matrix ที่สร้างที่นี่คือรากฐานของเฟรมเวิร์กโครงข่ายประสาทเทียมขนาดเล็กที่เราจะสร้างใน Phase 3 บทที่ 10

## แบบฝึกหัด

1. **ตรวจเมทริกซ์ผกผัน** คูณ `A @ A.inverse_2x2()` แล้วยืนยันว่าได้เมทริกซ์เอกลักษณ์ ลองกับเมทริกซ์ 2x2 สามตัว จะเกิดอะไรขึ้นเมื่อดีเทอร์มิแนนต์เป็นศูนย์

2. **เขียนเมทริกซ์ผกผัน 3x3** ขยายคลาส Matrix ให้หาเมทริกซ์ผกผันของเมทริกซ์ 3x3 ด้วยวิธี adjugate แล้วทดสอบเทียบกับ `np.linalg.inv` ของ NumPy

3. **สร้างโครงข่ายสองชั้น** ใช้แค่คลาส Matrix ของคุณ (ไม่ใช้ NumPy) สร้างโครงข่ายประสาทเทียมสองชั้น: ขาเข้า (3) -> ชั้นซ่อน (4) -> ขาออก (2) กำหนดน้ำหนักแบบสุ่ม รัน forward pass แล้วตรวจว่า shape ถูกทั้งหมด

### คำใบ้

**แบบฝึกหัดที่ 1** คูณ `A @ A.inverse_2x2()` กับเมทริกซ์สามตัว แล้วเทียบทุกช่องกับเมทริกซ์เอกลักษณ์ด้วยค่าคลาดเคลื่อน `1e-9` สำหรับเมทริกซ์ที่ดีเทอร์มิแนนต์เป็น 0 เช่น [[1, 2], [2, 4]] `inverse_2x2` จะเกิด `ValueError` ซึ่งเป็นผลที่ถูกต้อง

**แบบฝึกหัดที่ 2** คำนวณเมทริกซ์โคแฟกเตอร์ 3x3 แล้ว transpose เพื่อได้ adjugate จากนั้นหารทุกช่องด้วย `determinant()` ตรวจว่า `A @ A_inv` ได้เมทริกซ์เอกลักษณ์ และทุกช่องตรงกับ `np.linalg.inv(A)` ภายใน `1e-9`

**แบบฝึกหัดที่ 3** เขียน shape ของแต่ละเมทริกซ์ก่อนคูณ: `W1` เป็น 4x3 และ `W2` เป็น 2x4 แบบใน `demo_neural_network_layer` ข้อมูลขาเข้าขนาด 3x1 ต้องได้เวกเตอร์ชั้นซ่อนขนาด 4x1 และผลลัพธ์ขนาด 2x1

## คำศัพท์สำคัญ

| คำศัพท์ | ที่คนมักพูด | ความหมายจริง |
|------|----------------|----------------------|
| Vector (เวกเตอร์) | "ลูกศร" | รายการตัวเลขที่มีลำดับ ใน AI คือจุดในปริภูมิหลายมิติ |
| Matrix (เมทริกซ์) | "ตารางตัวเลข" | การแปลงเชิงเส้น จับคู่เวกเตอร์จากปริภูมิหนึ่งไปอีกปริภูมิหนึ่ง |
| Matrix multiply (การคูณเมทริกซ์) | "แค่คูณตัวเลข" | dot product ระหว่างทุกแถวของเมทริกซ์แรกกับทุกคอลัมน์ของเมทริกซ์ที่สอง ลำดับมีผล |
| Transpose | "พลิก" | สลับแถวกับคอลัมน์ เปลี่ยนเมทริกซ์ $m \times n$ เป็น $n \times m$ สำคัญมากใน backpropagation |
| Determinant (ดีเทอร์มิแนนต์) | "ตัวเลขอะไรสักอย่างจากเมทริกซ์" | วัดว่าเมทริกซ์ขยายพื้นที่ (2 มิติ) หรือปริมาตร (3 มิติ) แค่ไหน ศูนย์แปลว่าการแปลงบีบมิติหนึ่งหายไป |
| Inverse (เมทริกซ์ผกผัน) | "ย้อนเมทริกซ์" | เมทริกซ์ที่ย้อนการแปลง มีอยู่เฉพาะเมื่อดีเทอร์มิแนนต์ไม่เป็นศูนย์ |
| Identity matrix (เมทริกซ์เอกลักษณ์) | "เมทริกซ์น่าเบื่อ" | เมทริกซ์ที่เทียบได้กับการคูณด้วย 1 ใช้ใน residual connection (ResNet) |
| Broadcasting | "เวทมนตร์แก้ shape" | การยืด array ที่เล็กกว่าให้เท่า array ที่ใหญ่กว่า ด้วยการทำซ้ำไปตามมิติที่ขาด |
| Element-wise (ทีละสมาชิก) | "คูณธรรมดา" | คูณตำแหน่งที่ตรงกัน array ทั้งสองต้องมี shape เดียวกัน (หรือ broadcast ได้) |

## อ่านเพิ่มเติม

- [3Blue1Brown: Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra) - ภาพที่ช่วยให้เข้าใจทุกการดำเนินการในบทนี้
- [NumPy documentation on broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) - กฎที่ NumPy ใช้จริง
- [Stanford CS229 Linear Algebra Review](http://cs229.stanford.edu/section/cs229-linalg.pdf) - สรุปพีชคณิตเชิงเส้นสำหรับ ML แบบกระชับ
