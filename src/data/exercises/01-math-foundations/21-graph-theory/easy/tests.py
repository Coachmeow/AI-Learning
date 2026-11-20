def _run(sol, adj, start, want, th, en):
    fn = sol.get("bfs_distances")
    if fn is None:
        raise Fail("ไม่พบฟังก์ชัน bfs_distances", "Function bfs_distances was not found")
    got = fn(adj, start)
    if not isinstance(got, dict) or got != want:
        raise Fail(f"{th}: ควรได้ {want} แต่ได้ {got!r}", f"{en}: should be {want}, got {got!r}")


@check("path", th="เส้นทาง 0 – 1 – 2 – 3 จาก 0 ได้ระยะ 0, 1, 2, 3", en="The path 0 – 1 – 2 – 3 from 0 gives distances 0, 1, 2, 3")
def _(sol):
    adj = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
    _run(sol, adj, 0, {0: 0, 1: 1, 2: 2, 3: 3}, "เส้นทาง", "Path")


@check("lesson", th="กราฟในบทเรียน (0-1, 0-2, 1-3) จาก 0", en="The lesson's graph (0-1, 0-2, 1-3) from 0")
def _(sol):
    adj = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    _run(sol, adj, 0, {0: 0, 1: 1, 2: 1, 3: 2}, "กราฟในบทเรียน", "The lesson's graph")


@check("shortcut", th="วงรอบ 6 โหนดจาก 0: โหนด 3 อยู่ห่าง 3 ขั้น ทางไหนก็ได้", en="A 6-node cycle from 0: node 3 is 3 hops away either way")
def _(sol):
    adj = {i: [(i - 1) % 6, (i + 1) % 6] for i in range(6)}
    _run(sol, adj, 0, {0: 0, 1: 1, 5: 1, 2: 2, 4: 2, 3: 3}, "วงรอบ 6 โหนด", "6-node cycle")


@check("unreachable", th="โหนดที่ไปไม่ถึงไม่อยู่ในผลลัพธ์", en="Unreachable nodes are not in the result")
def _(sol):
    adj = {0: [1], 1: [0], 2: [3], 3: [2]}
    _run(sol, adj, 2, {2: 0, 3: 1}, "สองส่วนที่แยกกัน", "Two separate pieces")
