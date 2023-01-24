from rest_framework import serializers

from api.models.backup_schedule import BackupSchedule


class BackupScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSchedule
        fields = ('id', 'name', 'description', 'each_nth_minute',
                  'next_start', 'last_start', 'disabled', 'backup_job')


class BackupSchedulePostSerializer(BackupScheduleSerializer):
    pass


class BackupScheduleRetrieveSerializer(BackupScheduleSerializer):
    pass


class BackupScheduleGbModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSchedule
        fields = ('id', 'name', 'description',
                  'next_start')


class BackupScheduleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSchedule
        fields = ('id', 'name')


class BackupScheduleListSerializer(BackupScheduleBaseSerializer):
    pass


class BackupScheduleGetShortSerializer(BackupScheduleBaseSerializer):
    pass


class BackupScheduleOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSchedule
        fields = ('id',)
