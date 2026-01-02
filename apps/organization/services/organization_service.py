from apps.organization.models import Organization

def create_organization(*,name,description):
    organization=Organization.objects.create(name=name,description=description)
    return organization