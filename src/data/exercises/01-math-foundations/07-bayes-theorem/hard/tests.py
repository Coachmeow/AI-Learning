import math

DOCS = [
    "win free money now", "free lottery ticket winner", "claim your prize today free",
    "urgent offer free cash", "congratulations you won free",
    "meeting tomorrow at noon", "project update attached", "can we schedule a call",
    "quarterly report review", "lunch on thursday sounds good", "team standup notes attached",
    "please review the pull request",
]
LABELS = ["spam"] * 5 + ["ham"] * 7


def _model(sol, smoothing=1.0, docs=DOCS, labels=LABELS):
    NB = sol.get("NaiveBayes")
    if NB is None:
        raise Fail("ไม่พบคลาส NaiveBayes", "Class NaiveBayes was not found")
    m = NB(smoothing=smoothing)
    m.train(docs, labels)
    return m


def _ref_scores(doc, smoothing=1.0, docs=DOCS, labels=LABELS):
    vocab = {w for d in docs for w in d.lower().split()}
    words = [w for w in doc.lower().split() if w in vocab]
    out = {}
    for c in set(labels):
        cdocs = [d for d, l in zip(docs, labels) if l == c]
        cw = [w for d in cdocs for w in d.lower().split()]
        s = math.log(len(cdocs) / len(docs))
        for w in words:
            s += math.log((cw.count(w) + smoothing) / (len(cw) + smoothing * len(vocab)))
        out[c] = s
    return out


def _same(got, want, th, en, tol=1e-9):
    if not isinstance(got, dict) or set(got) != set(want) or not all(math.isclose(got[k], want[k], abs_tol=tol) for k in want):
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("scores", th="log_scores(\"free money now\") ตรงกับสูตร", en="log_scores(\"free money now\") matches the formula")
def _(sol):
    _same(_model(sol).log_scores("free money now"), _ref_scores("free money now"), "log_scores", "log_scores")


@check("unknown-words", th="คำที่ไม่อยู่ในคลังคำถูกข้าม", en="Words outside the vocabulary are skipped")
def _(sol):
    m = _model(sol)
    _same(m.log_scores("free blockchain zebra"), _ref_scores("free"), "\"free blockchain zebra\" ต้องได้คะแนนเท่ากับ \"free\"", "\"free blockchain zebra\" must score the same as \"free\"")


@check("proba", th="predict_proba รวมกันได้ 1 และตรงกับการทำให้เป็นมาตรฐาน", en="predict_proba adds up to 1 and matches normalisation")
def _(sol):
    ref = _ref_scores("please review the report")
    z = sum(math.exp(v) for v in ref.values())
    _same(_model(sol).predict_proba("please review the report"), {c: math.exp(v) / z for c, v in ref.items()}, "predict_proba", "predict_proba")


@check("long-message", th="ข้อความ 400 คำไม่ทำให้พัง", en="A 400-word message doesn't break it")
def _(sol):
    try:
        p = _model(sol).predict_proba("free " * 400)
    except ZeroDivisionError:
        raise Fail("ZeroDivisionError: exp ของคะแนน underflow เป็น 0 ทั้งหมด ต้องลบคะแนนสูงสุดออกก่อน", "ZeroDivisionError: exp of every score underflowed to 0; subtract the highest score first")
    if not isinstance(p, dict) or not math.isclose(p.get("spam", 0), 1.0, abs_tol=1e-9) or not math.isclose(sum(p.values()), 1.0, abs_tol=1e-9):
        raise Fail(f"ควรได้ spam ≈ 1.0 แต่ได้ {p!r}", f"Should give spam ≈ 1.0, got {p!r}")


@check("smoothing", th="ใช้ค่า smoothing ที่กำหนด (0.5)", en="Uses the given smoothing (0.5)", hidden=True)
def _(sol):
    _same(_model(sol, 0.5).log_scores("free meeting report"), _ref_scores("free meeting report", 0.5), "smoothing 0.5", "smoothing 0.5")


@check("three-classes", th="สามคลาสที่จำนวนข้อความไม่เท่ากัน", en="Three classes with different numbers of messages", hidden=True)
def _(sol):
    docs = ["goal match win", "match team score", "team goal", "vote election", "election poll vote today", "rain sun cloud"]
    labels = ["sport", "sport", "sport", "politics", "politics", "weather"]
    m = _model(sol, 1.0, docs, labels)
    _same(m.log_scores("team vote rain"), _ref_scores("team vote rain", 1.0, docs, labels), "สามคลาส", "Three classes")
