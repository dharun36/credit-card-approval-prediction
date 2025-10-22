# 🚀 Deployment Checklist for Render

Follow these steps to deploy your credit card approval app to Render with CI/CD.

## ✅ Pre-Deployment Setup

### 1. Push Your Code to GitHub
```powershell
# Make sure all changes are committed
git status

# Commit any pending changes
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git push origin dockerize
```

### 2. Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select repository: `dharun36/credit-card-approval-prediction`
5. Configure the service:

   | Setting | Value |
   |---------|-------|
   | **Name** | `credit-card-approval` (or your choice) |
   | **Region** | Choose closest to your users |
   | **Branch** | `dockerize` (or `main` after merge) |
   | **Runtime** | **Docker** |
   | **Dockerfile Path** | `Dockerfile` |
   | **Instance Type** | Free (or paid for production) |

6. Click **"Create Web Service"**

### 3. Configure Environment Variables on Render (Optional)

If you need custom settings, add these in Render:
- Go to your service → **Environment** tab
- Add variables:

| Key | Value | Notes |
|-----|-------|-------|
| `PORT` | Auto-set by Render | Don't add manually |
| `LOG_LEVEL` | `info` | Optional |
| `ALLOWED_ORIGINS` | `https://your-app.onrender.com` | For production CORS |
| `MODEL_PATH` | `best_model.pkl` | Optional (default works) |
| `SCALER_PATH` | `scaler.pkl` | Optional (default works) |

**Note:** `PORT` is automatically set by Render. Your Dockerfile already handles it.

### 4. Get Render Deploy Hook URL

1. In your Render service, go to **Settings**
2. Scroll to **Deploy Hook**
3. Click **"Create Deploy Hook"** if not created
4. Copy the URL (looks like):
   ```
   https://api.render.com/deploy/srv-xxxxxxxxxxxxx?key=yyyyyyyyyyyy
   ```
5. **Keep this secret!** Don't commit it to your repo.

### 5. Add Deploy Hook to GitHub Secrets

1. Go to your GitHub repository
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `RENDER_DEPLOY_HOOK_URL`
5. Value: Paste the deploy hook URL from step 4
6. Click **"Add secret"**

---

## 🔄 How Auto-Deployment Works

Once configured, every time you push to `main` or `dockerize`:

```
1. Push code to GitHub
   ↓
2. GitHub Actions runs CI/CD pipeline
   ↓
3. Tests run (pytest validates API)
   ↓
4. Docker image builds
   ↓
5. Container test passes
   ↓
6. Webhook triggers Render deployment
   ↓
7. Render pulls code and rebuilds
   ↓
8. Your app is live! 🎉
```

**Timeline:** Usually 3-5 minutes from push to live.

---

## 🧪 Test Your Deployment

### First-Time Deployment

After Render finishes building:

1. **Get your app URL** from Render dashboard (e.g., `https://credit-card-approval-xxxxx.onrender.com`)

2. **Test the endpoints:**

```powershell
# Health check (API docs)
curl https://your-app.onrender.com/docs

# Test prediction
curl -X POST https://your-app.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PriorDefault": 0,
    "CreditScore": 750,
    "YearsEmployed": 5.0,
    "Income": 60000.0,
    "Employed": 1,
    "Debt": 10000.0,
    "Age": 35
  }'
```

3. **Expected response:**
```json
{
  "approval": true,
  "message": "Approved",
  "probability": 0.85,
  "confidence": "85.0%"
}
```

### Subsequent Deployments

```powershell
# Make changes
git add app.py
git commit -m "Update validation logic"
git push origin dockerize

# Watch GitHub Actions
# Go to: https://github.com/dharun36/credit-card-approval-prediction/actions

# Wait for deployment
# Check Render dashboard for build logs
```

---

## 📊 Monitoring Your Deployment

### GitHub Actions Logs
- **URL:** `https://github.com/dharun36/credit-card-approval-prediction/actions`
- Shows: Tests, build status, deployment trigger

### Render Logs
- **Dashboard:** `https://dashboard.render.com/`
- Click your service → **Logs** tab
- Shows: Build logs, runtime logs, errors

---

## 🐛 Troubleshooting

### Deployment not triggering
- ✅ Check `RENDER_DEPLOY_HOOK_URL` is set in GitHub Secrets
- ✅ Verify you pushed to `main` or `dockerize` (not a PR)
- ✅ Check GitHub Actions logs for webhook call

### Render build failing
- ✅ Check Dockerfile path is set to `Dockerfile` (standard naming)
- ✅ Verify all required files are in repo (best_model.pkl, templates/, static/)
- ✅ Check Render build logs for specific error

### App not responding after deployment
- ✅ Verify `PORT` env is not manually set (Render auto-sets it)
- ✅ Check Dockerfile uses `${PORT:-8000}` syntax
- ✅ Look at Render runtime logs for startup errors

### Tests failing in CI
```powershell
# Run tests locally first
pytest tests/ -v

# Fix any failing tests before pushing
```

### CORS errors in production
- Update `ALLOWED_ORIGINS` env var on Render:
  ```
  ALLOWED_ORIGINS=https://your-frontend.com,https://your-app.onrender.com
  ```

---

## 🔐 Security Notes

### DO NOT commit:
- ❌ `.env` file (has secrets)
- ❌ Render deploy hook URL
- ❌ Any API keys or passwords

### DO commit:
- ✅ `.env.example` (template with dummy values)
- ✅ Docker and CI/CD configs
- ✅ Model files (if not too large)

---

## 🎯 Production Readiness

Before going live with real users:

- [ ] Switch from Free tier to paid instance (for reliability)
- [ ] Set up custom domain in Render
- [ ] Configure HTTPS (auto-enabled by Render)
- [ ] Add monitoring/alerts (Render has built-in alerts)
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Review and update CORS origins for production
- [ ] Load test your API
- [ ] Set up database if needed (currently stateless)

---

## 📚 Useful Commands

```powershell
# Check CI/CD status
git push origin dockerize
# Then visit: https://github.com/dharun36/credit-card-approval-prediction/actions

# Manual Render deployment (without pushing code)
curl -X POST https://api.render.com/deploy/srv-xxxxx?key=yyyyy

# View Render logs
# Dashboard → Your Service → Logs

# Rollback in Render
# Dashboard → Your Service → Manual Deploy → Select previous commit
```

---

## ✅ Final Checklist

Before your first deployment:

- [ ] Code pushed to GitHub
- [ ] Render service created with Docker runtime
- [ ] Dockerfile path set to `Dockerfile`
- [ ] Deploy hook URL copied from Render
- [ ] `RENDER_DEPLOY_HOOK_URL` added to GitHub Secrets
- [ ] Branch set to `dockerize` or `main`
- [ ] All tests passing locally (`pytest tests/ -v`)

**Ready to deploy?**
```powershell
git push origin dockerize
```

Then watch the magic happen in GitHub Actions! 🚀
