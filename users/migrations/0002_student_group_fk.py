import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='specialty',
        ),
        # Текстовое поле group нельзя «преобразовать» в ForeignKey,
        # поэтому удаляем его и добавляем новое поле-связь.
        migrations.RemoveField(
            model_name='student',
            name='group',
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='students', to='academics.group', verbose_name='Группа'),
        ),
    ]
