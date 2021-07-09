from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import DetailView
from .models import Language, Lesson, Unit, Content
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from students.forms import StudentEnrollment
from .forms import UnitFormSet


# Create your views here.
class LessonListView(ListView):
    """View for the list of lessons"""
    model = Lesson
    template_name = 'languages/management/lesson/list_lesson.html'

    def get_queryset(self):
        """Allows to only display or update the lessons created"""
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user)


class CreatorMixin(object):
    def get_queryset(self):
        """Allows to only display or update the lessons created"""
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user)


class EditableCreatorMixin(object):
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CreatorLessonMixin(CreatorMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Lesson
    fields = ['language', 'title', 'slug', 'overview']
    success_url = reverse_lazy('lessons_list')


class EditableCreatorMixinLesson(CreatorLessonMixin, EditableCreatorMixin):
    template_name = 'languages/management/lesson/form.html'


class ManageLessonView(CreatorLessonMixin, ListView):
    template_name = 'languages/management/lesson/list_lesson.html'
    permission_required = 'languages.view_lesson'


class LessonCreateView(EditableCreatorMixinLesson, CreateView):
    permission_required = 'languages.add_lesson'


class LessonUpdateView(EditableCreatorMixinLesson, UpdateView):
    permission_required = 'languages.change_lesson'


class LessonDeleteView(CreatorLessonMixin, DeleteView):
    template_name = 'languages/management/lesson/delete_lesson.html'
    permission_required = 'languages.delete_lesson'


def homepage(request):
    # return HttpResponse("This is my homepage(/)")
    return render(request, 'homepage.html')


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'languages/lesson/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = StudentEnrollment(initial={'lesson': self.object})
        return context


class LessonUnitUpdateView(TemplateResponseMixin, View):
    Lesson = None
    template_name = 'languages/management/unit/formset.html'

    def get_formset(self, data=None):
        return UnitFormSet(instance=self.lesson, data=data)

    def dispatch(self, pk, request):
        self.lesson = get_object_or_404(Lesson, id=pk, creator=request.user)
        return super().dispatch(pk, request)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'lesson': self.lesson,
                                        'formset': self.get_formset()})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('lessons_list')
        return self.render_to_response({'lesson': self.lesson,
                                        'formset': formset})
