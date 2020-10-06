from .models import User, Project, Sequence, Shot, Task
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "user"]


class AssignedToField(serializers.Field):
    def to_representation(self, value):
        user = value.assigned_to
        ret = {}
        if user.exists():
            ret = {"username": user.username}
        print(user)

        return ret

    def to_internal_value(self, data):
        ret = {"assigned_to": data["username"]}
        return ret


class TaskSerializer(serializers.ModelSerializer):
    assignedUser = AssignedToField(source="*")

    class Meta:
        model = Task
        fields = [
            "task_name",
            "pipeline_step",
            "status",
            "startdate",
            "duedate",
            "assignedUser",
        ]


class ShotSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Shot
        fields = ["shotcode", "status", "cut_in", "cut_out", "cut_duration", "tasks"]


class SequenceSerializer(serializers.ModelSerializer):
    shots = ShotSerializer(many=True, read_only=True)

    class Meta:
        model = Sequence
        fields = ["name", "status", "description", "shots"]


class ProjectSerializer(serializers.ModelSerializer):
    sequences = SequenceSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

