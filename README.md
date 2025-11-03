# backend-api-automation-framework
API automation framework design and implementation with the example of leetcode api.
=======
# LeetCode API Automation (Backend Testing Framework)
A production-ready **PyTest** automation framework for a LeetCode-like backend.

## Highlights
- PyTest + Requests fixtures & markers
- OpenAPI contract tests with schemathesis
- JSON Schema validation
- Allure reporting
- Pre-commit hooks
- FastAPI mock server + docker-compose
- GitHub Actions CI

See the full README in the zip for setup & usage.

---

## ✅ Basic Sample Run & Results

Below is a **quick local run** against the included FastAPI mock server and the provided tests.

### 1) Start the mock API
```bash
uvicorn mock.server:app --reload --port 8000
# Server at http://127.0.0.1:8000
```

### 2) Run a focused test set (API + perf)
```bash
# In a new terminal (same project root)
export BASE_URL=http://127.0.0.1:8000
pytest -q tests/api tests/performance
```

### ▶️ Sample Output
```
9 passed in 0.65s
```

> This executes:
> - `tests/api/test_health_smoke.py::test_health_ok`
> - `tests/api/test_problems.py::{test_problems_list_schema,test_problems_constraints,test_problems_sorted_desc}`
> - `tests/api/test_users.py::{test_user_by_id_schema[param0],param1,param2],test_user_not_found}`
> - `tests/performance/test_response_time.py::test_problems_response_time`

### 3) (Optional) Run everything including contract tests
```bash
pytest -q
```
> Note: Contract tests use **Schemathesis** to validate the OpenAPI spec end-to-end.

---

## 🔍 Test Scenarios Covered

### Smoke / Health
1. **/health → 200 & body `{"status": "ok"}`** (readiness probe)

### Problems API (`GET /problems`)
2. **Schema compliance** against `tests/schemas/problems_list.schema.json`
3. **Business constraints**: `0 <= num_solved <= num_total`
4. **Items well-formed**: `title`, `difficulty∈{Easy,Medium,Hard}`, `timestamp` ISO-UTC
5. **Temporal sanity**: timestamps are **not in the future**
6. **Ordering**: `recently_solved` sorted **desc** by `timestamp`

### Users API (`GET /users/{id}`)
7. **User schema** (seeded users: IDs `1, 2, 3`) match `tests/schemas/user.schema.json`
8. **Negative**: unknown user → `404` with `{"error_code": "USER_NOT_FOUND", "message": "..."}`

### Performance Guardrail
9. **Latency & payload size**: `/problems` responds in **<1.5s** and **<500 KB**

---

## 📦 Example JSON Payloads

### `/problems` (seeded)
```json
{
  "user_name": "umang",
  "num_solved": 250,
  "num_total": 300,
  "recently_solved": [
    {"title": "LRU Cache", "difficulty": "Medium", "timestamp": "2025-10-30T14:51:12Z"},
    {"title": "Two Sum", "difficulty": "Easy", "timestamp": "2025-10-28T09:23:45Z"}
  ]
}
```

### `/users/1` (seeded)
```json
{
  "id": 1,
  "name": "Umang Patel",
  "email": "umang@example.com",
  "joined_at": "2023-01-01T00:00:00Z"
}
```

---

## 🧪 Tips
- Use `-m smoke` for a tiny check: `pytest -m smoke -q`
- See verbose list with timing: `pytest -v --durations=5`
- Generate Allure reports: `pytest --alluredir=reports/allure && allure serve reports/allure`
>>>>>>> adc772a (Leetcode API autoamtion framework)
