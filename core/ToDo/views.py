from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DeleteView ,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from django.urls import reverse_lazy

# Create your views here.



class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"
    ordering = ["completed", "-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["priority_choices"] = Task.PRIORITY_CHOICES
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title","description","priority"]
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin,View):
    def post(self, request, task_id, *args, **kwargs):
        task = get_object_or_404(Task, pk=task_id)

        if "toggle_completed" in request.POST:
            task.completed = not task.completed
            task.save(update_fields=["completed"])

        elif "priority" in request.POST:
            priority = request.POST.get("priority")
            valid_priorities = dict(Task.PRIORITY_CHOICES)

            if priority in valid_priorities:
                task.priority = priority
                task.save(update_fields=["priority"])

        return redirect("task_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


