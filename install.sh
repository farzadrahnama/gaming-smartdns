#!/usr/bin/env bash
set -e
echo "🎮 Setting up SmartDNS & Panel..."
read -p "Enter Server IP: " IP
read -p "Enter Domain (e.g. dns.example.com): " DOMAIN
sed "s/YOUR_SERVER_IP/$IP/g" sniproxy.yaml.example > sniproxy.yaml
sed -i "s/your-domain.com/$DOMAIN/g" app.py
docker compose up -d
echo "✅ Done! Start panel: uvicorn app:app --host 0.0.0.0 --port 8080"
