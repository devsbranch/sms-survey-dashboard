from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage

from tralard.models import Beneficiary

class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise

class BeneficiaryOrgListView(LoginRequiredMixin, TemplateView):
    template_name = 'beneficiary/list.html'
    paginate_by = 20
    paginator_class = MyPaginator

    def get_context_data(self):
        context = super(BeneficiaryOrgListView, self).get_context_data()
        beneficiary_objects = Beneficiary.objects.all()
        
        page = self.request.GET.get('page', 1)
        paginator = self.paginator_class(beneficiary_objects, self.paginate_by)
        organizations = paginator.page(page)

        context['title'] = 'Beneficiary List'
        context['beneficiaries'] = organizations
        return context

class BeneficiaryOrgDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'beneficiary/detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(BeneficiaryOrgDetailView, self).get_context_data(**kwargs)

        beneficiary_org_id = self.kwargs.get('pk')
        beneficiary_org_object = Beneficiary.objects.get(id=beneficiary_org_id)
        context['title'] = 'Beneficiary Details'
        context['beneficiaries'] = beneficiary_org_object
        print
        return context
