# Generated by Django 4.2.7 on 2023-11-10 11:49

from django.db import migrations, models


def create_required_operations(apps, schema_editor):
    Operator = apps.get_model("calculator", "Operator")
    Operator.objects.bulk_create([Operator(operator=op) for op in ("*", "/", "+", "-")])


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Operator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        choices=[
                            ("*", "MULTIPLICATION"),
                            ("/", "DIVISION"),
                            ("+", "ADDITION"),
                            ("-", "SUBTRACTION"),
                        ],
                        max_length=1,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="operator",
            constraint=models.CheckConstraint(
                check=models.Q(("operator__in", ["*", "/", "+", "-"])),
                name="operator_valid",
            ),
        ),
        migrations.RunPython(create_required_operations, migrations.RunPython.noop),
    ]
