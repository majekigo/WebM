from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, CategoryForm, TagForm, OrderForm, OrderPositionFormSet
from .models import Product, Category, Tag, Order


#Функции
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def catalog(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 1)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'catalog.html', {'products': products})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


def products_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    products_with_tag = Product.objects.filter(tags=tag)
    return render(request, 'products_by_tag.html', {'products': products_with_tag, 'tag': tag})


def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products_in_category = Product.objects.filter(categories=category)
    return render(request, 'products_by_category.html', {'products': products_in_category, 'category': category})


# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'product_view/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_view/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(categories__in=self.object.categories.all()).exclude(id=self.object.id).distinct()
        category = self.object.categories.first()
        context['category_id'] = category.pk if category else None

        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_view/product_create.html'
    success_url = reverse_lazy('product_list')

    @method_decorator(permission_required('products.add_product'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_view/product_update.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    @method_decorator(permission_required('products.change_product'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_view/product_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')

    @method_decorator(permission_required('products.delete_product'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'category_view/category_list.html'
    context_object_name = 'categories'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Category.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return Category.objects.all()


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_view/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(categories=self.object)
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_view/category_create.html'
    success_url = reverse_lazy('category_list')

    @method_decorator(permission_required('products.add_category'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Tag Views
class TagListView(ListView):
    model = Tag
    template_name = 'tag_view/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Tag.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return Tag.objects.all()


class TagDetailView(DetailView):
    model = Tag
    template_name = 'tag_view/tag_detail.html'
    context_object_name = 'tag'


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag_view/tag_create.html'
    success_url = reverse_lazy('tag_list')

    @method_decorator(permission_required('products.add_tag'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# Order Views
class OrderListView(ListView):
    model = Order
    template_name = 'order_view/order_list.html'
    context_object_name = 'orders'
    paginate_by = 3

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_view/order_detail.html'
    context_object_name = 'order'


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_view/order_create.html'
    success_url = reverse_lazy('order_list')

    @method_decorator(permission_required('products.add_order'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderPositionFormSet(self.request.POST, prefix='order_positions')
        else:
            context['formset'] = OrderPositionFormSet(prefix='order_positions')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(reverse_lazy('order_list'))
        else:
            return redirect(reverse_lazy('create_order'))


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_view/order_update.html'
    form_class = OrderForm
    success_url = reverse_lazy('order_list')

    @method_decorator(permission_required('products.change_order'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderPositionFormSet(
                self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderPositionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order_view/order_delete.html'
    context_object_name = 'order'
    success_url = reverse_lazy('order_list')

    @method_decorator(permission_required('products.delete_order'))
    def dispatch(self, *args, **kwargs):
        order = self.get_object()
        order.is_deleted = True
        order.save()
        return redirect(self.success_url)
