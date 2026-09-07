import os
import sys


def main():
    import http.server
    http.server.BaseHTTPRequestHandler.version_string = lambda self: "Webserver"
    
    try:
        import django.core.servers.basehttp
        django.core.servers.basehttp.ServerHandler.server_software = "Webserver"
    except ImportError:
        pass

    try:
        import django.views.static
        _original_serve = django.views.static.serve
        def secure_serve(request, path, document_root=None, show_indexes=False):
            response = _original_serve(request, path, document_root, show_indexes)
            response["X-Content-Type-Options"] = "nosniff"
            # Also add Content-Security-Policy to static files to make it even more secure!
            response["Content-Security-Policy"] = "default-src 'self'"
            return response
        django.views.static.serve = secure_serve
    except ImportError:
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it is installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
