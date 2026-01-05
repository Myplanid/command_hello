#!/bin/bash
# Dooray 웹훅 테스트 스크립트

# 웹훅 URL 설정 (여기에 실제 URL을 넣거나 환경변수로 설정)
WEBHOOK_URL="${DOORAY_WEBHOOK_URL:-YOUR_WEBHOOK_URL_HERE}"

# 메시지 설정
MESSAGE="${1:-🎉 Dooray 웹훅 1차 테스트입니다!}"
BOT_NAME="${2:-Cursor Agent}"

if [[ "$WEBHOOK_URL" == "YOUR_WEBHOOK_URL_HERE" ]]; then
    echo "⚠️  웹훅 URL을 설정해주세요!"
    echo "사용법:"
    echo "  export DOORAY_WEBHOOK_URL='https://hook.dooray.com/services/...'"
    echo "  ./dooray_webhook.sh '메시지'"
    exit 1
fi

echo "📤 Dooray 웹훅으로 메시지 전송 중..."
echo "   URL: ${WEBHOOK_URL:0:50}..."
echo "   메시지: $MESSAGE"

# 웹훅 전송
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d "{\"botName\": \"$BOT_NAME\", \"text\": \"$MESSAGE\"}" \
    "$WEBHOOK_URL")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" == "200" ]]; then
    echo "✅ 성공! (HTTP $HTTP_CODE)"
    echo "   응답: $BODY"
else
    echo "❌ 실패! (HTTP $HTTP_CODE)"
    echo "   응답: $BODY"
fi
