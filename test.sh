#!/bin/bash

# === Test Configuration ===
YEAR=2025
GP="Spanish Grand Prix"
TYPE="R"
DRIVERS=("VER" "LEC" "NOR")

RUN_SCRIPT="./run.sh"

echo "=== Testing: Best Laps + Laptime Distribution ==="
$RUN_SCRIPT --year "$YEAR" --gp "$GP" --type "$TYPE" --best-laps || exit 1

echo
echo "=== Testing: Results ==="
$RUN_SCRIPT --year "$YEAR" --gp "$GP" --type "$TYPE" --results || exit 1

echo
echo "=== Testing: Position Changes ==="
$RUN_SCRIPT --year "$YEAR" --gp "$GP" --type "$TYPE" --position-changes || exit 1

echo
echo "=== Testing: Strategy ==="
$RUN_SCRIPT --year "$YEAR" --gp "$GP" --type "$TYPE" --strategy || exit 1

echo
echo "=== Testing: Driver Lap Styling (for multiple drivers) ==="
for drv in "${DRIVERS[@]}"; do
  echo "--- Driver: $drv ---"
  $RUN_SCRIPT --year "$YEAR" --gp "$GP" --type "$TYPE" --driver-styling --driver "$drv" || exit 1
done

echo
echo "✅ All CLI tests completed successfully!"
