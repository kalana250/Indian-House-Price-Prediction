# ══════════════════════════════════════════════
# Dockerfile for Indian House Price Predictor
# ══════════════════════════════════════════════

# Step 1: Start with Python 3.13
# (like choosing what operating system to use)
FROM python:3.13-slim

# Step 2: Who made this
LABEL maintainer="your-name"
LABEL description="Indian House Price Prediction App"

# Step 3: Set working directory inside container
# (like cd /app — go into this folder)
WORKDIR /app

# Step 4: Copy requirements file first
# (copy the list of packages we need)
COPY requirements.txt .

# Step 5: Install all Python packages
# --no-cache-dir = don't save download cache
# (keeps the container small)
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy ALL project files into container
COPY . .

# Step 7: Tell Docker our app uses port 5000
# (open door number 5000)
EXPOSE 5000

# Step 8: Command to start the app
# (what runs when container starts)
CMD ["python", "app.py"]