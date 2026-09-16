# Writing Knowledge C1 — cơ chế trước, mẫu tham khảo sau

E1: [Purified Plan](../../integrations/content_intelligence/PURIFIED-PLAN-E1.md)
đã cho phép psychology NONE trong plan mới. Các ghi chú compatibility C1/D1 bên
dưới mô tả route lịch sử; không được dùng để ép psychology lên route E1.

D1 runtime integration hiện được mô tả tại [Context Packs](../../integrations/content_intelligence/CONTEXT-PACKS-D1.md).
Các ghi chú “chưa nối runtime” bên dưới mô tả phạm vi C1 gốc; D1 đã project các
section được chọn vào từng stage, vẫn giữ psychology/title-eight compatibility.

Canonical knowledge authority cho RP3.C, dựa trên quyết định Owner trong prompt C1.
Đây là mô hình kiến thức, chưa phải migration runtime. Không tự cấp quyền viết.
Recipe data chuẩn ở [recipes.json](recipes.json); bản đồ tài sản và ngoại lệ chuyển tiếp
ở [ASSET-MAP.md](ASSET-MAP.md). Không sao chép thư viện lớn vào active context.

## Thứ tự và ranh giới

**CORE → CONTENT JOB → RECIPE → MECHANISMS → OPTIONAL REFERENCE**.
Creator Memory (voice, chuyện thật, POV, CTA, lịch sử đã viết) là nguồn riêng được
chọn rõ ràng, không phải luật chung. Platform/Workflow Infrastructure quản lý quyền,
nguồn, hash, currentness, approval, stage và publication; nằm ngoài mô hình này.
Customer truth vẫn từ intelligence/evidence; creator memory không được thay thế nó.

Trong mô hình C1, reference không có quyền bắt buộc dùng contrast, đặt tên psychology,
giả lập cảm xúc, áp sales framework hay đổi angle. Chỉ chọn kỹ thuật giúp công việc
của bài. Reference không phải bằng chứng cho một trải nghiệm/số liệu của creator.

## Sáu lăng kính ngữ nghĩa

| Lăng kính | Ý nghĩa |
|---|---|
| CLEAR | Hiểu ngay ý và quan hệ giữa các ý; không cần giải mã câu chữ. |
| RELEVANT | Hiểu vì sao liên quan đến mình, không bịa danh tính hoặc động cơ người đọc. |
| VALUABLE | Nhận một giá trị có ý nghĩa, không chỉ cảm giác bài đã đủ mục. |
| TRUE | Claim, Story, Knowledge đúng nguồn, phạm vi, mức chắc chắn và giới hạn. |
| FELT | Có chất người/chuyển động cảm xúc khi hữu ích; không ép kịch tính. |
| COMPLETE | Trả được lời hứa/payoff đã mở, kể cả một suy ngẫm yên tĩnh. |

Đây không phải sáu boolean, điểm số, regex hay ngưỡng nghiệm thu. Không thay thế
provenance/currentness/approval/truth guards hoặc independent Critic.

## Trước khi viết: một Creative Plan tích hợp

Plan giải quyết: **ONE IDEA** (ý chính), **READER VALUE** (người đọc nhận gì),
**CONTENT JOB** (mục đích), **RECIPE** (cách tổ chức), **PROOF** (cơ sở),
**EMOTIONAL MOVEMENT** (điểm đầu → câu hỏi/căng thẳng/thay đổi → điểm cuối),
**HOOK / OPENING** (chú ý mà không đổi nghĩa), **PAYOFF** (trả lời hứa).
Đó là câu hỏi thiết kế trong cùng một plan, không phải tám màn hình duyệt hay
các micro-gate psychology/recipe/Story/hook/title/outline/CTA.

Proof có thể là customer evidence, creator Story, creator Knowledge/POV, external
knowledge hoặc NONE cho suy ngẫm phi dữ kiện không cần proof. NONE không miễn
bằng chứng cho một claim thực tế. POV phải được trình bày là POV, không nâng thành
customer truth. Emotion có thể nhẹ; thiếu dữ kiện về cảm xúc thì không tự điền.

## Job và recipe

Chỉ chín job ban đầu: TEACH, DIAGNOSE, BELIEF_SHIFT, STORY, MISTAKE_LESSON,
CASE_STUDY, REFRAME, PERSUADE, REFLECT. Job là mục đích; không phải platform,
mode, psychology, creator pillar hoặc kiểu tiêu đề. Không ép một job cho mọi bài.

[recipes.json](recipes.json) là biểu diễn tối thiểu đọc được: mỗi recipe chỉ có
job, when_to_use, required_inputs, optional_inputs, core_sequence, reader_value,
truth_limits, completion_condition. Các ô là chỉ dẫn ngữ nghĩa, không prompt lớn.
Required input thiếu thì chọn cách khác hoặc báo thiếu; không sáng tác dữ kiện để
điền đủ sequence. Trình tự là cơ chế tổ chức, không quota đoạn hay climax bắt buộc.
TEACH không cần belief shift; REFLECT không cần checklist hoặc CTA hành động.
PAS/AIDA là lựa chọn của PERSUADE, không làm cả Reelo sales-first.

## Story: có công việc rõ ràng hoặc NONE

Story selection: DIRECT / ADJACENT / NONE. Nếu bỏ Story mà bài không yếu đi,
ưu tiên NONE. Không có Story thì không cần narrative structure. Khi chọn STORY
làm job chính nhưng không có chuyện phù hợp, đổi recipe qua plan review; không
giả vờ NONE vẫn đủ để kể một trải nghiệm có thật.

Khi hữu ích: SITUATION → DESIRE → TENSION / CONFLICT → TURN / CHANGE → MEANING
→ READER PAYOFF. Không tạo climax, realization, cảm xúc, kết quả hoặc lời nói
không có nguồn để làm trọn khung. ADJACENT chỉ minh họa một nét tương đồng,
không chứng minh cùng hoàn cảnh, nguyên nhân hay kết quả. Personal-story-first
được phép, kể “mình/tôi” khi có giá trị và làm rõ sớm sự liên quan với người đọc.

Capture giữ `/nap-chuyen` và Story Vault: WHAT HAPPENED? WHY DOES IT MATTER?
WHO MIGHT CARE? Lưu raw trước, cấu trúc sau. Hai câu sau có thể chưa rõ; không
bắt chủ thể viết một chuyện hoàn chỉnh khi nạp. Không đổi private schema, không
migrate kho, không biến diễn giải thành lời kể gốc. Backup/nguyên văn/provenance
và phân biệt chuyện thật với chuyên môn của capability hiện hữu được giữ.

## Hook

RAPID CONTEXT + RELEVANCE + CURIOSITY / TENSION + TRUTH + CLARITY.
Người đọc biết đang nói chuyện gì, vì sao đáng theo dõi, với lời hứa trung thực.
Contrast là một lựa chọn; “bạn” là kỹ thuật tạo liên quan, không lệnh cấm “mình”.
Không đánh đổi hiểu nghĩa lấy wordplay hoặc độ sốc. Story-first hợp lệ khi sự
liên quan hiện ra nhanh. Không ép số hook hay toàn bộ kho vào mô hình kiến thức.

REEL thêm SPOKEN + TEXT + VISUAL + optional AUDIO cùng một ý; tín hiệu không
được mâu thuẫn hoặc làm mất hiểu nghĩa. Đây là concept alignment, không bắt
sản xuất media trong C1. SHORT_ARTICLE và LONG_ARTICLE là văn viết; không bắt
Reel hook package. Reel không phải bài ngắn đọc lên. Mode vẫn theo A1.

## Title

WHAT IS THIS ABOUT? + WHY SHOULD I CARE? + optional TENSION.
Review ngữ nghĩa: CLEAR, RELEVANT, FAITHFUL TO ONE IDEA, USEFUL PROMISE,
NO DECODING REQUIRED. Không tạo 50 mẫu bắt buộc hoặc một bộ scoring mới.
Title đã được Owner duyệt vẫn khóa nguyên văn; mechanism không cho Writer
đổi title/hook/mode/angle. Các title frame lịch sử là reference.

## Psychology và Reference

Psychology là support reference tùy chọn trong C1; không cần đặt tên mechanism
cho mọi bài. Không được bịa customer motive, đổi angle, ép fear/loss/contrast,
đổi audience truth hay lấn Reader Value. Hook examples, title frames, Story
techniques, lexical craft, anti-AI patterns, platform tactics, CTA patterns có
thể phong phú trong reference. Chỉ tra khi hữu ích; không tự thành active authority.
Natural Vietnamese, nhịp câu và voice riêng vẫn quan trọng; đơn giản hóa không
đồng nghĩa viết giọng chung hoặc cắt chất người. Lịch sử chống lặp vẫn riêng.

## Tương thích có chủ đích — chưa migration runtime

C1 bỏ mandatory authority khỏi **mô hình kiến thức mới**, không gỡ gate đang
chạy. V2 hiện vẫn yêu cầu psychology trong PlanProposal và kiểm library; title
8-check A1 vẫn còn psychology/frame/trục và bảng candidate. Không gửi recipe C1
như PlanProposal hoặc dùng NONE để lách schema cũ. Optional psychology là năng
lực của knowledge model, chưa phải khả năng nhận null của runtime V2.

[A1](../../integrations/content_intelligence/SEMANTICS-A1.md) giữ quyền chuẩn cho
mode/title-8/Critic severity; [B1](../../integrations/content_intelligence/CREATOR-BOUNDARY-B1.md)
giữ creator isolation. Chín hard categories, exact approval locks, source hashes,
immutable Zone A/B, max-one-rewrite, UNKNOWN và human gate không đổi.
Không thay file legacy, candidate counts, private data, config read_files hoặc
approved manifests. Vì vậy runtime còn đọc luật lịch sử; C1 không tuyên bố đã
giảm token hay loại toàn bộ luật bắt buộc khỏi prompt hiện hành.

RP3.D cần dùng bản đồ này để chọn context theo job/mode và bảo vệ các phần guard
trong file hỗn hợp. Trước khi thực sự cho psychology null hoặc thay title checks,
cần explicit migration được review, không chỉ bỏ file khỏi manifest. Không tự
thực thi D, chạy C5 hay tái duyệt plan từ tài liệu C1. Tests cấu trúc không chứng
minh chất lượng văn hoặc semantic grounding của output mô hình.
