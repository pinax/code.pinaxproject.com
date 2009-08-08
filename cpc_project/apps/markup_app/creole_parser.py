from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.util import ClassNotFound

from django_markup.bundles.WikiCreole.creole import Parser
from django_markup.bundles.WikiCreole.creole2html import HtmlEmitter
from django_markup.filter import MarkupFilter


class PygmentsHtmlEmitter(HtmlEmitter):
    
    def preformatted_emit(self, node):
        content = node.content
        lines = content.split("\n")
        if lines[0].startswith("#!code"):
            lexer_name = lines[0].split()[1]
            del lines[0]
        else:
            lexer_name = None
        content = "\n".join(lines)
        try:
            lexer = get_lexer_by_name(lexer_name)
        except ClassNotFound:
            lexer = TextLexer()
        return highlight(content, lexer, HtmlFormatter(cssclass="syntax")).strip()


class CreoleMarkupFilter(MarkupFilter):
    title = "Creole (Wiki Syntax)"
    
    def render(self, text, **kwargs):
        return PygmentsHtmlEmitter(Parser(text).parse()).emit()
