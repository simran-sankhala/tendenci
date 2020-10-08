# Generated by Django 2.2.16 on 2020-10-07 16:53
import os
from django.db import migrations


def migrate_categories_for_templates():
    """
    Migrate categories for templates pulled down to the site.
    
    directories/meta.html
    ============================================
    Replace:
    {% with directory.cat as directory_cat %}
        {% if directory_cat %}
            <li>
                <ul class="list-inline">
                    <li><strong>{% trans "Category:" %}</strong> <a href="{% url 'directories' %}?cat={{ directory_cat.pk }}">{{ directory_cat.name }}</a></li>
                    {% if directory.sub_cat %}
                        <li>|</li>
                        <li><strong>{% trans "Subcategory:" %}</strong> <a href="{% url 'directories' %}?cat={{ directory_cat.pk }}&sub_cat={{ directory.sub_cat.pk }}">{{ directory.sub_cat.name }}</a></li>
                    {% endif %}
                </ul>
            </li>
        {% endif %}
    {% endwith %}

    with:
    {% with directory.cats.all as directory_cats %}
        {% if directory_cats %}
            <li>
                <ul class="list-inline">
                    <li><strong>{% trans "Category:" %}</strong> 
                       {% for cat in directory_cats %}
                       <a href="{% url 'directories' %}?cat={{ cat.pk }}">{{ cat.name }}</a>{% if not forloop.last %}, {% endif %}
                       {% endfor %}
                     </li>
                     {% with directory.sub_cats.all as directory_sub_cats %}
                     {% if directory_sub_cats %}
                        <li>|</li>
                        <li><strong>{% trans "Subcategory:" %}</strong> 
                           {% for sub_cat in directory_sub_cats %}
                           <a href="{% url 'directories' %}?sub_cat={{ sub_cat.pk }}">{{ sub_cat.name }}</a>{% if not forloop.last %}, {% endif %}
                           {% endfor %}
                        </li>
                    {% endif %}
                    {% endwith %}
                </ul>
            </li>
        {% endif %}
    {% endwith %}
    
    """
    import re
    from tendenci.apps.theme.utils import get_theme_root
    dir_path = get_theme_root()
    file_path = '{}/templates/directories/meta.html'.format(dir_path)
    replace_with = """
    {% with directory.cats.all as directory_cats %}
        {% if directory_cats %}
            <li>
                <ul class="list-inline">
                    <li><strong>{% trans "Category:" %}</strong> 
                       {% for cat in directory_cats %}
                       <a href="{% url 'directories' %}?cat={{ cat.pk }}">{{ cat.name }}</a>{% if not forloop.last %}, {% endif %}
                       {% endfor %}
                     </li>
                     {% with directory.sub_cats.all as directory_sub_cats %}
                     {% if directory_sub_cats %}
                        <li>|</li>
                        <li><strong>{% trans "Subcategory:" %}</strong> 
                           {% for sub_cat in directory_sub_cats %}
                           <a href="{% url 'directories' %}?sub_cat={{ sub_cat.pk }}">{{ sub_cat.name }}</a>{% if not forloop.last %}, {% endif %}
                           {% endfor %}
                        </li>
                    {% endif %}
                    {% endwith %}
                </ul>
            </li>
        {% endif %}
    {% endwith %}
    """
    p = r'\{% with directory.cat as directory_cat %\}[\d\D\s\S\w\W]*?\{% endwith %\}'
    if os.path.isfile(file_path):
        print('Updating categories for file directories/meta.html' )
        with open(file_path, 'r') as f:
            content = f.read()
    
            content = re.sub(p, replace_with, content)
            
        with open(file_path, 'w') as f:
            f.write(content)


def cat_to_cats(apps, schema_editor):
    """
        Migrate data from cat and sub_cat to cats and sub_cats, respectively.
        (from ForeignKey to ManyToManyField)
    """
    Directory = apps.get_model('directories', 'Directory')
 
    for directory in Directory.objects.all():
        if directory.cat:
            directory.cats.add(directory.cat)
        if directory.sub_cat:
            directory.sub_cats.add(directory.sub_cat)

    # migrate templates pulled down to the site
    migrate_categories_for_templates()


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0014_auto_20201007_1622'),
    ]

    operations = [
        migrations.RunPython(cat_to_cats),
    ]
