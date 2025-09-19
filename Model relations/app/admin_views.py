# admin_views.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy.orm import joinedload

from .extensions import db
from .models import User, Order   # adjust the import path to your project layout

# --- Custom Admin Views ------------------------------------------------------

class SecureModelView(ModelView):
    """Restrict access so only logged-in admins can view the admin pages."""
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def inaccessible_callback(self, name, **kwargs):
        from flask import redirect, url_for
        return redirect(url_for("login"))  # replace with your login endpoint


class UserAdmin(SecureModelView):
    # Columns to display in the list view
    column_list = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'phone', 'is_admin', 'create_at', 'updated_at'
    )
    column_searchable_list = ('username', 'email', 'phone')
    column_filters = ('is_admin', 'create_at', 'updated_at')
    column_default_sort = ('create_at', True)   # newest first
    form_excluded_columns = ('password_hash', 'orders')  # don't show hash in forms

    # optional: eager-load orders when listing users
    def get_query(self):
        return super().get_query().options(joinedload(User.orders))


class OrderAdmin(SecureModelView):
    column_list = ('order_id', 'name', 'price', 'user.id')  # show related User
    column_searchable_list = ('name', 'user.username', 'user.email')
    column_filters = ('price', 'user.username')
    column_default_sort = ('order_id', True)

    # Show the user's username in a readable way
    column_labels = dict(user='User (username)')

    # Eager load the related user to reduce N+1 queries
    def get_query(self):
        return super().get_query().options(joinedload(Order.user))


# --- Register the admin site --------------------------------------------------

def init_admin(app):
    """Call this from your application factory or main app to enable the admin UI."""
    admin = Admin(app, name="My App Admin", template_mode="bootstrap4")
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(OrderAdmin(Order, db.session))
    return admin
