# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: NhomCuaCat
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md) — nhóm có 1 thành viên
- Repo: https://github.com/peaceminusone214/K5-L3A-DAY03-NhomCuaCat-ResearchAgentToolEval (`main`)
- Provider/model dùng cho v0–v3: OpenAI `gpt-4o-mini`; preflight và eval provider thật đã pass

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Research agent hỗ trợ tìm tin web, tìm bài đăng theo tài khoản/chủ đề, đọc URL, tìm policy nội bộ và tìm paper arXiv. Agent hỏi lại khi thiếu thông tin, yêu cầu xác nhận trước khi gửi Telegram, và định dạng kết quả thành digest.

**Cách chạy UI:**

> Lệnh chạy UI: `cd starter_v0 && streamlit run app.py`; dependency `streamlit` đã thêm vào `requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: Chưa deploy; chạy local bằng lệnh trên.

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy bài đăng gần đây của một tài khoản | không |
| social_search | tìm bài đăng theo chủ đề, Latest/Top | không |
| lookup | tìm web general/news theo timeframe | không |
| fetch | đọc một URL cụ thể | không |
| format | định dạng items thành digest | không |
| send | gửi Telegram sau xác nhận | không |
| policy | tìm policy nội bộ | không |
| papers | tìm paper arXiv | không |
| paper_text | trích text PDF arXiv | không |
| dedupe_items | loại item trùng theo URL/title | có |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1. `Tin tức AI hôm nay có gì nổi bật?`
2. `Tweet mới nhất của Sam Altman là gì?`
3. `Tóm tắt bài này: https://openai.com/blog/gpt-5`
4. `Đăng bản digest này lên Telegram giúp mình` (agent phải hỏi xác nhận)
5. `Tìm 3 paper arXiv về retrieval augmented generation`

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- Prompt đã chuyển từ đoán bừa sang hỏi lại khi thiếu handle/URL, thêm routing rõ cho từng tool và boundary xác nhận trước `send`.
- `tools.yaml` mô tả khi nào dùng/không dùng tool và convention của handle, topic, timeframe, search type, confirmed.
- Tool mới `dedupe_items` là phép biến đổi local, loại trùng theo URL/title và giữ thứ tự xuất hiện đầu tiên.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Mốc setup OpenAI | NA | 0.85 | `starter_v0/runs/v0_B_base_openai_20261110T203907945983.json` |
| v1 | system prompt | Boundary `clarify`/`send` rõ hơn | 0.85 | 0.90 | `starter_v0/runs/v1_B_base_openai_20261110T204004299242.json` |
| v2 | system prompt | Ưu tiên instruction mới nhất ở multi-turn | 0.90 | 0.95 | `starter_v0/runs/v2_B_base_openai_20261110T204046331049.json` |
| v3 | system prompt | Bắt buộc `response_type=text` cho clarify thường | 0.95 | 1.00 | `starter_v0/runs/v3_B_base_openai_20261110T204135078595.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R11_missing_url | missing_info | clarify thiếu `response_type=text` ở v0 | Sai argument clarify | Prompt v3 bắt buộc response_type |
| R12_confirm_before_send | wrong_boundary | Có xu hướng gửi trước xác nhận ở v0 | Vi phạm boundary side effect | Thêm rule clarify yes_no trước send |
| M06_switch_tool | wrong_tool | Chọn social_search thay lookup ở v0 | Không ưu tiên instruction mới nhất | Thêm rule multi-turn latest instruction |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01 | policy nội bộ | policy/data_privacy | PASS |
| G02 | paper arXiv | papers | PASS |
| G03 | dedupe URL | dedupe_items | PASS |
| G04 | xác nhận Telegram | clarify yes_no | PASS |
| G05 | thiếu tài khoản | clarify text | PASS |
| G06 | policy multi-turn | policy/source_citation | PASS |
| G07 | đổi Latest → Top | social_search Top | PASS |
| G08 | arXiv text multi-turn | paper_text | PASS |
| G09 | dedupe multi-turn | dedupe_items/title | PASS |
| G10 | carry news timeframe | lookup/news/day | PASS |
| **Tổng** | 5 single + 5 multi-turn | — | **10/10**; `runs/v3-group-final_B_group_openai_20261110T204725600914.json` |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay | lookup | v3 | Trả về 5 kết quả tin tức |
| 2 | Tóm tắt bài không có URL | clarify | v3 | Hỏi URL |
| 3 | Bổ sung URL | fetch | v3 | Đọc và tóm tắt URL thành công |
| 4 | Đăng digest Telegram | clarify yes_no | v3 | Không gửi trước xác nhận |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/dedupe_items/` | Loại trùng local, giữ thứ tự | Không gọi mạng |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | 3 test: happy path, key sai, input sai kiểu | Trả error dict |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py` | Streamlit chat UI | Cần provider key |

Tool unit tests: 3 test cho `dedupe_items`; kiểm tra duplicate URL, key không hợp lệ và input không phải list — các lỗi code eval routing không phát hiện được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- Chạy offline: `.venv/bin/python -m pytest -q` → 70 passed, 14 skipped. Các skip là challenge bonus của tool có sẵn. Live transcript thành công: `starter_v0/transcripts/v3_openai_20261110T210013336905.transcript.json`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
