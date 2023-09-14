from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Полное описание')),
                ('rules', models.TextField(blank=True, null=True, verbose_name='Правила игры')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/game/', verbose_name='Изображение')),
                ('exist', models.BooleanField(default=True, verbose_name='Наличие')),
            ],
            options={
                'verbose_name': 'Игру',
                'verbose_name_plural': 'Игры',
                'ordering': ['title', 'id'],
            },
        ),
    ]
