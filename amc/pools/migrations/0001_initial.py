# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 05:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Againpurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AgainpurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaseNum', models.IntegerField()),
                ('againpurchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Againpurchase')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerName', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderTime', models.DateTimeField(auto_now=True)),
                ('receiver', models.CharField(max_length=30)),
                ('receAddress', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('outDemandTimes', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNum', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OutDemand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Order')),
            ],
        ),
        migrations.CreateModel(
            name='OutdemandDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outNum', models.IntegerField()),
                ('outDemand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.OutDemand')),
            ],
        ),
        migrations.CreateModel(
            name='Payable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalAccount', models.FloatField()),
                ('invoiceStatus', models.CharField(max_length=20)),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PayableDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('unitPrice', models.FloatField()),
                ('salsAmount', models.IntegerField()),
                ('totalsales', models.FloatField()),
                ('payable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Payable')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('productSize', models.CharField(max_length=20)),
                ('stock', models.IntegerField()),
                ('safastock', models.IntegerField()),
                ('purchasePrice', models.FloatField()),
                ('saleprice', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('totalAccount', models.FloatField()),
                ('payable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Payable')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDatail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaseNum', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Receivable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalAccount', models.FloatField()),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ReceivableDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('unitPrice', models.FloatField()),
                ('salsAmount', models.IntegerField()),
                ('totalsales', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product')),
                ('receivable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Receivable')),
            ],
        ),
        migrations.CreateModel(
            name='SaleAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('totalAccount', models.FloatField()),
                ('receivable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Receivable')),
            ],
        ),
        migrations.CreateModel(
            name='Stocknotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addTime', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Order')),
            ],
        ),
        migrations.CreateModel(
            name='StocknoticeDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stocknoticeNum', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product')),
                ('stocknotice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Stocknotice')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplierName', models.CharField(max_length=50)),
                ('linkMan', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('productScope', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30)),
                ('realName', models.CharField(max_length=30)),
                ('userPassword', models.CharField(blank=True, max_length=20)),
                ('userDepart', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Userrole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roleName', models.CharField(max_length=30)),
                ('roleDes', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='userRole',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Userrole'),
        ),
        migrations.AddField(
            model_name='stocknotice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.User'),
        ),
        migrations.AddField(
            model_name='receivable',
            name='stocknotice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Stocknotice'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.User'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Supplier'),
        ),
        migrations.AddField(
            model_name='payabledetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product'),
        ),
        migrations.AddField(
            model_name='payable',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Purchase'),
        ),
        migrations.AddField(
            model_name='outdemanddetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product'),
        ),
        migrations.AddField(
            model_name='outdemand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.User'),
        ),
        migrations.AddField(
            model_name='order_detail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.User'),
        ),
        migrations.AddField(
            model_name='againpurchasedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.Product'),
        ),
        migrations.AddField(
            model_name='againpurchase',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pools.User'),
        ),
    ]
