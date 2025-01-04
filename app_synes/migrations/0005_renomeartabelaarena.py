from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('app_synes', '0004_excluirtabelaarena'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NovaArena',
            new_name='Arena',
        ),
    ]