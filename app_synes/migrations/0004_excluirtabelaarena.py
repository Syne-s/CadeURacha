from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('app_synes', '0003_novaarena'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Arena',
        ),
    ]