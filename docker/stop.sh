#!/bin/bash
# Stop and clean up Quantum LMS Docker containers

echo "========================================"
echo "  Stopping Quantum LMS"
echo "========================================"
echo ""

cd "$(dirname "$0")"

docker-compose down

echo ""
echo "[OK] Containers stopped and removed"
echo ""
echo "To also remove volumes (CAREFUL: deletes database):"
echo "  docker-compose down -v"
echo ""
