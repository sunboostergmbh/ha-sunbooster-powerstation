#!/usr/bin/env bash
# Sunbooster Customer-Key generieren
# Verwendung: ./generate_key.sh <DEVICE_ID> [CUSTOMER_NAME]
# Voraussetzung: ADMIN_TOKEN in /etc/sunbooster/.admin_token

set -euo pipefail

DEVICE_ID="${1:-}"
CUSTOMER="${2:-beta}"
ADMIN_TOKEN_FILE="/etc/sunbooster/.admin_token"
PROXY_URL="https://api.sunbooster.com"

if [ -z "$DEVICE_ID" ]; then
  echo "Usage: $0 <DEVICE_ID> [CUSTOMER_NAME]"
  echo "Example: $0 502065bd3c63 'Max Mustermann'"
  exit 1
fi

if [ ! -r "$ADMIN_TOKEN_FILE" ]; then
  echo "ERROR: $ADMIN_TOKEN_FILE not readable"
  exit 1
fi

ADMIN_TOKEN="$(cat "$ADMIN_TOKEN_FILE")"

RESPONSE=$(curl -fsS -X POST \
  -H "X-Admin-Token: $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"device_id\":\"$DEVICE_ID\",\"customer\":\"$CUSTOMER\"}" \
  "$PROXY_URL/v1/admin/issue_key")

KEY=$(echo "$RESPONSE" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("key","ERR"))')

if [ "$KEY" = "ERR" ] || [ -z "$KEY" ]; then
  echo "Failed to generate key. Response:"
  echo "$RESPONSE"
  exit 1
fi

echo "Customer Key for device $DEVICE_ID ($CUSTOMER):"
echo
echo "$KEY"
echo
echo "(in E-Mail-Template einsetzen als {{CUSTOMER_KEY}})"
