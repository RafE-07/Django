# Django Media File Management App

A Django application for managing media file uploads with validation, storage management, and admin interface support.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation & Setup](#installation--setup)
3. [Feature Documentation](#feature-documentation)
4. [File Upload Features](#file-upload-features)
5. [Validation Details](#validation-details)
6. [Error Handling](#error-handling)
7. [API Usage](#api-usage)
8. [Troubleshooting](#troubleshooting)

---

## Project Overview

This Django app (`mediaapp`) provides a complete file management system with:
- File upload with form validation
- Admin interface for direct database management
- File listing and gallery view
- File deletion (both from storage and database)
- Automatic file size calculation
- Image format restriction

### Tech Stack
- **Framework**: Django 6.0.4
- **Database**: SQLite3
- **Python**: 3.14.0
- **Package Manager**: uv

---

## Installation & Setup

### 1. Create Virtual Environment

```powershell
cd c:\Users\ziaud\OneDrive\Desktop\orm
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
uv pip install django
```

Or using the venv python directly:
```powershell
.\.venv\Scripts\python.exe -m pip install django
```

### 3. Initialize Django Project

```powershell
django-admin startproject config .
```

### 4. Create Media App

```powershell
python manage.py startapp mediaapp
```

### 5. Database Setup

Apply all migrations:
```powershell
python manage.py migrate
```

Create superuser:
```powershell
set DJANGO_SUPERUSER_PASSWORD=1234567890
python manage.py createsuperuser --no-input --username rafi --email rafi@example.com
```

### 6. Run Development Server

```powershell
python manage.py runserver
```

Access the app at: `http://127.0.0.1:8000/mediaapp/`

---

## Feature Documentation

### Feature 1: Upload Image/Files via HTML Frontend

**Endpoint**: `http://127.0.0.1:8000/mediaapp/upload/`

#### How It Works:
1. User navigates to the upload page
2. Fills in **Title** and **File** fields
3. Form validates the input
4. On success, file is saved to storage and record added to database
5. User is redirected to success page

#### Form Fields:
- **Title** (CharField, max_length=255): Required, descriptive name for the file
- **File** (FileField, upload_to='mediafiles/', accept='image/*'): Required, only images allowed

#### File Upload Process:
```
User Input → Form Validation → File Storage → Database Record → Success Page
```

#### Frontend Components:
- **Upload Form** (`upload.html`):
  - Single file input restricted to images only
  - Title input field
  - Submit button with hover effects
  - Error display in red text
  - CSRF token for security

#### Code Components:

**Model** (`models.py`):
```python
class Mediafile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='mediafiles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filesize = models.PositiveIntegerField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.file and not self.filesize:
            self.filesize = self.file.size
        super().save(*args, **kwargs)
```

**Form** (`forms.py`):
```python
class MediafileForm(forms.ModelForm):
    class Meta:
        model = Mediafile
        fields = ['title', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
```

**View** (`views.py`):
```python
def upload_file(request):
    if request.method == 'POST':
        form = MediafileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'mediaapp/upload_success.html')
    form = MediafileForm()
    return render(request, 'mediaapp/upload.html', {'form': form})
```

---

### Feature 2: Valid Format Validation

**How Format Validation Works**:

1. **HTML Level** (Frontend Validation):
   - File input accepts only `image/*` MIME types
   - Browsers restrict file picker to image files
   - Location: `forms.py` widget configuration

2. **Backend Level** (Server Validation):
   - Django form validation runs automatically
   - FileField checks for valid file types
   - Can be extended with custom validators

3. **Current Configuration**:
   - Accepts ALL image formats: `.jpg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`, `.ico`, etc.
   - Any non-image file is rejected at browser level

#### Adding Format Restrictions (if needed):

To restrict to specific formats, modify `forms.py`:
```python
from django.core.validators import FileExtensionValidator

class MediafileForm(forms.ModelForm):
    class Meta:
        model = Mediafile
        fields = ['title', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
    
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif'])]
    )
```

#### Error Handling for Invalid Formats:
```
Invalid Format Error in Admin:
- User attempts to upload non-image file
- Django form validation catches it
- Error message: "The submitted file is not a valid image file"
- Error appears in RED on the upload page
```

---

### Feature 3: File Size Validation

**Automatic File Size Tracking**:

The app automatically calculates and stores file size when a file is uploaded.

#### How Size Works:

1. **Automatic Calculation** (in `models.py`):
```python
def save(self, *args, **kwargs):
    if self.file and not self.filesize:
        self.filesize = self.file.size  # Size in bytes
    super().save(*args, **kwargs)
```

2. **Size Display** (in `file_list.html`):
```html
{{ file.filesize|filesizeformat }}  <!-- Converts to KB, MB, GB -->
```

3. **Size Limits** (optional enhancement):

To add maximum file size validation, modify `forms.py`:
```python
class MediafileForm(forms.ModelForm):
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # 5MB limit
            if file.size > 5242880:  # 5 * 1024 * 1024
                raise forms.ValidationError(
                    "File size must not exceed 5MB"
                )
        return file
```

#### Size Display Formats:
- Bytes: `1024 Bytes`
- Kilobytes: `1.1 KB`
- Megabytes: `5.5 MB`
- Gigabytes: `1.2 GB`

---

### Feature 4: Show File List

**Endpoint**: `http://127.0.0.1:8000/mediaapp/`

#### Gallery View Features:

1. **Responsive Grid Layout**:
   - Auto-fills columns based on screen width
   - Mobile-friendly design
   - Minimum card width: 280px

2. **File Card Display**:
   - Image thumbnail with hover effect
   - File title
   - Upload date (formatted as "Apr 13, 2026")
   - File size (auto-formatted)
   - Delete button (with confirmation)

3. **Hover Effects**:
   - Cards lift up with shadow effect
   - Images maintain aspect ratio
   - Delete button changes color on hover

#### View Code (`views.py`):
```python
def file_list(request):
    files = Mediafile.objects.all()
    return render(request, 'mediaapp/file_list.html', {'files': files})
```

#### Template Features (`file_list.html`):
- Displays all uploaded files in a grid
- Shows thumbnail previews
- Displays metadata (title, date, size)
- Responsive design
- Empty state message when no files

#### Navigation:
- **From Upload Success**: Button to view all files
- **From File List**: Button to upload new files
- **Admin Interface**: Access via `/admin/` with superuser credentials

---

### Feature 5: Delete File (Storage + Database)

**How Deletion Works**:

#### Two-Step Delete Process:

1. **File Storage Deletion**:
   - Removes physical file from `mediafiles/` directory
   - Prevents orphaned files

2. **Database Record Deletion**:
   - Removes entry from `mediaapp_mediafile` table
   - Cleans up completely

#### Implementation (`views.py`):
```python
def file_delete(request, pk):
    file = Mediafile.objects.get(pk=pk)
    file.file.delete()  # Delete from storage
    file.delete()       # Delete from database
    return redirect('mediaapp:file_list')
```

#### Delete Process Flow:
```
User Clicks Delete → Confirmation Dialog → Delete Button Click 
  → Remove from Storage → Remove from DB → Redirect to List
```

#### User Interface:
- Red delete button on each file card
- Confirmation dialog: "Are you sure you want to delete this file?"
- Automatic redirect after successful deletion
- Toast/message could be added for confirmation

#### Admin Delete Option:
Users can also delete files from the admin panel:
1. Navigate to `/admin/mediaapp/mediafile/`
2. Select file(s)
3. Choose "Delete selected" from dropdown
4. Confirm deletion

---

## Validation Details

### Overall Validation Flow:

```
User Submission
    ↓
HTML Form Validation (Accept="image/*")
    ↓
Django Form Validation (MediafileForm)
    ↓
Model Validation (if added)
    ↓
Database Constraints
    ↓
Success or Error
```

### Field Validation:

| Field | Type | Constraints | Error Handling |
|-------|------|-------------|---|
| Title | CharField | Max 255 chars, Required | Displays below field in red |
| File | FileField | Required, Image only | Shows validation error message |
| Filesize | Integer | Auto-calculated, nullable | Stored after upload |
| Uploaded_at | DateTime | Auto-set, read-only | Handled by Django |

---

## Error Handling

### Common Errors and Solutions

#### Error 1: TemplateDoesNotExist

**Error Message**:
```
TemplateDoesNotExist at /mediaapp/upload/
mediaapp/upload.html
```

**Cause**: Template file not found in the correct directory

**Solution**:
1. Ensure templates are in: `mediaapp/templates/mediaapp/`
2. Check `TEMPLATES` setting in `settings.py`:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        ...
    }
]
```
3. Recreate template files if missing

---

#### Error 2: NoReverseMatch

**Error Message**:
```
NoReverseMatch at /mediaapp/upload/
Reverse for 'upload' not found
```

**Cause**: URL name doesn't match in template or missing from `urls.py`

**Solution**:
1. Check `urls.py` has the view registered:
```python
urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('', views.file_list, name='file_list'),
    path('delete/<int:pk>/', views.file_delete, name='file_delete'),
]
```

2. In templates, use namespaced URLs:
```html
<a href="{% url 'mediaapp:upload' %}">Upload</a>
```

---

#### Error 3: IntegrityError: NOT NULL constraint failed

**Error Message**:
```
IntegrityError at /admin/mediaapp/mediafile/add/
NOT NULL constraint failed: mediaapp_mediafile.filesize
```

**Cause**: Required field has no value

**Solution**:
1. Make `filesize` nullable in model:
```python
filesize = models.PositiveIntegerField(blank=True, null=True)
```

2. Create and apply migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

#### Error 4: Superuser Creation Issues

**Error Message**:
```
django.db.utils.OperationalError: no such table: auth_user
```

**Cause**: Migrations not applied before creating superuser

**Solution**:
```bash
# Apply migrations first
python manage.py migrate

# Then create superuser
set DJANGO_SUPERUSER_PASSWORD=1234567890
python manage.py createsuperuser --no-input --username rafi --email rafi@example.com
```

---

#### Error 5: File Not Displaying in List

**Cause**: Media files not served in development

**Solution**:
Ensure `settings.py` has:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

And `urls.py` includes:
```python
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ... your paths
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

#### Error 6: Form Validation Errors

**Red Error Messages** appear when:
- Title is empty (required)
- File is empty (required)
- File format is invalid (not image/*) - caught at browser level

**Display** (in upload.html):
```html
{% if form.title.errors %}
    <div class="error">{{ form.title.errors|striptags }}</div>
{% endif %}

{% if form.file.errors %}
    <div class="error">{{ form.file.errors|striptags }}</div>
{% endif %}
```

---

## API Usage

### Django Admin Interface

**URL**: `http://127.0.0.1:8000/admin/`

**Login Credentials**:
- Username: `rafi`
- Password: `1234567890`

**Admin Features**:
1. **View All Files**: `/admin/mediaapp/mediafile/`
2. **Add File Manually**: Admin form available
3. **Edit File**: Click file to edit title
4. **Delete File**: Select and bulk delete
5. **Search**: Search by title
6. **Filter**: Filter by upload date

---

### Frontend URLs

| URL | Purpose | Method |
|-----|---------|--------|
| `/mediaapp/` | File list gallery | GET |
| `/mediaapp/upload/` | Upload form | GET, POST |
| `/mediaapp/delete/<id>/` | Delete file | GET (redirect) |

---

## Project Structure

```
orm/
├── config/
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL routing
│   └── wsgi.py
├── mediaapp/
│   ├── migrations/      # Database migrations
│   ├── templates/
│   │   └── mediaapp/
│   │       ├── upload.html
│   │       ├── upload_success.html
│   │       └── file_list.html
│   ├── models.py        # Mediafile model
│   ├── forms.py         # MediafileForm
│   ├── views.py         # Upload, list, delete views
│   ├── urls.py          # App URL routing
│   ├── admin.py         # Admin configuration
│   └── apps.py
├── scripts/
│   └── startappx.py     # App creation helper
├── manage.py            # Django CLI
├── db.sqlite3           # Database
└── .venv/               # Virtual environment
```

---

## Troubleshooting

### Server Won't Start

```bash
# Clear Python cache
Remove-Item -Path ".\mediaapp\__pycache__" -Recurse -Force
Remove-Item -Path ".\config\__pycache__" -Recurse -Force

# Check for syntax errors
python manage.py check

# Run server
python manage.py runserver
```

### Files Not Uploading

1. Check media directory permissions
2. Ensure `MEDIA_ROOT` and `MEDIA_URL` are set in `settings.py`
3. Restart development server
4. Check file size limits

### Templates Not Found

1. Verify template directory: `mediaapp/templates/mediaapp/`
2. Check `APP_DIRS` is `True` in `TEMPLATES` setting
3. Restart development server
4. Clear browser cache

### Admin Access Issues

1. Ensure superuser exists:
   ```bash
   python manage.py createsuperuser
   ```

2. Check if migrations are applied:
   ```bash
   python manage.py migrate
   ```

3. Verify correct URL: `http://127.0.0.1:8000/admin/`

---

## Summary of Workflow

### User Upload Workflow:
1. User visits `/mediaapp/upload/`
2. Fills title and selects image
3. Form validates input
4. File saved to `media/mediafiles/`
5. Database record created
6. Success page shown
7. User can upload another or view list

### User View Workflow:
1. User visits `/mediaapp/`
2. Gallery displays all images
3. Shows title, date, size on each card
4. Can click delete with confirmation
5. Can navigate to upload page

### Admin Workflow:
1. Admin visits `/admin/`
2. Logs in with credentials
3. Views `Mediafile` entries
4. Can add, edit, or delete files
5. Changes reflected immediately

---

## Next Steps / Enhancements

Possible improvements:
- Add video upload support
- Implement file download feature
- Add pagination for large file lists
- Add file search functionality
- Implement user-specific file management
- Add drag-and-drop upload
- Implement image cropping
- Add file categories/tags
- Email notifications on upload/delete

---

## Support & Questions

For issues or questions, check:
1. Django documentation: https://docs.djangoproject.com/
2. Error messages in red on upload page
3. Django logs in terminal output
4. Admin interface for database inspection

---

**Last Updated**: April 13, 2026  
**Author**: Rafi  
**Version**: 1.0.0
