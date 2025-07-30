# 🚀 Deployment Guide - FraudGuard AI

## Quick Deploy to Streamlit Cloud

### Step 1: Fork the Repository
1. Go to [https://github.com/Cngh10/Fraud-Detection-Project](https://github.com/Cngh10/Fraud-Detection-Project)
2. Click the "Fork" button to create your own copy

### Step 2: Deploy to Streamlit Cloud
1. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your forked repository
5. Set the file path to: `app.py`
6. Click "Deploy"

### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.streamlit.app`
- Share this URL with others to use your fraud detection system

## Alternative Deployment Options

### Heroku Deployment
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy to Heroku
heroku create your-fraudguard-app
git push heroku main
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t fraudguard-ai .
docker run -p 8501:8501 fraudguard-ai
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Access at http://localhost:8501
```

## Environment Variables (Optional)

For production deployment, you can set these environment variables:

```bash
# Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Troubleshooting

### Common Issues:

1. **Model Loading Error**: Ensure `final_xgboost_model.joblib` is in the root directory
2. **Dependencies Error**: Check that all packages in `requirements.txt` are installed
3. **Port Issues**: Make sure port 8501 is available
4. **Memory Issues**: The model file is ~134KB, should work on most platforms

### Performance Tips:

- Use Streamlit Cloud for best performance
- The app loads the model once and caches it
- Interactive charts may take a moment to render
- For high-traffic deployment, consider using multiple instances

## Support

If you encounter any issues:
1. Check the [Streamlit documentation](https://docs.streamlit.io/)
2. Review the [GitHub repository](https://github.com/Cngh10/Fraud-Detection-Project)
3. Open an issue on GitHub

---

**🛡️ FraudGuard AI** - Ready for deployment! 🚀 