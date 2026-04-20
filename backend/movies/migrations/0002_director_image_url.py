from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
