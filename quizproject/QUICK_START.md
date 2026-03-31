# 🚀 Quick Start Guide - Admin Quiz Management System

**Time to Deploy**: 5-10 minutes  
**Difficulty**: Easy  
**Prerequisites**: Django 6.0.2, Python 3.12

---

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (1 min)

```bash
cd quizproject

# Install Excel support
pip install openpyxl

# Add to requirements.txt
echo "openpyxl>=3.0.0" >> requirements.txt
```

### Step 2: Create/Update Models (2 min)

Copy these files to `quizapp/`:
- `admin_models.py`
- `validators.py`
- `file_parsers.py`
- `services.py`
- `admin_forms.py`
- `admin_views.py`
- `admin_urls.py`

### Step 3: Run Migrations (1 min)

```bash
python manage.py makemigrations quizapp
python manage.py migrate
```

### Step 4: Create Templates (1 min)

```bash
mkdir -p quizapp/Templates/quizapp/admin

# Copy all HTML files to quizapp/Templates/quizapp/admin/:
```

Templates needed:
- dashboard.html
- bulk_upload.html
- preview_upload.html
- upload_success.html
- upload_history.html
- upload_detail.html
- create_quiz.html
- quiz_detail.html
- audit_log.html

### Step 5: Update URL Configuration (1 min)

In `quizproject/urls.py`:

```python
# Add this URL pattern
path('admin/quiz/', include('quizapp.admin_urls')),
```

### Step 6: Test (1 min)

```bash
python manage.py runserver
```

Visit: `http://localhost:8000/admin/quiz/`

---

## 🎯 First Upload (3 minutes)

### Prerequisites
- Admin user account
- One quiz created (or create via dashboard)

### Steps

1. **Go to Dashboard**
   ```
   http://localhost:8000/admin/quiz/
   ```

2. **Create a Test Quiz**
   - Click "+ Create New Quiz"
   - Fill in title, description, time limit
   - Click "Create Quiz"

3. **Create Test File**
   
   **File: `test_questions.csv`**
   ```csv
   question,options,correct_answer,points
   What is 2+2?,3|4|5|6,4,1
   What is the capital of France?,London|Paris|Berlin,Paris,1
   What is Python?,A language|A snake|A food,A language,1
   ```

4. **Upload File**
   - Click "📤 Bulk Upload Questions"
   - Select your quiz
   - Upload the CSV file
   - Click "Start Upload & Validation"

5. **Review Preview**
   - Check the validation results
   - Verify 3 valid rows
   - Check the confirmation box
   - Click "Commit to Database"

6. **Success!**
   - View the success page
   - Click "View Questions" to see your uploaded questions

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Admin dashboard loads at `/admin/quiz/`
- [ ] Can create new quiz
- [ ] Can upload CSV file
- [ ] Preview shows 3 valid rows
- [ ] Can commit upload
- [ ] Success page appears
- [ ] Questions appear in quiz detail
- [ ] Audit log shows the action

---

## 🎬 Common Tasks

### Upload CSV File

```bash
# Drag and drop or browse to select file
# Supported files: .csv, .json, .xlsx
# Max size: 10MB
```

### Create Manual Quiz Entry

```python
from quizapp.services import QuizManagementService

Quiz = QuizManagementService.create_quiz(
    title="My Quiz",
    description="Test description",
    admin_user=user,
    time_limit=60
)
```

### Check Upload Status

```
Visit: /admin/quiz/uploads/
- See all uploads
- Filter by status
- Download error reports
```

### View Audit Trail

```
Visit: /admin/quiz/audit/
- See all admin actions
- Filter by action type
- View details
```

---

## 🔍 Troubleshooting

### Templates Not Found
```
❌ Error: TemplateDoesNotExist: quizapp/admin/dashboard.html

✅ Solution:
1. Check directory: quizapp/Templates/quizapp/admin/
2. Verify file names exactly match
3. Check settings.py has correct TEMPLATES config
```

### Module Not Found
```
❌ ImportError: No module named 'openpyxl'

✅ Solution:
pip install openpyxl
```

### Permission Denied
```
❌ Error: 403 Forbidden

✅ Solution:
1. Login with staff/superuser account
2. User must have is_staff=True
```

### File Upload Fails
```
❌ Error: Unsupported file format

✅ Solution:
- Use .csv, .json, or .xlsx
- Check file size < 10MB
- Ensure UTF-8 encoding
```

---

## 📚 File Formats

### CSV (simplest)
```csv
question,options,correct_answer,points
What is X?,A|B|C,B,1
```

### JSON
```json
{
  "questions": [
    {
      "question": "What is X?",
      "options": ["A", "B", "C"],
      "correct_answer": "B",
      "points": 1
    }
  ]
}
```

### Excel
- Column A: question
- Column B: options (pipe-separated)
- Column C: correct_answer
- Column D: points

---

## 🔐 Security Notes

⚠️ **Important**:
- Only admins can access system
- All uploads logged
- Temporary files auto-deleted
- Transactions atomic (safe)
- CSRF protected

---

## 📞 Need Help?

1. Check logs: `DJANGO_LOG_DIR/bulk_upload.log`
2. Review error report in admin
3. Check audit trail for tracking
4. See ADMIN_QUIZ_SYSTEM_GUIDE.md for details
5. See ADMIN_SYSTEM_SUMMARY.md for architecture

---

## 🎓 Next Steps

After initial setup:

1. ✅ Test with sample CSV
2. ✅ Test with sample JSON
3. ✅ Try test with Excel (if openpyxl installed)
4. ✅ Create real quiz
5. ✅ Upload real questions
6. ✅ Verify audit trail
7. ✅ Customize forms (optional)
8. ✅ Set up email notifications (optional)

---

## 📊 Example Workflows

### Workflow: Bulk Import Quiz Questions

```
1. Prepare CSV file with all questions
   ↓
2. Go to /admin/quiz/upload/
   ↓
3. Upload CSV file
   ↓
4. Review preview (should show 0 errors)
   ↓
5. Click "Commit to Database"
   ↓
6. Success! Questions are live
   ↓
7. Students can now take the quiz
```

### Workflow: Fix Bad Upload

```
1. Questions uploaded with errors
   ↓
2. Go to /admin/quiz/uploads/
   ↓
3. Find failed upload
   ↓
4. Click "Details"
   ↓
5. Download "Error Report as CSV"
   ↓
6. Review errors
   ↓
7. Fix in spreadsheet
   ↓
8. Re-upload corrected file
```

### Workflow: Audit Trail Check

```
1. Go to /admin/quiz/audit/
   ↓
2. Filter by action (e.g., "upload_commit")
   ↓
3. View who did what and when
   ↓
4. Check details (JSON)
   ↓
5. Export if needed
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Installation | 2 min |
| First CSV upload | 3 min |
| JSON upload | 5 min |
| Excel upload | 5 min |
| Error fixing | 10 min |
| Audit log review | 2 min |
| Full workflow | 15 min |

---

## 🎉 You're Done!

Your admin system is now ready. Start by:

1. Creating a quiz
2. Uploading your first CSV file
3. Reviewing the success page
4. Checking the audit log

**Happy uploading! 🚀**

---

**Quick Reference**:
- Dashboard: `/admin/quiz/`
- Upload: `/admin/quiz/upload/`
- History: `/admin/quiz/uploads/`
- Audit: `/admin/quiz/audit/`
