#!/usr/bin/env bash
set -e

echo "=================================================="
echo "  RWE Health Analytics - Safe Project Setup"
echo "=================================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating project structure...${NC}"

# Carpetas de datos y código
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/interim
mkdir -p notebooks

mkdir -p src/rwe_health_analytics/data
mkdir -p src/rwe_health_analytics/data_generation
mkdir -p src/rwe_health_analytics/models
mkdir -p src/rwe_health_analytics/evaluation
mkdir -p src/rwe_health_analytics/visualization
mkdir -p src/rwe_health_analytics/utils

mkdir -p tests/data
mkdir -p tests/models
mkdir -p dashboard/components
mkdir -p docs
mkdir -p models
mkdir -p logs
mkdir -p .github/workflows

echo -e "${GREEN}✓ Directories created${NC}"

echo -e "${BLUE}Ensuring __init__.py files exist...${NC}"

for f in \
  src/rwe_health_analytics/__init__.py \
  src/rwe_health_analytics/data/__init__.py \
  src/rwe_health_analytics/data_generation/__init__.py \
  src/rwe_health_analytics/models/__init__.py \
  src/rwe_health_analytics/evaluation/__init__.py \
  src/rwe_health_analytics/visualization/__init__.py \
  src/rwe_health_analytics/utils/__init__.py \
  tests/__init__.py \
  tests/data/__init__.py \
  tests/models/__init__.py
do
  if [ ! -f "$f" ]; then
    touch "$f"
    echo "  - Created $f"
  else
    echo "  - Skipped $f (already exists)"
  fi
done

echo -e "${GREEN}✓ Package files ready${NC}"

echo -e "${BLUE}Creating .env (if missing)...${NC}"

if [ ! -f .env ]; then
  cat > .env << 'EOF'
PROJECT_NAME=rwe-health-analytics
DATA_DIR=data
MODELS_DIR=models
LOGS_DIR=logs
LOG_LEVEL=INFO
EOF
  echo "  - .env created"
else
  echo "  - Skipped .env (already exists)"
fi

echo -e "${BLUE}Creating pytest.ini (if missing)...${NC}"

if [ ! -f pytest.ini ]; then
  cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -vv
    --tb=short
pythonpath = src
EOF
  echo "  - pytest.ini created"
else
  echo "  - Skipped pytest.ini (already exists)"
fi

echo -e "${BLUE}Creating sample test for HealthcareDataLoader (if missing)...${NC}"

if [ ! -f tests/test_data_loader.py ]; then
  cat > tests/test_data_loader.py << 'EOF'
"""Basic tests for HealthcareDataLoader."""

from rwe_health_analytics.data.data_loader import HealthcareDataLoader


def test_loader_initialization():
    loader = HealthcareDataLoader()
    assert loader.data_dir is not None
EOF
  echo "  - tests/test_data_loader.py created"
else
  echo "  - Skipped tests/test_data_loader.py (already exists)"
fi

echo ""
echo "=================================================="
echo "  ✓ Safe Project Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Activa el entorno virtual:"
echo "     venv\\Scripts\\activate  (Windows)"
echo ""
echo "  2. Instala (o actualiza) dependencias si hace falta:"
echo "     pip install -r requirements.txt"
echo ""
echo "  3. Genera datos sintéticos:"
echo "     python src/rwe_health_analytics/data_generation/synthetic_data_generator.py"
echo ""
echo "  4. Lanza los tests:"
echo "     pytest"
echo ""
echo "Happy coding! 🚀"
echo ""
