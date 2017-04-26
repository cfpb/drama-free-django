from no_drama.template import get_template


def render_with_args(template_name, args):
    template = get_template(template_name)
    return template.render(args=args) + '\n'


def build(args):
    script = "#!%s\n" % args.python

    bootstrap_template_name = "bootstrap_%s.py.j2" % args.environment_type

    script += render_with_args(bootstrap_template_name, args)

    if args.vars:
        script += render_with_args('env_json.py.j2', args)

    if args.paths:
        script += "\n# extend sys.path\nimport sys" + "\n"
        script += "sys.path = %s + sys.path\n" % repr(args.paths)

    runner_template_name = '%s.py.j2' % args.type
    script += render_with_args(runner_template_name, args)

    args.output.write(script)
