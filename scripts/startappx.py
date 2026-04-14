import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python scripts/startappx.py <app_name>")
    sys.exit(1)

app = sys.argv[1]

# 1. Create app
subprocess.run(
    ["uv", "run", "python", "manage.py", "startapp", app],
    check=True,
)

# 2. Add to INSTALLED_APPS
settings_path = Path("config/settings.py")
settings = settings_path.read_text()

if f"'{app}'" not in settings:
    settings = settings.replace(
        "INSTALLED_APPS = [",
        f"INSTALLED_APPS = [\n    '{app}',"
    )
    settings_path.write_text(settings)

# 3. Create app urls.py (only if missing)
app_urls = Path(app) / "urls.py"
if not app_urls.exists():
    app_urls.write_text(
        "from django.urls import path\n\n"
        f"app_name = '{app}'\n\n"
        "urlpatterns = []\n"
    )

# 4. Wire URLs safely
main_urls_path = Path("config/urls.py")
main_urls = main_urls_path.read_text()

# 4a. Ensure include is imported (explicit & idempotent)
if "from django.urls import path, include" not in main_urls:
    if "from django.urls import path" in main_urls:
        main_urls = main_urls.replace(
            "from django.urls import path",
            "from django.urls import path, include",
        )
    else:
        main_urls = "from django.urls import path, include\n" + main_urls

# 4b. Ensure app url include exists
include_line = f"    path('{app}/', include('{app}.urls')),\n"

if include_line not in main_urls:
    main_urls = main_urls.replace(
        "urlpatterns = [\n",
        f"urlpatterns = [\n{include_line}"
    )

main_urls_path.write_text(main_urls)

print(f"App '{app}' created and wired successfully")

