#!/bin/bash

# ========================================
# PahamKode Deployment Script
# ========================================
# Script untuk deploy/update PahamKode di Azure VM
# Usage: ./deploy.sh

set -e  # Exit on error

echo "🚀 Starting PahamKode Deployment..."

# ==================== CONFIGURATION ====================

APP_DIR="/home/ikhsan/PahamKodev2"
SERVICE_NAME="pahamkode"
VENV_DIR="$APP_DIR/venv"
PYTHON_VERSION="python3.11"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ==================== FUNCTIONS ====================

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ==================== DEPLOYMENT STEPS ====================

# Step 1: Backup current .env
echo "📦 Step 1: Backup .env file..."
if [ -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env" "$APP_DIR/.env.backup"
    print_status ".env backed up"
else
    print_warning ".env not found - akan dibuat baru"
fi

# Step 2: Pull latest code dari GitHub
echo ""
echo "📥 Step 2: Pull latest code from GitHub..."
cd "$APP_DIR"
git fetch origin
git pull origin main
print_status "Code updated"

# Step 3: Restore .env
echo ""
echo "🔧 Step 3: Restore .env file..."
if [ -f "$APP_DIR/.env.backup" ]; then
    cp "$APP_DIR/.env.backup" "$APP_DIR/.env"
    print_status ".env restored"
fi

# Step 4: Create/activate virtual environment
echo ""
echo "🐍 Step 4: Setup Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    print_warning "Virtual environment not found, creating..."
    $PYTHON_VERSION -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
print_status "Virtual environment activated"

# Step 5: Install/Update dependencies
echo ""
echo "📚 Step 5: Install dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_status "Dependencies installed"

# Step 6: Update systemd service file
echo ""
echo "⚙️  Step 6: Update systemd service..."
sudo cp deployment/pahamkode.service /etc/systemd/system/
sudo systemctl daemon-reload
print_status "Service file updated"

# Step 7: Update nginx configuration
echo ""
echo "🌐 Step 7: Update nginx configuration..."
if [ -f "/etc/nginx/sites-available/pahamkode" ]; then
    sudo cp deployment/nginx-pahamkode.conf /etc/nginx/sites-available/pahamkode
    sudo nginx -t
    print_status "Nginx configuration updated"
else
    print_warning "Nginx config not found - skip (first deployment?)"
fi

# Step 8: Restart services
echo ""
echo "🔄 Step 8: Restart services..."
sudo systemctl restart $SERVICE_NAME
sudo systemctl restart nginx
print_status "Services restarted"

# Step 9: Check service status
echo ""
echo "🔍 Step 9: Verify deployment..."
sleep 3

if sudo systemctl is-active --quiet $SERVICE_NAME; then
    print_status "Service $SERVICE_NAME is running"
    
    # Show service logs (last 20 lines)
    echo ""
    echo "📋 Recent logs:"
    sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
else
    print_error "Service $SERVICE_NAME is NOT running!"
    echo ""
    echo "📋 Error logs:"
    sudo journalctl -u $SERVICE_NAME -n 50 --no-pager
    exit 1
fi

# Step 10: Health check
echo ""
echo "🏥 Step 10: Health check..."
sleep 2

if curl -s http://localhost:8501 > /dev/null; then
    print_status "App is responding on port 8501"
else
    print_warning "App not responding on port 8501 (might be starting up)"
fi

# ==================== SUMMARY ====================

echo ""
echo "================================================"
echo "🎉 Deployment Complete!"
echo "================================================"
echo ""
echo "📊 Status:"
sudo systemctl status $SERVICE_NAME --no-pager
echo ""
echo "🌐 Access URLs:"
echo "  - Local: http://localhost:8501"
echo "  - Public: http://$(curl -s ifconfig.me):8501"
echo ""
echo "📝 Useful commands:"
echo "  - View logs:    sudo journalctl -u $SERVICE_NAME -f"
echo "  - Restart app:  sudo systemctl restart $SERVICE_NAME"
echo "  - Stop app:     sudo systemctl stop $SERVICE_NAME"
echo "  - Start app:    sudo systemctl start $SERVICE_NAME"
echo ""
print_status "Deployment successful! 🚀"
