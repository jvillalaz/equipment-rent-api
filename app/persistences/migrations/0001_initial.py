from tortoise import migrations
from tortoise.migrations import operations as ops
from tools.application import naive_utcnow
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='CommandType',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=60)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'CommandTypes', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Defines the different types of commands that can be sent to equipment.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='EquipmentStatus',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=60)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'EquipmentStatuses', 'app': 'models', 'pk_attr': 'id', 'table_description': "Stores information about the system's users."},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Location',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=255)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'location', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Equipment',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=60)),
                ('current_status', fields.ForeignKeyField('models.EquipmentStatus', source_field='current_status_id', null=True, db_constraint=True, to_field='id', related_name='equipments', on_delete=OnDelete.CASCADE)),
                ('location', fields.OneToOneField('models.Location', source_field='location_id', null=True, db_constraint=True, to_field='id', related_name='equipment', on_delete=OnDelete.SET_NULL)),
                ('last_heartbeat', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'Equipments', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Stores the equipment available in the system.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Command',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('command_type', fields.ForeignKeyField('models.CommandType', source_field='command_type_id', db_constraint=True, to_field='id', related_name='commands', on_delete=OnDelete.CASCADE)),
                ('equipment', fields.ForeignKeyField('models.Equipment', source_field='equipment_id', db_constraint=True, to_field='id', related_name='commands', on_delete=OnDelete.CASCADE)),
                ('payload', fields.CharField(null=True, max_length=200)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'Commands', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Records commands sent to equipment.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='EquipmentStatusLog',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('status', fields.ForeignKeyField('models.EquipmentStatus', source_field='status_id', db_constraint=True, to_field='id', related_name='status_logs', on_delete=OnDelete.CASCADE)),
                ('equipment', fields.ForeignKeyField('models.Equipment', source_field='equipment_id', db_constraint=True, to_field='id', related_name='status_logs', on_delete=OnDelete.CASCADE)),
                ('details', fields.CharField(null=True, max_length=300)),
                ('reported_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'EquipmentStatusLogs', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Stores the status change logs of the equipment.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='ReservationStatus',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(unique=True, max_length=60)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'ReservationStatuses', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Stores the different statuses of a reservation.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='User',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=60)),
                ('email', fields.CharField(unique=True, max_length=60)),
                ('is_active', fields.BooleanField(default=True)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'Users', 'app': 'models', 'pk_attr': 'id', 'table_description': "Stores information about the system's users."},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Reservation',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='id', related_name='reservations', on_delete=OnDelete.CASCADE)),
                ('equipment', fields.ForeignKeyField('models.Equipment', source_field='equipment_id', db_constraint=True, to_field='id', related_name='reservations', on_delete=OnDelete.CASCADE)),
                ('start_time', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
                ('end_time', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
                ('status', fields.ForeignKeyField('models.ReservationStatus', source_field='status_id', db_constraint=True, to_field='id', related_name='reservations', on_delete=OnDelete.CASCADE)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'Reservations', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Stores information about reservations made by users.'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='UserAuth',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('username', fields.CharField(unique=True, max_length=60)),
                ('password_hash', fields.CharField(max_length=100)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', db_constraint=True, to_field='id', related_name='auths', on_delete=OnDelete.CASCADE)),
                ('created_at', fields.DatetimeField(default=naive_utcnow, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'UserAuth', 'app': 'models', 'pk_attr': 'id', 'table_description': 'Stores user credential information.'},
            bases=['Model'],
        ),
    ]
