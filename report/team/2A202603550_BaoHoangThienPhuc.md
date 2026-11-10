# Báo cáo cá nhân — Bảo Hoàng Thiên Phúc

- MSSV: `2A202603550`
- Email: `peaceminusone214@gmail.com`
- Nhóm: `NhomCuaCat`

## Phần việc phụ trách

- Thiết kế system prompt và tool routing.
- Viết tool mới `dedupe_items` cùng `TOOL.md` và đăng ký tool.
- Viết eval group 10 case, unit test và UI Streamlit.

## Đóng góp cụ thể

- Thêm rule routing cho timeline, social search, web lookup, fetch, policy, papers và clarify.
- Thêm guardrail xác nhận trước khi gửi Telegram.
- Viết 3 unit test cho tool mới: happy path, input không hợp lệ và lỗi kiểu dữ liệu.
- Thêm 10 eval case gồm 5 single-turn và 5 multi-turn.

## Bằng chứng và tự kiểm tra

- `starter_v0/tools/dedupe_items/`
- `starter_v0/tests/test_tools_todo.py`
- `starter_v0/data/eval_group.json`
- `starter_v0/app.py`
- Pytest offline: `70 passed, 14 skipped`; các test skipped là challenge bonus của starter.

## Công cụ AI đã sử dụng

Sử dụng Codex để đọc README, triển khai code/test/UI và phân tích cấu trúc lab. Kết quả được tự kiểm tra bằng contract test, unit test, kiểm tra schema eval và compile Python.
