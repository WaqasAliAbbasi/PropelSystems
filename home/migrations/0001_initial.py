# Generated by Django 2.1.2 on 2018-11-13 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='item_images')),
                ('shipping_weight_grams', models.PositiveIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('altitude_meters', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Queued for Processing'), (2, 'Processing by Warehouse'), (3, 'Queued for Dispatch'), (4, 'Dispatched'), (5, 'Delivered')], default=1)),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)),
                ('time_placed', models.DateTimeField(auto_now_add=True)),
                ('time_dispatched', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Location')),
            ],
            bases=('home.location',),
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Location')),
            ],
            bases=('home.location',),
        ),
        migrations.AddField(
            model_name='distance',
            name='location_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_from', to='home.Location'),
        ),
        migrations.AddField(
            model_name='distance',
            name='location_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_to', to='home.Location'),
        ),
        migrations.AddField(
            model_name='order',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Clinic'),
        ),
        migrations.AddField(
            model_name='item',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Warehouse'),
        ),
        migrations.AddField(
            model_name='clinic',
            name='linked_warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Warehouse'),
        ),
    ]
