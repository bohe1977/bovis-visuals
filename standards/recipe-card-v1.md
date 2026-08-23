# Recipe Card v1 운영 표준

이 표준은 사용자가 요리 추천을 요청할 때 사용하는 BOVIS 카드의 단일 기준이다. 개별 HTML을 직접 수정하지 않는다.

## 생성 순서

1. 개인 요리 SQLite와 원문 Instagram 근거에서 추천 후보를 선별한다.
2. `data/recipe-guides/<guide>.json`에 **정확히 8개**를 작성한다.
3. 원문에서 재료·순서가 불완전하면 `status: "followup"` 및 `notice: "원문에서 추가 조리사항 확인 필요"`를 사용한다.
4. 원문에 별도 주의가 있으면 `status: "caution"`과 원문 근거의 안내 문구를 쓴다.
5. 아래 명령으로 검수와 렌더링을 실행한다.

```bash
python3 -m unittest tests/test_recipe_card_contract.py -v
python3 scripts/render_recipe_cards.py \
  --input data/recipe-guides/<guide>.json \
  --output <public-page>/index.html
```

## 고정 UI

- 중앙의 카드별 색 원형 순번
- 카드 상단 색 띠 없음, 레퍼런스 아래 내부 색 줄만 사용
- 검은 `레퍼런스` 버튼
- 준비물·조리 흐름·안내문은 동일 글꼴
- 조리 단계 숫자는 검은색
- 미확인/주의 사항은 조리 흐름 뒤 충분한 여백과 회색 `확인 사항` 박스

`standards/recipe-card-contract-v1.json`과 `templates/recipe-cards-v1.html`을 바꾸려면 `tests/test_recipe_card_contract.py`의 계약 테스트도 함께 갱신하고, 현재 8개 카드의 공개 화면을 재검증한다.
