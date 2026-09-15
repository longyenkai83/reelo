
> **V2 handoff:** Với Content Intelligence Packet, đọc
> `integrations/content_intelligence/V2-BOUNDARY.md`. Main dùng outbox
> `notion_handoff.py`: recheck current ledger → prepare/claim → tạo đúng một DRAFT
> tại đích owner cho phép → fetch xác minh status/Source ID/data source → acknowledge URL.
> Không gọi lại Workflow bằng topic/Markdown, không ghi _INDEX hoặc status đã duyệt/đã đăng
> chỉ vì Critic PASS. Không có packet V2: giữ quy trình legacy bên dưới.

# CHẾ ĐỘ BATCH — chạy hàng loạt từ bảng Notion (bán tự động)

> Tính năng phụ của skill `viet-script`. Chỉ dùng khi anh gõ **"chạy hết link trong inbox"** / **"chạy batch"**. Quy trình thường (1 link / 1 lần) KHÔNG cần file này.

Kích hoạt khi anh gõ: **"chạy hết link trong inbox"** / "chạy batch" / "viết N chủ đề".

---
## 🔴 LUẬT THÉP — BATCH CHẠY QUA WORKFLOW (chốt 2026-07-23 · kiến trúc Orchestrator-Workers)
> **CẤM Main Thread tự chạy vòng lặp duyệt/viết từng bài trong batch.** Làm vậy dồn toàn bộ nháp + biên bản Critic vào phiên chính → phồng context, dễ "Prompt too long".
> **Khi user ra lệnh chạy batch, Main BẮT BUỘC ủy thác toàn bộ danh sách cho Workflow `batch-content`** (`.claude/workflows/batch-content.js`):
> ```
> Workflow({ scriptPath: '.claude/workflows/batch-content.js', args: [ {chu_de, dinh_dang?, nguon?, ghi_chu?}, ... ] })
> ```
> 🔴 **DÙNG `scriptPath` (KHÔNG dùng `name`).** Nghiệm thu 2026-07-23: gọi bằng `name` bị **cache bản script cũ + args không bind → trả rỗng**; gọi bằng `scriptPath` đọc file tươi + nhận args đúng (chạy 3 bài OK). `args` truyền **mảng thật** (không phải chuỗi).
> Workflow chạy CÁCH LY: mỗi bài **phái thợ viết → phái `critic-ban-giam-khao` chấm độc lập (mọi bài PHẢI qua Critic) → lưu file `BATCH-NHÁP`**; chỉ trả về Main **ĐÚNG 1 BẢNG tổng kết** ( Tên · Định dạng · Trục · Trạng thái Critic · File ). **TUYỆT ĐỐI không in nháp / biên bản Critic ra chat chính.** Main **đứng chờ nhận bảng**, không tự viết.
> **Sau khi nhận bảng, Main làm nốt phần Workflow KHÔNG làm được** (Workflow agent không có Notion MCP): ghi `scripts-output/_INDEX.md` (tuần tự — tránh race) + đẩy Notion từng bài theo `_private/brand/<brand>/notion-config.md`.
> *(Vì sao Workflow chứ không phải agent .md nested: **subagent KHÔNG phái được subagent** trong harness → orchestrator .md không phái được Critic, hỏng cổng "batch không miễn Critic". Fable 5 verify 2026-07-23.)*

---
### Quy trình worker (tham chiếu — Workflow áp cho từng bài. Phần Notion inbox/đẩy bên dưới do MAIN xử lý)

**Nguồn link = Notion database "Inbox Link" của brand** (lõi chung KHÔNG ghi cứng ID).
- **ID database + data source: lấy ở LỚP RIÊNG** → `_private/brand/<brand>/notion-config.md` (mỗi brand/workspace một ID; đổi khách → thay file đó, không sửa skill).
- Cần connector **Notion** bật trong Claude Code của người chạy. Nếu không có Notion → fallback đọc file local `inbox-link.md`.

Cách chạy:
1. Query database, lấy các dòng **Trạng thái = "Chờ chạy"**.
2. Với TỪNG dòng (KHÔNG dừng chờ duyệt từng bài):
   - Đổi Trạng thái dòng đó → **"Đang chạy"**.
   - GATE: câu 1–2 rút từ video; câu 3 từ Brand Profile theo cột **Brand** (nếu `_private/brand/` chỉ có 1 brand thì lấy brand đó; nhiều brand thì HỎI).
   - Transcript → raw → wiki. Không transcript → set Trạng thái **"Lỗi"** + Ghi chú lý do, bỏ qua, chạy link sau.
   - 🔴 **SOI CHIẾN LƯỢC (BẮT BUỘC — chống bài lẻ):** **① nếu có file kế hoạch nhãn `🟢 ĐANG CHẠY` và hôm nay trong khoảng ngày → lấy đích/CTA/tầng phễu từ đó trước** *(nhãn `⚫ HẾT HẠN` thì bỏ qua)*; **②** rồi gán link vào **ô còn trống** trong `_private\brand\<brand>\ma-tran-30-ngay.md` khớp **Pillar + Giai đoạn phễu**; ghi **Pillar + Giai đoạn** vào dòng Notion (cột tương ứng). Link **lệch không khớp ô** → ghi "ngoài kế hoạch" + Ghi chú, vẫn chạy. Chưa có ma trận → bỏ qua bước này (nhắc 1 lần ở báo cáo cuối).
   - **Tự chọn 1 format hợp nhất** (ghi lý do). Nếu cột **Format muốn** có ghi thì theo đúng nó.
   - Viết **reel** bản nháp (định dạng mặc định), lưu `scripts-output\`, đầu bài ghi `TRẠNG THÁI: BATCH-NHÁP (chưa anh duyệt)`.
   - Cập nhật dòng Notion: Trạng thái **"Xong"** · **Format đã chọn** · **Ngày chạy** · Ghi chú (2–3 format khác hợp video).
   - **Đưa NỘI DUNG bài vào THÂN trang Notion** (insert_content): đặt **Tiêu đề trang** = tên bài tiếng Việt + " (nháp)"; đầu thân thêm 1 dòng trích dẫn "🟡 BẢN NHÁP — chưa duyệt · Format · Nguồn+link"; rồi toàn bộ lời thoại. Cột **Bài ra** chỉ ghi "📄 Nội dung trong trang" (KHÔNG ghi đường dẫn file local vì người dùng bấm không mở được).
3. Xong tất cả → báo **bảng tổng** trong chat: link → format → tên file; link nào Lỗi.
- **KHÔNG tự làm reel** trong batch (reel làm sau khi anh duyệt bản dài).
> Batch = ra NHÁP hàng loạt để anh review nhanh, KHÔNG phải bản chốt. Anh đọc, cái nào ưng → giữ / đổi format / cắt reel.
