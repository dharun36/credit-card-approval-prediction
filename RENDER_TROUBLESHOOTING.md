# Render Deployment Troubleshooting Guide

## Common Causes of "Cause of failure could not be determined"

This error typically happens when Render encounters issues during the build or deployment process. Let's check systematically:

---

## 🔍 Step 1: Verify Render Service Configuration

Go to your Render dashboard and check these settings:

### Required Settings:
| Setting | Correct Value | ⚠️ Common Mistake |
|---------|---------------|-------------------|
| **Runtime** | Docker | Using Web Service instead |
| **Dockerfile Path** | `DockerFile` | Using `Dockerfile` (case matters!) |
| **Branch** | `dockerize` | Wrong branch selected |
| **Root Directory** | `/` (empty or root) | Wrong path |

**Action:** 
1. Go to Render → Your Service → Settings
2. Verify "Dockerfile Path" is exactly: `DockerFile`
3. Verify "Branch" matches your pushed branch

---

## 🔍 Step 2: Check Build Logs on Render

**Where to find logs:**
1. Render Dashboard → Your Service
2. Click on the failed deployment
3. Look at "Build Logs" and "Deploy Logs"

**What to look for:**
- Docker build errors
- Missing files errors
- Port binding issues
- Python/package errors

---

## 🔍 Step 3: Most Common Issues & Fixes

### Issue 1: Dockerfile Name Case Sensitivity ⚠️
**Your file:** `DockerFile` (capital D and F)
**Render expects:** Exact match in settings

**Fix:**
```powershell
# Option A: Rename to standard (recommended)
git mv DockerFile Dockerfile
git commit -m "Rename to standard Dockerfile"
git push origin dockerize

# Then update Render settings: Dockerfile Path = Dockerfile
```

**OR keep DockerFile and ensure Render settings match exactly.**

---

### Issue 2: Missing Model Files
If your model files are too large or not committed:

**Check:**
```powershell
git ls-files | Select-String "\.pkl$"
# Should show: best_model.pkl, model.pkl
```

**Fix if missing:**
```powershell
git add best_model.pkl model.pkl
git commit -m "Add model files"
git push origin dockerize
```

---

### Issue 3: Port Binding Issues
Your Dockerfile should use the PORT environment variable:

**Correct (what you have):**
```dockerfile
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

**Wrong:**
```dockerfile
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Issue 4: Requirements.txt Issues
**Check for dependency conflicts:**

```powershell
# Test locally first
pip install -r requirements.txt
```

**Fix if there are conflicts:**
- Update package versions
- Remove incompatible packages
- Test Docker build locally

---

### Issue 5: Missing Static/Template Files
**Check they're committed:**
```powershell
git ls-files templates/
git ls-files static/
```

**Should show:**
- templates/index.html
- static/css/*, static/js/*

---

## 🔧 Quick Diagnostic Commands

Run these locally to catch issues before deploying:

```powershell
# 1. Test Docker build locally
docker build -t test-app -f DockerFile .

# 2. Test Docker run
docker run -p 8000:8000 test-app

# 3. Test with PORT env (like Render)
docker run -e PORT=10000 -p 10000:10000 test-app

# 4. Check logs
docker logs <container-id>

# 5. Verify all files are in image
docker run --rm test-app ls -la /app
```

---

## 🎯 Recommended Fix for Your Case

Based on the error, here's the most likely issue and fix:

### **Issue: Dockerfile Name Mismatch**

**Do this:**

1. **Standardize the Dockerfile name:**
```powershell
# Rename DockerFile to Dockerfile (standard convention)
git mv DockerFile Dockerfile
```

2. **Update docker-compose.yml:**
```yaml
# Change this line:
dockerfile: DockerFile
# To:
dockerfile: Dockerfile
```

3. **Update CI/CD workflow:**
```yaml
# In .github/workflows/ci-cd.yml, change:
docker build ... -f DockerFile .
# To:
docker build ... -f Dockerfile .
```

4. **Commit and push:**
```powershell
git add Dockerfile docker-compose.yml .github/workflows/ci-cd.yml
git commit -m "Standardize to Dockerfile naming"
git push origin dockerize
```

5. **Update Render settings:**
   - Go to Service Settings
   - Dockerfile Path: `Dockerfile` (not DockerFile)
   - Save changes
   - Trigger manual deploy

---

## 🔍 Alternative: Keep DockerFile and Fix Render

If you want to keep the name `DockerFile`:

1. **Verify Render Dockerfile Path setting:**
   - Must be exactly: `DockerFile` (case-sensitive)

2. **Check it's in repo root:**
   ```powershell
   git ls-files | Select-String "^DockerFile$"
   ```

3. **Manual deploy to see real error:**
   - Render Dashboard → Manual Deploy
   - Watch build logs in real-time

---

## 📊 How to Get Better Error Messages

1. **Enable verbose logging in Render:**
   - Settings → Environment
   - Add: `VERBOSE_LOGS=true`

2. **Check specific build phase:**
   - Look for which step failed (build, start, health check)

3. **Test health endpoint:**
   - After deployment, check: `https://your-app.onrender.com/docs`
   - If 502/503: App didn't start
   - If 404: Routes not configured
   - If timeout: Port binding issue

---

## 🚨 Quick Checklist

Before redeploying, verify:

- [ ] Dockerfile path in Render matches actual filename (case-sensitive)
- [ ] All model files (.pkl) are committed and pushed
- [ ] Templates and static files are committed
- [ ] requirements.txt has no conflicts
- [ ] Dockerfile uses `${PORT:-8000}` for port binding
- [ ] Branch in Render settings matches your pushed branch
- [ ] Docker build works locally: `docker build -f DockerFile .`

---

## 💡 Next Steps

1. **Rename to standard Dockerfile (recommended):**
   ```powershell
   git mv DockerFile Dockerfile
   # Update docker-compose.yml and ci-cd.yml
   git commit -m "Standardize Dockerfile name"
   git push origin dockerize
   ```

2. **Update Render:**
   - Dockerfile Path: `Dockerfile`
   - Manual Deploy

3. **Watch the build logs** to see the actual error

Want me to help rename the Dockerfile and update all references? This will likely fix the issue immediately.
