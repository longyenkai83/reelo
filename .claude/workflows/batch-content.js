export const meta = {
  name: 'batch-content',
  description: 'Chạy batch viết nhiều bài Reelo trong không gian cách ly (Orchestrator-Workers): mỗi bài phái thợ viết → phái Critic độc lập chấm → lưu file nháp BATCH-NHÁP. Chỉ trả về Main 1 BẢNG tổng kết (có cột TIÊU ĐỀ + KHUNG + cờ DUYỆT — Main trình bảng cho người duyệt chốt tiêu đề TRƯỚC khi ghi _INDEX/đẩy Notion; không in nháp/biên bản Critic) để chống phình context.',
  phases: [
    { title: 'Viết', detail: 'mỗi bài 1 thợ viết theo quy trình viet-script' },
    { title: 'Chấm', detail: 'phái critic-ban-giam-khao chấm độc lập' },
    { title: 'Sửa', detail: 'sửa 1 vòng nếu Critic CẦN SỬA rồi chấm lại' },
  ],
}

// args = danh sách bài cần chạy. Mỗi phần tử là string (chủ đề) HOẶC object:
//   { chu_de: '...', dinh_dang?: 'Reel|Bài ngắn|Bài dài|Carousel', nguon?: 'wiki ... / link', ghi_chu?: '...' }
// Nhận args BỀN: chấp cả khi runtime truyền args dạng chuỗi JSON, hoặc {items:[...]}.
let _raw = args
if (typeof _raw === 'string') {
  try { _raw = JSON.parse(_raw) } catch (e) { _raw = null }
}
const items = Array.isArray(_raw) ? _raw : (_raw && Array.isArray(_raw.items)) ? _raw.items : []
if (!items.length) {
  return [{ ten: '(rỗng)', dinh_dang: '—', truc: '—', critic: '—', file: 'args không phải mảng bài. typeof args=' + (typeof args) }]
}

const norm = (it) => (typeof it === 'string' ? { chu_de: it } : (it || {}))

// Pool trục — Orchestrator GÁN round-robin để các bài CÙNG batch không trùng trục.
// (Writer chạy song song không thấy nhau qua _INDEX; nên phải phân bổ trục TRƯỚC khi viết.
//  Ưu tiên các trục đang thiếu trong kho: nghịch lý / hình ảnh cụ thể / ẩn dụ / câu hỏi.)
const TRUC_POOL = ['nghịch lý', 'hình ảnh cụ thể', 'ẩn dụ', 'câu hỏi', 'tuyên ngôn', 'contrast']

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    verdict: { type: 'string', enum: ['ĐẠT', 'CẦN SỬA'] },
    so_chu: { type: 'number' },
    do_tuoi: { type: 'string' },
    loi: { type: 'array', items: { type: 'string' } },
  },
  required: ['verdict'],
}

const WRITER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    ten: { type: 'string' },
    tieu_de: { type: 'string' },
    khung_tieu_de: { type: 'string' },
    dinh_dang: { type: 'string' },
    truc: { type: 'string' },
    file: { type: 'string' },
    ok: { type: 'boolean' },
    ghi_chu: { type: 'string' },
  },
  required: ['ten', 'file', 'ok'],
}

const WRITER_PROMPT = (it, trucGoiY) => `Bạn là thợ viết content Reelo, viết ĐÚNG 1 bài rồi LƯU FILE. Làm việc trong không gian cách ly — KHÔNG in nháp ra ngoài, chỉ trả metadata.

🎯 TRỤC GỢI Ý cho bài này (Orchestrator đã phân bổ để KHÔNG trùng trục với các bài khác trong CÙNG batch): **${trucGoiY}**. Ưu tiên viết theo trục này; chỉ đổi sang trục khác nếu nội dung thật sự không hợp + ghi lý do vào ghi_chu. (Vẫn soi _INDEX ở bước 3 để không trùng bài ĐÃ có trong sổ.)

Bài cần viết:
- Chủ đề: ${it.chu_de || '[tự rút từ nguồn]'}
- Định dạng: ${it.dinh_dang || '[TỰ CHỌN 1 định dạng hợp nhất, ghi lý do]'}
- Nguồn: ${it.nguon || '[tự tìm trong _private/kho-kien-thuc/wiki/]'}
- Ghi chú: ${it.ghi_chu || '(không)'}

QUY TRÌNH BẮT BUỘC (đọc file thật, KHÔNG làm tắt):
1. Read \`.claude/skills/viet-script/SKILL.md\` + reference định dạng tương ứng trong \`.claude/skills/viet-script/references/\` hoặc \`engine/cong-thuc-viral/dinh-dang-dau-ra.md\`. Read \`engine/cong-thuc-viral/cong-kiem-chat-luong.md\` để tự rà trước.
2. Read nguồn thật trong \`_private/kho-kien-thuc/wiki/\` — mở \`wiki/_INDEX.md\` tìm wiki hợp chủ đề, đừng đoán tên file. CHỐNG BỊA: mọi số/quote/case phải truy được về wiki/raw/kho-cau-chuyen; thiếu → [chưa có]. Kiến thức vay mượn của người khác dẫn dạng "mình nghe/học được", KHÔNG gán thành chuyện của chủ thể.
3. Soi \`scripts-output/_INDEX.md\` chống lặp: trích nguyên văn TRỤC của 2 bài gần nhất, CHỌN TRỤC KHÁC (đừng lặp; ưu tiên trục đang thiếu: nghịch lý/hình ảnh cụ thể/ẩn dụ). Né các góc đã viết.
4. Voice Hiền (reel/bài viết bắt buộc): xưng "mình" gọi "bạn", điềm tĩnh, THẤU không phán, kết bằng câu hỏi tự soi. Carousel KHÔNG bắt voice Hiền nhưng phải tiếng Việt tự nhiên + how-to áp dụng được.
5. Đủ số chữ theo định dạng (Reel 170–220 · Bài ngắn 200–400 · Bài dài 400–800 · Carousel 5–8 slide). ĐẾM CHỮ THẬT, đừng ước.
6. Header file phải có 3 dòng bằng chứng cho Critic: Reference đã mở · GATE 5 câu · số chữ đếm thật; + bảng ≥8 hook (trừ Carousel) + trích nguyên văn _INDEX 2 bài.
6B. 🔴 BẢNG TIÊU ĐỀ — BẮT BUỘC, KHÔNG ĐƯỢC BỎ. Batch không có người duyệt đứng cạnh, nên đây là cổng DUY NHẤT gác tiêu đề.
   - Read "engine/cong-thuc-viral/bo-tieu-de.md" (kho khung, đánh SỐ) + "engine/cong-thuc-viral/nguyen-ly-tam-ly.md" (7 nguyên lý). CẤM nhớ suông.
   - Dựng bảng 3-5 phương án tiêu đề. Mỗi dòng khai ĐỦ BA CỘT RIÊNG:
       (1) NGUYÊN LÝ TÂM LÝ — tên có thật trong nguyen-ly-tam-ly.md
       (2) KHUNG TIÊU ĐỀ — SỐ có thật trong bo-tieu-de.md, HOẶC ghi thẳng chữ TỰ CHẾ (tự chế được phép, nhưng phải khai + vẫn neo được 1 nguyên lý ở cột 1)
       (3) TRỤC BÀI — 1 trong 6 trục
     🔴 BA BẢNG NÀY KHÁC NHAU. Điền tên bảng này sang cột bảng kia = SAI. Hay nhầm nhất: "Khung số đóng" là NGUYÊN LÝ (cột 1); "Nghịch lý" / "Hình ảnh cụ thể" là TRỤC (cột 3) — cả hai đều KHÔNG phải khung tiêu đề.
   - Tiêu đề CHỐT phải qua 3 cửa:
       (a) NHẮM MỘT NGƯỜI — đọc lên phải chỉ ra được MỘT người cụ thể trong ho-so-khach-hang.md của brand. Ai đọc cũng thấy hợp = chưa nhắm ai = làm lại.
       (b) ĐỌC RỜI CÓ HIỂU — che cả bài, chỉ đưa tiêu đề, người lạ vẫn biết bài nói gì.
       (c) KHÔNG TỪ NỘI BỘ — cấm nhãn quy trình lọt ra tiêu đề công khai ("Cho đủ:", "Mở (CT1):", "Thân:", tên pillar, mã trụ, mã ngày, tên khung/công thức).
   - Đặt tiêu đề chốt CẠNH câu mở chốt, đọc liền hai dòng: cấm đá nhau cả hai chiều (giấu đáp án ở câu mở rồi in nguyên đáp án lên tiêu đề, hoặc ngược lại). Với REEL: mặc định tiêu đề = câu mở; tách nhau thì phải khai lý do.
   - ⚠️ Luật "giữ đáp án cho thân bài" là luật của CÂU MỞ, KHÔNG áp cho tiêu đề. Việc của tiêu đề là làm người ta BẤM VÀO.
7. LƯU file vào \`scripts-output/\` (hoặc \`carousel-output/\` nếu Carousel), tên kebab không dấu + hậu tố định dạng. 🔴 Dòng ĐẦU file: \`TRẠNG THÁI: BATCH-NHÁP (chưa duyệt)\`. KHÔNG tự ghi _INDEX, KHÔNG đẩy Notion (Main làm sau).

Trả metadata: { ten (tiêu đề tiếng Việt), tieu_de (ĐÚNG tiêu đề đã chốt ở bước 6B), khung_tieu_de (SỐ khung có thật, hoặc chữ TỰ CHẾ), dinh_dang, truc, file (đường dẫn đã lưu), ok:true, ghi_chu }. Nếu không viết được (thiếu nguồn…) → ok:false + ghi_chu lý do.`

const CRITIC_PROMPT = (file, dinh_dang) => `Chấm bản nháp tại: \`${file}\` (định dạng: ${dinh_dang}).
Đọc rubric DUY NHẤT \`engine/cong-thuc-viral/cong-kiem-chat-luong.md\` (Read lại) + reference định dạng. Tự mở wiki nguồn verify CHỐNG BỊA (Lớp 1 VETO). Tự mở \`scripts-output/_INDEX.md\` kiểm chống lặp trục. Đếm chữ thật trong trần. Chấm Lớp 1 (chống bịa) · Lớp 2 (giọng AI, contrast ≤3) · Lớp 3 (HOOK **VÀ TIÊU ĐỀ** — chấm cả hai, đừng bỏ tiêu đề) · lớp ngôn ngữ · Lớp 6 (độ tươi).
🔴 LỚP 3 PHẦN TIÊU ĐỀ — bắt buộc tự đối chiếu, CẤM tin bảng nhãn trong bài: tự Read "engine/cong-thuc-viral/bo-tieu-de.md" (lắp thử tiêu đề vào madlib xem có vừa khung bài khai không) + tự Read "engine/cong-thuc-viral/nguyen-ly-tam-ly.md" (dò tên nguyên lý có thật). Bài tự tick "đã có khung" KHÔNG tính là bằng chứng.
Chấm đủ 7 ô: (1) khai đủ ba cột riêng, mỗi cột chỉ nhận giá trị từ đúng bảng của nó — khung phải là SỐ có thật hoặc chữ TỰ CHẾ (2) NHẮM MỘT NGƯỜI cụ thể trong ho-so-khach-hang.md, ai đọc cũng hợp = trượt (3) đọc rời có hiểu (4) không từ nội bộ ("Cho đủ:", "Mở (CT1):", mã trụ/ngày…) (5) không đá nhau với câu mở (6) đúng vai — tiêu đề để BẤM VÀO, luật giữ-đáp-án là của câu mở (7) reel thì tiêu đề khớp câu mở, tách phải khai lý do.
Ô (1)(2)(3) trượt = Lớp 3 CHƯA ĐẠT. Bác tiêu đề thì phải kèm 2-3 tiêu đề thay, mỗi cái ghi SỐ khung có thật + tên nguyên lý — cấm chê suông.
🔴 TRẢ CỰC GỌN qua schema: verdict (ĐẠT/CẦN SỬA) · so_chu · do_tuoi · loi (mảng lỗi ngắn). KHÔNG in phân tích dài.`

const FIX_PROMPT = (file, loi) => `Sửa bản nháp tại \`${file}\` theo các lỗi Critic nêu (giữ nguyên ý + nguồn, chỉ sửa lỗi): ${JSON.stringify(loi || [])}. Sửa xong lưu lại file. KHÔNG in nội dung ra ngoài, chỉ báo "đã sửa".`

async function writeOne(rawItem, idx) {
  const it = norm(rawItem)
  const trucGoiY = it.truc || TRUC_POOL[idx % TRUC_POOL.length]
  const draft = await agent(WRITER_PROMPT(it, trucGoiY), { label: `viết:${it.chu_de || 'bài'}`, phase: 'Viết', schema: WRITER_SCHEMA })
  if (!draft || !draft.ok || !draft.file) {
    return { ten: it.chu_de || '(?)', dinh_dang: it.dinh_dang || '—', truc: '—', critic: '❌ không viết được', file: (draft && draft.ghi_chu) || '—' }
  }
  let verdict = await agent(CRITIC_PROMPT(draft.file, draft.dinh_dang), { agentType: 'critic-ban-giam-khao', label: `chấm:${draft.ten}`, phase: 'Chấm', schema: VERDICT_SCHEMA })
  if (verdict && verdict.verdict === 'CẦN SỬA') {
    await agent(FIX_PROMPT(draft.file, verdict.loi), { label: `sửa:${draft.ten}`, phase: 'Sửa' })
    verdict = await agent(CRITIC_PROMPT(draft.file, draft.dinh_dang), { agentType: 'critic-ban-giam-khao', label: `chấm2:${draft.ten}`, phase: 'Chấm', schema: VERDICT_SCHEMA })
  }
  const status = verdict ? (verdict.verdict === 'ĐẠT' ? `✅ ĐẠT${verdict.do_tuoi ? ' ' + verdict.do_tuoi : ''}` : '❌ CẦN SỬA (còn lỗi sau 1 vòng)') : '⚠️ Critic lỗi'
  // Batch mất khâu "trình người duyệt chốt tiêu đề" của SKILL.md → thay bằng cờ để Main biết đường trình trước khi ghi _INDEX/đẩy Notion.
  const khung = draft.khung_tieu_de || '(không khai)'
  const canhBao = /tự chế|tu che|TỰ CHẾ/i.test(khung)
    ? '🟠 TỰ CHẾ — trình người duyệt chốt'
    : /^\s*(khung\s*)?\d{1,2}\s*$/i.test(String(khung).trim())
      ? '✅ khung có số'
      : '🔴 KHÔNG TRUY ĐƯỢC — trình người duyệt'
  return {
    ten: draft.ten,
    tieu_de: draft.tieu_de || draft.ten,
    khung_tieu_de: khung,
    duyet_tieu_de: canhBao,
    dinh_dang: draft.dinh_dang,
    truc: draft.truc,
    critic: status,
    file: draft.file,
  }
}

log(`Batch bắt đầu: ${items.length} bài (chạy cách ly, chỉ trả bảng tổng).`)
const rows = await parallel(items.map((it, i) => () => writeOne(it, i)))
return rows.filter(Boolean)
