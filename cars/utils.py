menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add a new car', 'url_name': 'add_car'},
    {'title': 'Feedback', 'url_name': 'contact'},
]


class DataMixin:
    title_page = None
    extra_context = {}
    country_selected = None
    paginate_by = 2

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.country_selected is not None:
            self.extra_context['country_selected'] = self.country_selected

    def get_mixin_context(self, context, **kwargs):
        context['country_selected'] = None
        context.update(kwargs)
        return context
