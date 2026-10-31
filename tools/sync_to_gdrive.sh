#!/usr/bin/env bash
# Beyond Likes Continuous Google Drive Sync Utility
# Synchronizes local development with shared Google Drive storage

set -e

SOURCE_DIR="/home/ayush-pandey/RESEARCH_TO_PRODUCT_VENTURE"
TARGET_DIR="/home/ayush-pandey/GoogleDrive/RESEARCH_TO_PRODUCT_VENTURE"
NOTEBOOK_TARGET="/home/ayush-pandey/GoogleDrive/Colab Notebooks"

echo "=== 🔄 Beyond Likes -> Google Drive Sync ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"

rsync -avu \
  --exclude='.venv' \
  --exclude='.venv_py312' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  "$SOURCE_DIR/" "$TARGET_DIR/"

# Copy latest training notebook to Colab root folder for 1-click execution
if [ -d "$NOTEBOOK_TARGET" ]; then
  cp -u "$SOURCE_DIR/model_pipeline/train_massive_scale_colab.ipynb" "$NOTEBOOK_TARGET/Beyond_Likes_Massive_Scale_Training.ipynb" 2>/dev/null || true
fi

echo "✅ Google Drive sync complete at $(date)!"
