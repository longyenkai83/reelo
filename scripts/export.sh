#!/usr/bin/env bash
# export.sh — Đóng gói Reelo thành BẢN BÁN (sạch data riêng).
# Dùng: bash scripts/export.sh <thư-mục-đích>
# Copy toàn project sang đích, TỰ LOẠI BỎ mọi thứ riêng của chủ + rác vận hành.
# Bản xuất KHÔNG có _private/ → khi mở, engine tự chuyển chế độ intake (/bat-dau).

set -euo pipefail

DEST="${1:-}"
if [ -z "$DEST" ]; then
  echo "❌ Thiếu thư mục đích. Dùng: bash scripts/export.sh <thư-mục-đích>"
  exit 1
fi

SRC="$(cd "$(dirname "$0")/.." && pwd)"   # gốc project (cha của scripts/)

echo "📦 Xuất bản Reelo (bản BÁN) từ:"
echo "   $SRC"
echo "   → $DEST"

mkdir -p "$DEST"

# Danh sách LOẠI BỎ khỏi bản bán (data riêng + rác vận hành + lịch sử)
EXCLUDES=(
  "_private"              # DATA RIÊNG chị Hiền — tuyệt đối không bán
  "scripts-output"        # thành phẩm của chủ
  "carousel-output"       # thành phẩm của chủ
  "_backup"               # backup nội bộ
  "_archive"              # lưu trữ nội bộ
  ".obsidian"             # trạng thái Obsidian cá nhân
  ".git"                  # lịch sử git (nếu có)
  "NHAT-KY-PHIEN.md"      # nhật ký vận hành
  "NHAT-KY-PHIEN_archive.md"
  "SO-LOI-REELO.md"       # sổ lỗi nội bộ
  "openspec/changes"      # đề xuất đang mở (giữ specs/ baseline)
  "openspec/archive"
)

# Dùng rsync nếu có (sạch + nhanh); nếu không, fallback cp + xóa.
if command -v rsync >/dev/null 2>&1; then
  ARGS=()
  for e in "${EXCLUDES[@]}"; do ARGS+=(--exclude "$e"); done
  rsync -a "${ARGS[@]}" "$SRC/" "$DEST/"
else
  cp -a "$SRC/." "$DEST/"
  for e in "${EXCLUDES[@]}"; do rm -rf "${DEST:?}/$e"; done
fi

# Chốt an toàn 1: chắc chắn KHÔNG còn _private trong bản xuất
if [ -e "$DEST/_private" ]; then
  echo "🛑 LỖI AN TOÀN: _private/ vẫn còn trong bản xuất → DỪNG."
  exit 2
fi

# Chốt an toàn 2 (thêm 2026-08-06): quét NỘI DUNG file còn sót tên/dữ liệu riêng của chủ.
# Xoá thư mục _private/ là chưa đủ — tên brand, audience, định vị, số kênh có thể đã bị
# viết thẳng vào engine/ hoặc .claude/ từ trước. Bán kèm mấy dòng đó là bán kèm data của chủ.
echo "🔎 Quét rò rỉ dữ liệu riêng trong phần bán…"
LEAK_PAT='Nhi Hiền|chị Hiền|nhi-hien|lifestyleu40|4 lớp tự do|360\.888'
LEAKS="$(grep -rIn -E "$LEAK_PAT" "$DEST/engine" "$DEST/.claude" 2>/dev/null || true)"
if [ -n "$LEAKS" ]; then
  echo "🛑 LỖI AN TOÀN: bản bán còn dữ liệu riêng của chủ → DỪNG."
  echo "$LEAKS" | head -20
  echo "   → Sửa các dòng trên thành dạng trung tính (<brand>, 'chủ thể', 'brand'), rồi chạy lại."
  exit 3
fi
echo "   ✅ engine/ + .claude/ sạch."

echo "✅ Xong. Bản bán sạch tại: $DEST"
echo "   (KHÔNG có _private/ — khách mở sẽ chạy intake /bat-dau để khai brand mới.)"
