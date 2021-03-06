from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.detail import DetailView
from .models import Language, Lesson, Unit, Content, Profile
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from students.forms import StudentEnrollment
from .forms import UnitFormSet, InstructorLoginForm
from django.forms.models import modelform_factory
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.core.cache import cache
from .forms import InstructorRegistrationForm, UserProfileForm, UserForm
from django.contrib import messages


# Create your views here.
class LessonListView(TemplateResponseMixin, View):
    """View for the list of lessons"""
    model = Lesson
    template_name = 'lessons/list_lessons.html'

    def get(self, request, language=None):
        """ Execute get requests"""

        # Get data from the cache data
        languages = cache.get('all_languages')
        # Do calculations when data are not in the cached data
        if not languages:
            languages = Language.objects.annotate(total_lessons=Count('lessons'))
            cache.set('all_languages', languages)

        all_lessons = Lesson.objects.annotate(total_units=Count('units'))

        #  Build key dynamically using language id
        if language:
            language = get_object_or_404(Language, slug=language)
            key = f'language_{language.id}_lessons'
            lessons = cache.get(key)
            # Do calculations when data are not in the cached data
            if not lessons:
                lessons = all_lessons.filter(language=language)
                cache.set(key, lessons)
        # Use all_lessons cache key to store all lessons
        else:
            lessons = cache.get('all_lessons')
            if not lessons:
                lessons = all_lessons
                cache.get('all_lessons', lessons)

        return self.render_to_response({'languages': languages,
                                        'language': language,
                                        'lessons': lessons})


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
    fields = ['language', 'title', 'slug', 'outline']
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
    """Returns HttpResponse"""
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Instructors').exists() and \
                request.user.groups.filter(name='Students').exists() or \
                request.user.groups.filter(name='Instructors').exists():
            return HttpResponseRedirect(reverse_lazy('lessons_list'))
        else:
            return HttpResponseRedirect(reverse_lazy('student_lesson_list'))

    return render(request, 'homepage.html')


class LessonDetailView(DetailView):
    """ View for lesson details"""
    model = Lesson
    template_name = 'lessons/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = StudentEnrollment(initial={'lesson': self.object})

        return context


class UnitOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """ Allows the user to reorder lesson units """

    def post(self, request):
        """ Execute post requests"""
        for unit_id, unit_order in self.request_json.items():
            Unit.objects.filter(id=unit_id, lesson_creator=request.user).update(order=unit_order)

        return self.render_json_response({'Done and saved': 'Approved'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """ Allows the user to reorder lesson contents """

    def post(self, request):
        """ Execute post requests"""
        for content_id, content_order in self.request_json.items():
            Content.objects.filter(id=content_id, lesson_creator=request.user).update(order=content_order)

        return self.render_json_response({'Done and saved': 'Approved'})


class UpdateLessonUnitView(TemplateResponseMixin, View):
    """ Takes care of handling formsets for updating, deleting and adding units"""
    Lesson = None
    template_name = 'languages/management/unit/formset.html'

    def get_formset(self, data=None):
        """ To avoid repeating the same process for the formsets"""
        return UnitFormSet(instance=self.lesson, data=data)

    def dispatch(self, request, pk):
        """ Takes an HTTP request and redirects to a method that matches the HTTP method used"""
        self.lesson = get_object_or_404(Lesson, id=pk, creator=request.user)

        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        """ Execute get requests"""
        formset = self.get_formset()

        return self.render_to_response({'lesson': self.lesson,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        """ Execute post requests"""
        formset = self.get_formset(data=request.POST)
        # Validate all forms
        if formset.is_valid():
            formset.save()
            return redirect('lessons_list')

        return self.render_to_response({'lesson': self.lesson,
                                        'formset': formset})


class CreateContentView(TemplateResponseMixin, View):
    """ Helps creating and updating lesson contents"""
    model = None
    unit = None
    object_to_create = None
    template_name = 'languages/management/content/form.html'

    def get_model(self, model_name):
        """returns actual model class """
        content_type = ['text', 'image', 'video', 'file']
        if model_name in content_type:
            return apps.get_model(app_label='languages', model_name=model_name)

        return None

    def get_form(self, model, *args, **kwargs):
        """Returns model form"""
        Form = modelform_factory(model, exclude=['order', 'creator', 'created_on', 'updated_on'])

        return Form(*args, **kwargs)

    def dispatch(self, request, unit_id, model_name, id=None):

        self.model = self.get_model(model_name)
        self.unit = get_object_or_404(Unit, id=unit_id, lesson__creator=request.user)

        if id:
            self.object_to_create = get_object_or_404(self.model, id=id, creator=request.user)

        return super().dispatch(request, unit_id, model_name, id)

    def get(self, request, unit_id, model_name, id=None):
        """Execute get requests"""
        return self.render_to_response({'form': self.get_form(self.model, instance=self.object_to_create),
                                        'object': self.object_to_create})

    def post(self, request, unit_id, model_name, id=None):
        """Execute post requests"""
        form = self.get_form(self.model,
                             instance=self.object_to_create,
                             data=request.POST,
                             files=request.FILES)

        # Valid of the forms
        if form.is_valid():
            object_to_create = form.save(commit=False)
            object_to_create.creator = request.user
            object_to_create.save()
            # Create new object if id is not provided
            if not id:
                Content.objects.create(unit=self.unit, item=object_to_create)
                # return redirect('unit_content_list', self.unit.id)

        return self.render_to_response({'form': form,
                                        'object': self.object_to_create})


class DeleteContentView(View):
    """Helps deleting lesson contents"""

    def post(self, request, unit_id):
        """Execute post requests"""
        content = get_object_or_404(Content, id=unit_id,
                                    unit__lesson__creator=request.user)
        unit = content.unit
        content.item.delete()
        content.delete()
        return redirect('unit_content_list', unit.id)


class ContentListView(TemplateResponseMixin, View):
    """ List View for Unit contents """
    template_name = 'languages/management/unit/list.html'

    def get(self, request, unit_id):
        """Execute get requests"""
        unit = get_object_or_404(Unit, id=unit_id, lesson__creator=request.user)
        return self.render_to_response({'unit': unit
                                        })


def instructor_login_view(request):
    """ Login View for Instructors"""

    if request.method == 'POST':
        form = InstructorLoginForm(request.POST)
        if form.is_valid():
            credentials = form.cleaned_data
            user = authenticate(request, password=credentials['password'], username=credentials['username'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Welcome back!")
                    return redirect('lessons_list')
                else:
                    messages.info(request, 'You account has been disabled')
                    return HttpResponse('Disabled account')
            else:
                messages.info(request, 'Your credentials are invalid')
                return HttpResponse('Invalid login')
    else:
        form = InstructorLoginForm()
    return render(request, 'account/login.html', {'form': form})


def instructor_registration(request):
    if request.method == 'POST':

        instructor_form = InstructorRegistrationForm(request.POST)

        if instructor_form.is_valid():
            new_instructor = instructor_form.save(commit=False)
            new_instructor.set_password(instructor_form.cleaned_data['password1'])
            new_instructor.save()
            group = Group.objects.get(name='Instructors')
            # Add new instructor to Instructors group
            new_instructor.groups.add(group)
            # Create Profile for new instructor
            Profile.objects.create(user=new_instructor)

            login(request, new_instructor)
            messages.success(request, 'Welcome! Your account has been successfully created')

            return HttpResponseRedirect(reverse_lazy('lessons_list'))

            # return render(request, 'registration/instructor_registration.html', {'new_student': new_student})
    else:
        instructor_form = InstructorRegistrationForm()
    return render(request, 'registration/instructor_registration.html', {'instructor_form': instructor_form})


def custom_logout_view(request):
    """Custom Log out request"""

    logout(request)
    messages.success(request, 'You have successfully logged out from hiPal')
    return render(request, 'registration/logout.html')


@login_required
def edit_profile(request):
    """View to edit profile"""
    if request.method == 'POST':
        user_form = UserForm(instance=request.user, data=request.POST)
        user_profile_form = UserProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Profile has been successfully updated')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html',
                  {'user_form': user_form, 'user_profile_form': user_profile_form})
