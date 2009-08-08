from django import template

from django_markup.markup import formatter

from markup_app.creole_parser import CreoleMarkupFilter


register = template.Library()


formatter.register("creole", CreoleMarkupFilter)
