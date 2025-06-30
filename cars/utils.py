menu = [
    {'title': 'About page', 'url_name': 'about'},
    {'title': 'Add a new car', 'url_name': 'add_car'},
    {'title': 'Feedback', 'url_name': 'contact'},
    {'title': 'Log In', 'url_name': 'login'},
]


class DataMixin:
    title_page = None
    extra_context = {}
    country_selected = None

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.country_selected is not None:
            self.extra_context['country_selected'] = self.country_selected

        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context['country_selected'] = None
        context.update(kwargs)
        return context
