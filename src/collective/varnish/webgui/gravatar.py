from jinja2 import nodes
from jinja2.ext import Extension


#class FragmentGravatarExtension(Extension):
#    """ """
#    tags = set(['gravatar'])
#
#    def __init__(self, environment):
#        super(FragmentGravatarExtension, self).__init__(environment)
#
#        # add the defaults to the environment
#        environment.extend(
#            email_gravatar='00000000000000000000000000000000',
#            gravatar_size=27
#        )
#
#    def parse(self, parser):
#        lineno = parser.stream.next().lineno
#
#        # now we parse a single expression that is used as cache key.
#        args = [parser.parse_expression()]
#
#        if parser.stream.skip_if('comma'):
#            args.append(parser.parse_expression())
#        else:
#            args.append(nodes.Const(None))
#
#        body = parser.parse_statements(['name:endgravatar'], drop_needle=True)
#
#        return nodes.CallBlock(self.call_method('_gravatar_support', args),
#                               [], [], body).set_lineno(lineno)
#
#    def _gravatar_support(self, email, size, caller):
#        gv = caller()
#        return 'FUNCIONA'
#
#gravatar = FragmentGravatarExtension


class FragmentGravatarExtension(Extension):

        tags = set(['gravatar'])

        def parse(self, parser):
            lineno = parser.stream.next().lineno
            args = [parser.parse_expression()]
            args.append(nodes.Const(args[0].name))
            return nodes.CallBlock(
                self.call_method('_render', args),
                [], [], []).set_lineno(lineno)

        def _render(self, value, name, *args, **kwargs):
            if some_condition():
                return '<gravatar id="%s">%s</gravatar>' % (name, value)
            return value
