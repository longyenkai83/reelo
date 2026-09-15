# Cổng V2 — Content Intelligence → Reelo

Chỉ áp dụng cho luồng `v2.content-intelligence-packet.1` đã qua adapter. Luồng cũ giữ nguyên.

- Zone A là customer truth duy nhất; Zone B là ý định sáng tạo đã chọn, luôn PROPOSED.
  Zone C cho phép sáng tạo cách diễn đạt. Writer/Critic/Rewrite không được sửa A/B.
- GATE tâm lý câu 1–2 đọc audience/context/situation và Jobs/Pains/Gains trong A.
  Không tự suy tuổi, nghề, người mua, động cơ ẩn hay nỗi đau từ hồ sơ brand hoặc kho bài.
  Thiếu thì ghi chưa biết. V2 là B2C-first; không tạo buying committee.
- GATE câu 3 nối giá trị riêng của B với brand/business facts được cung cấp. Brand mismatch
  phải báo; không sửa hồ sơ khách hoặc thay góc để khớp brand.
- Story, RAW, WIKI, voice và editorial memory là tài nguyên chỉ đọc: dùng cho cách kể,
  giọng và kiến thức có nguồn. Creator Story phải giữ chủ thể; ví dụ tưởng tượng phải ghi
  rõ là minh họa. Chúng không tự trở thành customer truth hoặc bằng chứng nhu cầu.
- Giữ nguyên kỹ thuật hook, tiêu đề, tâm lý, storytelling, ngôn ngữ, giọng và định dạng.
  Trong rubric, chấm đủ **8 ô tiêu đề**, gồm ô ⑧. Ô nhắm người dùng bằng ngữ cảnh/câu nói
  có nguồn trong A, không lấy persona từ `ho-so-khach-hang.md`. Không buộc bịa tên/nghề.
- Ngoại lệ legacy cho `% thị trường` tu từ **không áp dụng V2**. Mọi số, quote, case và
  demographic phải có căn cứ. Không nâng customer speech thành hành vi mua/market validation.
- External assertion thiếu evidence: bỏ/giảm mức khẳng định nếu vẫn giữ ý định B; nếu không
  làm được thì `BLOCKED_PENDING_RESEARCH`. Không tạo research agent.
- Writer → Critic độc lập → tối đa một lần sửa → Critic lại. Mỗi bản lưu riêng, có parent.
  Không xóa slot thất bại. Critic PASS không phải human approval hay permission to publish.
- Notion chỉ nhận bản nháp tới đích được owner chỉ định. Không tự đăng mạng xã hội,
  đánh dấu đã duyệt, cập nhật profile, portfolio hoặc toàn bộ kho lịch sử.

Adapter Python chạy **trước native host**, kiểm contract độc lập, lưu packet bất biến và
reservation SQLite. Insight nạp lại hai ledger hiện tại trước gửi. Model không có quyền
khai `current=true` thay cho kiểm tra này. SQLite đặt trong LOCALAPPDATA trên một máy;
không dùng Google Drive/OneDrive làm cơ sở dữ liệu đồng thời giữa các máy.

Host cấu hình rõ executable 2.1.270, workspace và danh sách file được đọc. Hooks/plugins/MCP
bị tắt trong lần viết; chỉ Workflow/Read. Draft được trả có cấu trúc, code lưu ngoài repo.
Không dùng PATH fallback. Chỉ terminal task có tương quan với đúng Workflow mới là kết quả;
ACK, exit 0 và lời mô hình không chứng minh hoàn tất. Mất kết quả: UNKNOWN, không tự chạy lại.

Nguồn kiến trúc: Phase 9 blueprint; shared map r6, D13–D17; Insight docs/v2/00–15.
Unified Web Business OS là đích về sau; Phase 9 chỉ thêm application service, CLI/UI adapters.

C5.2 clarification: external knowledge is not creator experience. First-person learning,
meetings, actions or history need creator-specific evidence; customer speech/illustrations
cannot supply it. Unknown rental/shared context remains unknown. Critic must independently
verify relevant voice/story/knowledge sources. Any unresolved truth, intent, scope or source
verification defect belongs in blocking_issues, not notes. Code projects PASS only with zero
blockers; otherwise REVISE, with the raw review retained. No change to legacy or packet schema.

C5.4 owner-authorized decision: deterministic local Phase 9 code now calls one native Workflow
per stage (Writer, Critic1, optional Rewrite, Critic2), preserving this creative boundary.
The model cannot decide stage transitions or final execution status. Persist/validate each
terminal stage before continuing; stop UNKNOWN on malformed/stopped/mismatched output, retaining
all verified predecessors. No retry/resume framework. C5.3 permission rules remain unchanged.

C5.5: Critic emits typed findings. The nine hard truth/scope categories always block in
Python regardless of model severity or verdict; notes cannot be used to downgrade a detected
hard-boundary defect. Raw versus normalized findings retain the audit trail. Anonymous comment
counts are not verified people; separate sources do not explain each other's experiences.
One Critic only, existing maximum one rewrite, no extra semantic checker or legacy changes.
