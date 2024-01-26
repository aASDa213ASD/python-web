from flask import render_template

def render(template: str, **kwargs):
    return render_template(template, **kwargs)