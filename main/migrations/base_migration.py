from django.contrib.auth.hashers import make_password
from django.db import migrations

def groups_apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Administrators'),
        Group(name=u'Staff'),
        Group(name=u'Users'),
    ])

def groups_revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            u'Administrators',
            u'Staff',
            u'Users',
        ]
    ).delete()

def create_administrator(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User(
        username='Admin'.lower(),
        email='admin@niejestessam.pl',
        password=make_password('Helpdesk.123'),
         first_name="Administrator",
        last_name="systemu",
        is_superuser=False,
        is_staff=False,
    )
    user.save()

    Group = apps.get_model('auth', 'Group')
    group = Group.objects.get(name='Administrators')
    user.groups.add(group)

def create_staff_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User(
        username='Staff'.lower(),
        email='staff@niejestessam.pl',
        password=make_password('Helpdesk.123'),
         first_name="Pracownik",
        last_name="systemu",
        is_superuser=False,
        is_staff=False,
    )
    user.save()

    Group = apps.get_model('auth', 'Group')
    group = Group.objects.get(name='Staff')
    user.groups.add(group)

def create_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User(
        username='User'.lower(),
        email='user@niejestessam.pl',
        password=make_password('Helpdesk.123'),
         first_name="Użytkownik",
        last_name="systemu",
        is_superuser=False,
        is_staff=False,
    )
    user.save()

    Group = apps.get_model('auth', 'Group')
    group = Group.objects.get(name='Users')
    user.groups.add(group)

class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(groups_apply_migration, groups_revert_migration),
        migrations.RunPython(create_administrator),
        migrations.RunPython(create_staff_user),
        migrations.RunPython(create_user),
    ]