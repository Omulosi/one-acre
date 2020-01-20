from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from app.models import Farm

class FarmAdmin(sqla.ModelView):
    can_export = True
    export_max_rows = 1000
    export_types = ['csv', 'xls']

    form_widget_args = {
        'id': {
            'readonly': True
        },
        'person': {
            'readonly': True
        }
    }
    column_searchable_list = [
        'name',
        'stage',
        'location',
        'active',
    ]

    column_default_sort = ('createdon', True)

    column_filters = [
        'name',
        'stage',
        'location',
        'active',
        'duration',
        'units',
        'margin',
        'price',
        'active',
        'farmer'
    ]
