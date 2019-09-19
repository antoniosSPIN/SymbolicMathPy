from flask import Blueprint


class BaseBlueprint(Blueprint):

    """The Flask Blueprint subclass."""

    def route(self, rule, **options):
        """Override the `route` method; add rules with and without slash."""
        def decorator(f):
            new_rule = rule.rstrip('/')
            new_rule_with_slash = '{}/'.format(new_rule)
            super(BaseBlueprint, self).route(new_rule, **options)(f)
            super(BaseBlueprint, self).route(new_rule_with_slash, **options)(f)
            return f
        return decorator
