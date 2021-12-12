from rest_framework import serializers
from .models import Poll, Question, Choices, UserPollAnswer, UserQuestionAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class PollDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = '__all__'

    @staticmethod
    def get_questions(obj):
        return QuestionDetailSerializer(Question.objects.filter(poll=obj), many=True).data


class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    @staticmethod
    def get_choices(obj):
        return ChoicesDetailSerializer(Choices.objects.filter(question=obj), many=True).data


class QuestionCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'question_type')


class QuestionUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text',)


class ChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = ('choices_options',)


class ChoicesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        fields = '__all__'


class UserQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuestionAnswer
        fields = ('question_id', 'question_text', 'answer')


class UserAnswerSerializator(serializers.Serializer):
    user_id = serializers.IntegerField()
    poll = serializers.IntegerField()
    questions = UserQuestionAnswerSerializer(many=True)
