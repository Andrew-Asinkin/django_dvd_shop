from django.urls import path
from django.conf.urls import url

from shop import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delivery", views.delivery, name="delivery"),
    path("contacts", views.contacts, name="contacts"),
    # url(r"^section/(?P<pk>\d+)$", views.Sections.as_view(), name="section"),
    path("section/<slug:slug>", views.Sections.as_view(), name="section"),
    # url(r"^product/(?P<pk>\d+)$", views.ProductDetailView.as_view(), name="product"),
    path("product/<slug:slug>", views.ProductDetailView.as_view(), name="product"),
    path("search", views.search, name="search"),
    path("cart", views.cart, name="cart"),
    path("order", views.order, name="order"),
    path("addorder", views.addorder, name="addorder"),
    path("orders", views.orders, name="orders"),
    url(r"^cancelorder/(?P<pk>\d+)$", views.cancelorder, name="cancelorder"),
]

# < a href = "{% url 'section' section.pk %}" > {{product.section.title}} < / a >