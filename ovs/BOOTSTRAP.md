# Developer information for Bootstrap
In order to make your page work with bootstrap all you have to do is extend
`base.html`. Like this:
```html+jinja
{% extends "base.html" %}
{% block title %}Title{% endblock %}
{% block head %}Optional. Put any additional header tags here{% endblock %}

{% block content %}
    Page content goes here (you can use bootstrap)
{% endblock %}
```

The navbar is defined in `base.html` and uses an if-elif-else chain on role to
determine which bar to use. When rendering your page do so like this:
```python
@route()
def page():
    role = UserService.get_user_by_id(current_user.get_id()).first().role
    return render_template('my_page.html', role=role)
```
You should also pass in whatever other fields are required. For instance if the
role is RESIDENT a profile is required to display their preferred name.
