from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from .forms import AddReviewForm, ReviewForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Books, Review
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import BookForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


class BookListView(View):
    def get(self, request):
        book = Books.objects.all().order_by('-id')
        context = {
            'book': book
        }
        return render(request, 'book_list.html', context=context)


# class BookDetailView(View):
#     def get(self, request, pk):
#         book = Books.objects.get(pk)
#         reviews = Review.objects.filter(book=pk)
#         context = {
#             'book': book,
#             'reviews': reviews
#         }
#         return render(request, 'book_detail.html', context=context)

@method_decorator(login_required, name='dispatch')
class BookDetailView(View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        reviews = Review.objects.filter(book=book)
        user_has_reviewed = reviews.filter(user=request.user).exists()

        context = {
            'book': book,
            'reviews': reviews,
            'current_user': request.user,
            'user_has_reviewed': user_has_reviewed
        }
        return render(request, 'book_detail.html', context=context)


class BookUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(instance=book)
        context = {
            'form': form
        }
        return render(request, 'update.html', context=context)

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('products:book_update', pk=book.pk)
        else:
            context = {
                'form': form
            }
            return render(request, 'update.html', context=context)


class BookCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = BookForm()
        context = {
            'form': form
        }
        return render(request, 'book_create.html', context=context)

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.save()
            return redirect('products:book_list')
        else:
            return render(request, 'book_create.html', {'form': form})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Books
    template_name = 'book_delete.html'
    success_url = reverse_lazy('products:book_list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        book = get_object_or_404(Books, pk=pk)
        if book.user != self.request.user:
            messages.error(self.request, 'У вас недостаточно прав для удаления этой книги!')
            return redirect('products:book_list')
        return book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete book'
        return context

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        messages.success(self.request, 'Книга была успешна удалена.')
        return redirect(self.success_url)


class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'book': book,
            'add_review_form': add_review_form
        }
        return render(request, 'add_review.html', context=context)

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = add_review_form.save(commit=False)
            review.user = book
            review.save()
            messages.success(request, "Книга успешно добавлено!")
            return redirect('products:book_detail', pk=pk)
        else:
            messages.error(request, 'Что-то преизошло не так, пожалуйста, повторите попытку.')
            context = {
                'book': book,
                'add_review_form': add_review_form
            }
            return render(request, 'add_review.html', context=context)


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        is_author = review.user == request.user
        return render(request, 'delete_review.html',{'review': review, 'is_author': is_author})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user:
            messages.error(request, 'У вас нет прав удалить этот отзыв.')
            return redirect('product:book_detail', pk=review.book_id)

        review.delete()
        messages.success(request, 'Отзыв успешно удален.')
        return redirect('products:book_detail', pk=review.book_id)


# class DeleteReviewView(LoginRequiredMixin, DeleteView):
#     model = Review
#     template_name = 'delete_review.html'
#
#     def get_object(self, queryset=None):
#         review = super().get_object(queryset)
#         if review.user != self.request.user:
#             messages.error(self.request, 'У вас нет прав удалить этот отзыв.')
#             return None
#         return review
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_author'] = self.get_object() is not None
#         return context
#
#     def delete(self, request, *args, **kwargs):
#         review = self.get_object()
#         if review is None:
#             return redirect('products:book_detail', pk=self.kwargs['pk'])
#         messages.success(request, 'Отзыв успешно удален.')
#         return super().delete(request, *args, **kwargs)
#
#     def get_success_url(self):
#         review = self.object
#         return reverse_lazy('products:book_detail', kwargs={'pk': review.book_id})


class UpdateReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(instance=review)
        context = {
            'form': form,
            'review': review
        }
        return render(request, 'update_review.html', context=context)

    def post(self, request,pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлён.')
            return redirect('products:book_detail', pk=review.book_id)
        else:
            messages.error(request, 'Ошибка обновления формы. Пожалуста, проверьте форму')













