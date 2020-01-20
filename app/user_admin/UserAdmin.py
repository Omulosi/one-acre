from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from app.models import User

class UserAdmin(sqla.ModelView):

    can_view_details = True  # show a modal dialog with records details
    action_disallowed_list = ['delete', ]

    column_default_sort = ('createdon', True)

    form_widget_args = {
        'id': {
            'readonly': True
        },
        'farms': {
            'readonly': True
        },
        'id': {
            'readonly': True
        },
        'funded_farms': {
            'readonly': True
        },
        'bank_name': {
            'readonly': True
        },
        'bank_account_num': {
            'readonly': True
        },
        'bank_account_name': {
            'readonly': True
        },
        'email': {
            'readonly': True
        },
        'role': {
            'readonly': True
        },

    }

    column_list = [
        'email',
        'bank_name',
        'bank_account_num',
        'bank_account_name',
        'role',
        'admin',
        'confirmed',
        'createdon',
        'farms',
        'funded_farms'
    ]
    form_columns = [
        'email',
        'bank_name',
        'bank_account_num',
        'bank_account_name',
        'role',
        'admin',
        'confirmed',
        'createdon',
        'farms',
        'funded_farms'
    ]
    column_searchable_list = [
        'email',
        'role',
        'confirmed',
        'bank_name',
        'admin'
    ]
    column_filters = [
        'email',
        'bank_name',
        'bank_account_num',
        'bank_account_name',
        'admin',
        'confirmed',
        'createdon',
        'farms',
        'funded_farms',
        filters.FilterLike(User.role, 'Role', options=(('0', 'Funder'), ('1',
                                                                         'Farmner'))),
    ]
    column_editable_list = ['confirmed', 'admin',]

    # column details list
    column_auto_select_related = True

    # custom filter: each filter in the list is a filter operation (equals, not equals, etc)
    # filters with the same name will appear as operations under the same filter
    column_filters = [
        'createdon',
        'email',
        'bank_name',
        'role',
        'admin',
    ]
