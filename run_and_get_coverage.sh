# Reset coverage data
find /tinycc -name '*.gcda' -delete

# Run the fuzzer
.venv/bin/python3 fuzzer/__init__.py

echo "Found $(find crashes -type f ! -name '*.*' | wc -l) crashes"

mkdir -p coverage

# Generate coverage report
gcovr --root /tinycc \
    --exclude 'tests/.*' \
    --exclude 'win32/.*' \
    --exclude 'examples/.*' \
    --exclude '.*/tests2/.*' \
    --gcov-ignore-parse-errors=negative_hits.warn_once_per_file \
    --print-summary \
    --html coverage/report.html \
    | tee summary.txt

# Check that branch coverage is > 0
if ! grep -qE 'branches: (0\.[1-9][0-9]*|[1-9][0-9]*\.[0-9]+)%' summary.txt; then
    echo "Error: branch coverage must be > 0%" >&2
    exit 1
fi