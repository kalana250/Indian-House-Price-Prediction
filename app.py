# ══════════════════════════════════════════════
# app.py - Flask Web Application
# This serves your house price prediction model
# ══════════════════════════════════════════════

from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np
import os

# Create Flask app
app = Flask(__name__)

# ── Load your trained model ─────────────────────────────────
# (you'll save these from your notebook)
MODEL_PATH     = 'model.pkl'
SCALER_PATH    = 'scaler.pkl'
ENCODINGS_PATH = 'encodings.pkl'

model     = None
scaler    = None
encodings = None

def load_models():
    """Load saved model files"""
    global model, scaler, encodings
    
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
            print("✅ Model loaded")
        
        if os.path.exists(SCALER_PATH):
            with open(SCALER_PATH, 'rb') as f:
                scaler = pickle.load(f)
            print("✅ Scaler loaded")
            
        if os.path.exists(ENCODINGS_PATH):
            with open(ENCODINGS_PATH, 'rb') as f:
                encodings = pickle.load(f)
            print("✅ Encodings loaded")
            
    except Exception as e:
        print(f"⚠️ Could not load models: {e}")
        print("   Running in demo mode")

# Load on startup
load_models()

# ── HTML Template ───────────────────────────────────────────
# This is your web page
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>House Price Predictor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1565c0;
            text-align: center;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 25px;
            font-size: 14px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            font-weight: bold;
            margin-bottom: 5px;
            color: #444;
            font-size: 13px;
        }
        select, input {
            width: 100%;
            padding: 10px;
            border: 1.5px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            box-sizing: border-box;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #1565c0;
        }
        .row {
            display: flex;
            gap: 15px;
        }
        .row .form-group {
            flex: 1;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #1565c0;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background: #0d47a1;
        }
        #result {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #e8f5e9;
            border-radius: 10px;
            text-align: center;
        }
        .price {
            font-size: 36px;
            font-weight: bold;
            color: #2e7d32;
        }
        .price-label {
            color: #666;
            font-size: 13px;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🏠 House Price Predictor</h1>
    <p class="subtitle">Indian Real Estate Price Estimation</p>
    
    <div class="row">
        <div class="form-group">
            <label>City</label>
            <select id="city">
                <option value="Mumbai">Mumbai</option>
                <option value="Delhi">Delhi</option>
                <option value="Bangalore">Bangalore</option>
                <option value="Hyderabad">Hyderabad</option>
                <option value="Chennai">Chennai</option>
                <option value="Pune">Pune</option>
                <option value="Patna">Patna</option>
            </select>
        </div>
        <div class="form-group">
            <label>Locality</label>
            <input type="text" id="locality" 
                   placeholder="e.g. Andheri West">
        </div>
    </div>
    
    <div class="form-group">
        <label>Property Type</label>
        <select id="proptype">
            <option value="Multistorey Apartment">
                Multistorey Apartment
            </option>
            <option value="Independent House">
                Independent House
            </option>
            <option value="Builder Floor Apartment">
                Builder Floor Apartment
            </option>
            <option value="Independent Villa">
                Independent Villa
            </option>
            <option value="Studio Apartment">
                Studio Apartment
            </option>
        </select>
    </div>
    
    <div class="row">
        <div class="form-group">
            <label>Furnishing</label>
            <select id="furnishing">
                <option value="Semi-Furnished">Semi-Furnished</option>
                <option value="Furnished">Furnished</option>
                <option value="Unfurnished">Unfurnished</option>
            </select>
        </div>
        <div class="form-group">
            <label>Rent or Sale</label>
            <select id="rentorsale">
                <option value="Sale">Sale</option>
                <option value="Rent">Rent</option>
            </select>
        </div>
    </div>
    
    <div class="row">
        <div class="form-group">
            <label>Bedrooms</label>
            <select id="bedrooms">
                <option value="1">1 BHK</option>
                <option value="2">2 BHK</option>
                <option value="3" selected>3 BHK</option>
                <option value="4">4 BHK</option>
                <option value="5">5 BHK</option>
            </select>
        </div>
        <div class="form-group">
            <label>Bathrooms</label>
            <select id="bathrooms">
                <option value="1">1</option>
                <option value="2" selected>2</option>
                <option value="3">3</option>
                <option value="4">4</option>
            </select>
        </div>
    </div>
    
    <div class="form-group">
        <label>Carpet Area (Sq-ft)</label>
        <input type="number" id="area" 
               value="1000" min="100" max="50000">
    </div>
    
    <button onclick="predict()">💰 Predict Price</button>
    
    <div id="result">
        <div class="price-label">Estimated Price</div>
        <div class="price" id="price-display">—</div>
        <div id="details" 
             style="color:#555; font-size:13px; margin-top:8px;">
        </div>
    </div>
</div>

<script>
function predict() {
    var data = {
        city:       document.getElementById('city').value,
        locality:   document.getElementById('locality').value,
        proptype:   document.getElementById('proptype').value,
        furnishing: document.getElementById('furnishing').value,
        rentorsale: document.getElementById('rentorsale').value,
        bedrooms:   document.getElementById('bedrooms').value,
        bathrooms:  document.getElementById('bathrooms').value,
        area:       document.getElementById('area').value
    };
    
    document.getElementById('price-display').innerText = 
        'Calculating...';
    document.getElementById('result').style.display = 'block';
    
    fetch('/predict', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(result => {
        if (result.success) {
            document.getElementById('price-display').innerText = 
                result.formatted_price;
            document.getElementById('details').innerHTML = 
                result.city + ' | ' + 
                result.bedrooms + ' BHK | ' +
                result.area + ' sq-ft';
        } else {
            document.getElementById('price-display').innerText = 
                'Error: ' + result.error;
        }
    })
    .catch(err => {
        document.getElementById('price-display').innerText = 
            'Connection error';
    });
}
</script>
</body>
</html>
"""

# ── ROUTES ──────────────────────────────────────────────────

@app.route('/')
def home():
    """Serve the main page"""
    return render_template_string(HTML_PAGE)

@app.route('/predict', methods=['POST'])
def predict():
    """Receive form data and return prediction"""
    try:
        # Get data from form
        data = request.get_json()
        
        city        = data.get('city', 'Mumbai')
        locality    = data.get('locality', 'Unknown')
        proptype    = data.get('proptype', 'Multistorey Apartment')
        furnishing  = data.get('furnishing', 'Semi-Furnished')
        rentorsale  = data.get('rentorsale', 'Sale')
        bedrooms    = int(data.get('bedrooms', 3))
        bathrooms   = int(data.get('bathrooms', 2))
        area        = float(data.get('area', 1000))
        
        # If model is loaded, use it
        if model is not None and scaler is not None:
            # Apply encodings and predict
            # (uses your saved model)
            prediction = get_real_prediction(
                city, locality, proptype, 
                furnishing, rentorsale,
                bedrooms, bathrooms, area
            )
        else:
            # Demo mode if model not loaded
            prediction = get_demo_prediction(
                city, bedrooms, area, rentorsale
            )
        
        # Format price
        if prediction >= 10_000_000:
            formatted = f"₹{prediction/10_000_000:.2f} Crore"
        elif prediction >= 100_000:
            formatted = f"₹{prediction/100_000:.1f} Lakhs"
        else:
            formatted = f"₹{prediction:,.0f}"
        
        return jsonify({
            'success':        True,
            'formatted_price': formatted,
            'exact_price':    prediction,
            'city':           city,
            'bedrooms':       bedrooms,
            'area':           area
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error':   str(e)
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status':       'running',
        'model_loaded': model is not None
    })

# ── HELPER FUNCTIONS ────────────────────────────────────────

def get_real_prediction(city, locality, proptype,
                        furnishing, rentorsale,
                        bedrooms, bathrooms, area):
    """Use your real trained model"""
    # Build input same way as notebook
    import pandas as pd
    
    input_data = {col: 0.0 for col in scaler.feature_names_in_}
    
    user_input = {
        'city':             city,
        'locality':         locality,
        'propertyType':     proptype,
        'furnishing':       furnishing,
        'RentOrSale':       rentorsale,
        'bedrooms':         float(bedrooms),
        'bathrooms':        float(bathrooms),
        'carpetArea':       float(area),
        'flrNum':           2.0,
        'totalFlrNum':      5.0,
        'postedOn_DaysAgo': 30.0,
    }
    
    input_data.update(user_input)
    df = pd.DataFrame([input_data])
    
    # Apply encodings
    for col, mapping in encodings.items():
        if col in df.columns:
            val = df[col].iloc[0]
            df[col] = mapping.get(val, len(mapping)//2)
    
    # Scale and predict
    scaled = scaler.transform(
        df[scaler.feature_names_in_].astype(float)
    )
    log_pred = model.predict(scaled)[0]
    
    return float(np.exp(log_pred))

def get_demo_prediction(city, bedrooms, area, rentorsale):
    """Demo prediction when model not loaded"""
    base = 15000 if rentorsale == 'Rent' else 3500000
    
    city_mult = {
        'Mumbai': 3.9, 'Delhi': 2.8,
        'Bangalore': 2.6, 'Pune': 2.0,
        'Hyderabad': 1.8, 'Chennai': 1.7,
        'Patna': 0.85
    }.get(city, 1.5)
    
    return base * city_mult * (area/1000) * (1 + (bedrooms-2)*0.18)

# ── START APP ───────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 45)
    print("  🏠 House Price Predictor Starting...")
    print("=" * 45)
    print(f"  Open browser: http://localhost:5000")
    print("  Press Ctrl+C to stop")
    print("=" * 45)
    
    app.run(
        host='0.0.0.0',  # accept connections from anywhere
        port=5000,
        debug=False
    )