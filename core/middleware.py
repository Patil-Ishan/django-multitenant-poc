from django.http import Http404
from easy_tenants.utils import tenant_context
from core.models import Tenant

class TenantResolutionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/media'):
            response = self.get_response(request)
            return response
        
        host = request.get_host().split(':')[0]
        
        try:
            tenant = Tenant.objects.get(domain=host)
            with tenant_context(tenant=tenant):
                response = self.get_response(request)
            return response
        except Tenant.DoesNotExist:
            raise Http404(f"Tenant not found for domain: {host}")
