# Auto-activate .venv on shell startup
if [ -f "${PWD}/.venv/Scripts/activate" ]; then
    source "${PWD}/.venv/Scripts/activate"
fi

# Fallback for users starting from different directories
if [ -z "$VIRTUAL_ENV" ] && [ -f "$(dirname "$PWD")/.venv/Scripts/activate" ]; then
    source "$(dirname "$PWD")/.venv/Scripts/activate"
fi
