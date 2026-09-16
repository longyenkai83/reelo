# C1 — bản đồ trách nhiệm tài sản hiện hữu

Đọc [CORE.md](CORE.md) trước. Disposition dưới đây áp dụng cho mô hình C1;
file lịch sử chưa di chuyển/xóa và runtime chưa đổi retrieval. CORE/RECIPE/
REFERENCE/CREATOR_MEMORY là lớp kiến thức; LEGACY_COMPAT là phần tạm giữ để
tương thích. Guard thuộc infrastructure được chỉ rõ, không bỏ theo reference.
Mọi ví dụ lịch sử là minh họa, không phải source của customer/creator truth.

## Formats 01–17

Nguồn: `.claude/skills/viet-script/formats/` (các bản mirror nếu có cùng ranh giới).
Tên dưới đây nhận diện file cũ; không tạo thêm 17 recipe mới.

| File | Disposition / lớp / đích | Phần tách riêng |
|---|---|---|
| 01-how-to.md | MERGE INTO RECIPE / RECIPE / TEACH | Steps phục vụ học; ví dụ niche, độ dài kênh, CTA mặc định → REFERENCE; quota cũ → LEGACY_COMPAT. |
| 02-numbered-list.md | MOVE TO REFERENCE / REFERENCE / kỹ thuật trình bày TEACH hoặc DIAGNOSE | Danh sách không phải job; số điểm/CTA không universal; các chẩn đoán ví dụ không là truth. |
| 03-problem-solution.md | MERGE INTO RECIPE / RECIPE / DIAGNOSE hoặc TEACH theo mục đích | Có possible mechanism; agitate bắt buộc và “một nguyên nhân gốc” → LEGACY_COMPAT; ví dụ → REFERENCE. |
| 04-before-after-bridge.md | MERGE INTO RECIPE / RECIPE / CASE_STUDY hoặc PERSUADE | Before/after thật cần evidence; ngôi thứ nhất và cảm xúc tăng dần không bắt buộc; ví dụ → REFERENCE. |
| 05-contrarian.md | MERGE INTO RECIPE / RECIPE / BELIEF_SHIFT hoặc REFRAME | Tôn trọng frame cũ; belief phải có nguồn/HYPOTHESIS. Phủ nhận mạnh/mời tranh luận → REFERENCE, không gate. |
| 06-case-study.md | KEEP AS RECIPE / RECIPE / CASE_STUDY | Giữ process/result có nguồn; hook số, quota bài học, CTA → REFERENCE; không bịa số để đủ mẫu. |
| 07-breakdown.md | MERGE INTO RECIPE / RECIPE / TEACH hoặc DIAGNOSE | What/why/how là cấu trúc giải thích; claim algorithm và engagement ví dụ không tự là kiến thức verified. |
| 08-personal-story.md | KEEP AS RECIPE / RECIPE / STORY | Giữ chuyện thật, meaning, reader bridge; climax và mọi realization phải có nguồn; ví dụ → REFERENCE. |
| 09-transformation-story.md | MERGE INTO RECIPE / RECIPE / STORY hoặc CASE_STUDY | Không ép điểm A đủ tệ, khó khăn giữa đường, kết quả bất ngờ; không hứa người đọc đạt cùng kết quả. |
| 10-experiment.md | MERGE INTO RECIPE / RECIPE / CASE_STUDY; MISTAKE_LESSON nếu trọng tâm là sai lầm | Thiết kế/diễn biến/kết quả thật; số liệu và cảm xúc mẫu → REFERENCE, không evidence. |
| 11-pas.md | KEEP AS RECIPE / RECIPE / PERSUADE sub-recipe PAS | Chỉ khi job persuasive; pain/solution/claim phải grounded; không bắt mọi bài agitate. |
| 12-script-formula.md | LEGACY ONLY / LEGACY_COMPAT / khuôn video 5 phần | Topic/roadmap/momentum → REFERENCE; belief/contrast/credibility bắt buộc không là CORE. |
| 13-hook-frameworks.md | MOVE TO REFERENCE / REFERENCE / hook techniques | Lấy cơ chế có ích, không mandatory library, không mang trải nghiệm mẫu sang creator. |
| 14-story-levels.md | MOVE TO REFERENCE / REFERENCE / narrative craft | Độ sâu/cảnh/nhịp khi hữu ích; không ép mọi job lên cấp Story hoặc tự thêm drama. |
| 15-story-locks.md | MOVE TO REFERENCE / REFERENCE / attention craft | Naming/loop/transition tùy chọn; lệnh đổi nghi ngờ thành chắc chắn và đoán suy nghĩ → LEGACY_COMPAT, không chuyển sang C1. |
| 16-sales-page.md | MERGE INTO RECIPE / RECIPE / PERSUADE | PASTOR/proof-loop là reference sub-recipe; không bịa testimonial, identity, enemy, price anchor hoặc ép sales lên mọi job. |
| 17-story-loops.md | MOVE TO REFERENCE / REFERENCE / setup-payoff | Promise/payoff → CORE COMPLETE; quota 3–5 loops và phải bất ngờ → LEGACY_COMPAT, không luật mọi bài. |

## Các family hỗn hợp

Đường dẫn `engine/cong-thuc-viral/` trừ khi ghi khác.

| Family / vị trí | Phân tách C1 | Compatibility / lưu ý |
|---|---|---|
| story-structures.md A–C, D1–D2; khung-7-khuc-ke-chuyen.md | RECIPE: câu chuyện phục vụ ý/meaning/payoff; CORE: chuyện thật; REFERENCE: ẩn dụ, turning-message, giữ chân, proportions, ví dụ | Không mọi chuyện phải có câu “vỡ ra”; không đoán tâm lý người đọc. B1 đã tách ví dụ, giữ gate. |
| hook-system.md A/B3/F/H | CORE: rõ/đúng ý/liên quan/payoff; RECIPE mechanism: hook alignment REEL; REFERENCE: B/B2 công thức, C/D leverage/locks, E craft | G/I candidate-count/diversity và luật contrast bắt buộc → LEGACY_COMPAT; không bỏ current approved-plan checks. |
| checklist-hook.md §1–7 | CORE: chân thật, relevance, rõ, promise/payoff; REFERENCE: fatigue, lỗi craft, 5+5+5, timing | Cấm “Tôi”, quota từ, phải shock/contrast/CTA → LEGACY_COMPAT. Personal-story-first hợp lệ trong C1. |
| kho-hook.md | REFERENCE: khung/câu mẫu/nguồn minh họa | Không kho customer truth hoặc bắt copy lời. Anti-repeat vẫn đọc editorial history qua route cũ. |
| bo-tieu-de.md | CORE: hiểu nghĩa/đúng ý/đáng quan tâm; REFERENCE: title frames và ví dụ | Ba cột phân loại, candidate table/library check → LEGACY_COMPAT của title-8 A1, chưa gỡ. |
| nguyen-ly-tam-ly.md; psychology-gate.md | REFERENCE: cơ chế hỗ trợ; CORE: audience relevance/reader value; CREATOR_MEMORY: profile thực sự được cấu hình | “Nền móng bắt buộc mọi bài” không vào C1. Runtime PlanProposal/library validation còn nguyên; profile không là observed truth. |
| .claude/skills/viet-script/vietnamese-language-layer.md; references/ky-thuat-ke-chuyen.md; references/cum-tu-noi-thu-hut.md và mirrors | CORE: dễ hiểu, tự nhiên, không làm sai nghĩa; REFERENCE: từ nối/nhịp/cảnh/anti-AI/attention techniques | Voice/nhịp/ưu tiên của creator → CREATOR_MEMORY; quota và cấm từ máy móc → LEGACY_COMPAT, không chuẩn ngữ nghĩa. |
| viet-script/references/cong-thuc-pas-promise.md; formats/11-pas.md | RECIPE: PERSUADE/PAS; REFERENCE: ví dụ B1 ở reference-examples | Không biến PAS thành recipe mặc định của REFLECT/TEACH; không chế pain hay promise. |
| viet-script/references/format-bai-viet.md | CORE: văn viết khác văn nói; RECIPE: cấu trúc theo job; REFERENCE: nhịp/ảnh theo kênh | LONG không mặc định Story trong C1. Word ranges/image requirement/action CTA hiện hành → LEGACY_COMPAT, không tự gỡ publication requirements. |
| viet-script/references/luat-viet-cot-loi.md | CORE: thật, đủ giá trị, dễ hiểu; REFERENCE: trục/craft/funnel tips; CREATOR_MEMORY: lived proof/voice | Source/evidence/approval guards → infrastructure bảo vệ; quota EEAT/action/salesfit → LEGACY_COMPAT, không ép mọi job. |
| cong-kiem-chat-luong.md; Critic prompt/schema | CORE: chất lượng ngữ nghĩa; LEGACY_COMPAT: title-8, quota/format checks lịch sử | Independent Critic, 9 hard categories, currentness/truth veto → infrastructure giữ nguyên. Sáu lens không thay runtime output schema. |
| .claude/skills/nap-chuyen/SKILL.md; private Story Vault | CREATOR_MEMORY: raw chuyện/chuyên môn, attribution; CORE: không bịa | Capture raw trước, không migrate data/schema; backup/nguyên văn/provenance giữ nguyên. |
| private voice/writing-rules/CTA; scripts-output/_INDEX.md | CREATOR_MEMORY: sở thích, creator evidence, editorial history/chống lặp | B1 chọn workspace rõ ràng; không copy source riêng vào CORE. Không ghi ngược. |

## Chuyển tiếp và tiêu chí cho bước sau

Không có file legacy bị xóa hoặc rewrite trong C1. Quyền mandatory của reference
được loại trong **canonical knowledge model**; runtime cũ còn nguyên để giữ A1/B1.
Không dùng bảng này để bỏ cả file hỗn hợp khỏi read_files: có thể làm mất source,
guard hoặc voice. RP3.D phải chứng minh context selection giữ capability và có
review riêng cho mọi schema/gate migration; chưa được C1 cho phép triển khai.

Không sửa UNKNOWN/history, hash/approval, Zone A/B hoặc route legacy. Recipe
không có approval riêng; vẫn một human Creative Plan gate và final human approval.
No Writer / model generation / Notion / publish / merge / acceptance run trong C1.
