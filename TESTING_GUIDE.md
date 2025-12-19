# 🧪 Complete API Testing Guide

## ✅ Quick Test Using Swagger UI

Your API is running! Test it at: **http://localhost:8000/docs**

---

## 📋 Step-by-Step Test Flow

### **Step 1: Create Admin Account**

1. Open http://localhost:8000/docs
2. Find `POST /api/auth/signup`
3. Click "Try it out"
4. Enter:
```json
{
  "username": "admin1",
  "password": "mypassword",
  "full_name": "Admin User"
}
```
5. Click "Execute"
6. **COPY the `access_token`** from response

---

### **Step 2: Authorize**

1. Click the **🔒 Authorize** button (top right)
2. Paste: `Bearer YOUR_TOKEN_HERE`
   (Include the word "Bearer" + space + your token)
3. Click "Authorize"
4. Click "Close"

---

### **Step 3: Upload Image**

1. Find `POST /api/upload`
2. Click "Try it out"
3. Click "Choose File" and select an image
4. Click "Execute"
5. **COPY the `url`** from response

Example response:
```json
{
  "url": "http://localhost:8000/uploads/abc123.jpg",
  "filename": "abc123.jpg",
  "size": 12345
}
```

---

### **Step 4: Verify Image Accessible**

1. Copy the URL from previous step
2. Paste it in browser: `http://localhost:8000/uploads/abc123.jpg`
3. ✅ Image should display!

---

### **Step 5: Create Blog Post with Image**

1. Find `POST /api/blog`
2. Click "Try it out"
3. Enter:
```json
{
  "title": "My First Post",
  "content": "This is my blog post with an image!",
  "media_url": "http://localhost:8000/uploads/abc123.jpg",
  "author_name": "Admin User"
}
```
4. Click "Execute"
5. Note the blog post `id` from response

---

### **Step 6: Get Blog Post (Public)**

1. Find `GET /api/blog/{post_id}`
2. Enter the `id` from previous step
3. Click "Execute"
4. ✅ Should see your blog post with the image URL!

---

## 🎯 Test Results You Should See

✅ **Signup** → Returns access token  
✅ **Upload Image** → Returns URL  
✅ **Image Accessible** → Opens in browser  
✅ **Create Blog Post** → Stores image URL  
✅ **Get Blog Post** → Shows image URL in `media_url`

---

## 📁 File Locations

- **Uploaded Images**: `c:\Users\DELL\Desktop\backend\uploads\`
- **Database**: Remote MySQL at `98.130.114.230`

---

## 🔧 Testing from Command Line (PowerShell)

If you want to test with commands:

### Login and get token:
```powershell
$body = @{username='admin1';password='mypassword'} | ConvertTo-Json
$response = Invoke-RestMethod -Uri http://localhost:8000/api/auth/login -Method POST -Body $body -ContentType 'application/json'
$token = $response.access_token
Write-Host "Token: $token"
```

### Upload image:
```powershell
$headers = @{Authorization="Bearer $token"}
$file = Get-Item "C:\path\to\your\image.jpg"
$response = Invoke-RestMethod -Uri http://localhost:8000/api/upload -Method POST -Headers $headers -Form @{file=$file}
Write-Host "Image URL: $($response.url)"
```

---

## ✅ Your API is Working!

All endpoints are ready:
- ✅ Authentication (signup/login)
- ✅ Image upload
- ✅ Blog CRUD
- ✅ Public access to content

**Use Swagger UI at http://localhost:8000/docs for easiest testing!**
