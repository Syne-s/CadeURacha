# Generated by Django 5.1.3 on 2025-02-22 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_synes', '0029_alter_arena_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arena',
            options={'ordering': ['-data_cadastro'], 'permissions': [('can_add_arena', 'Can add new arena on map')], 'verbose_name': 'Quadra', 'verbose_name_plural': 'Quadras'},
        ),
    ]
