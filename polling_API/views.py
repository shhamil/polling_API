from django.utils.datetime_safe import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework import generics
from .serializers import (PollSerializer,
                          PollDetailSerializer,
                          QuestionCreateSerializers,
                          QuestionUpdateSerializers,
                          ChoicesSerializer,
                          QuestionDetailSerializer,
                          UserAnswerSerializator,
                          UserQuestionAnswerSerializer)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Poll, Question, Choices, UserPollAnswer, UserQuestionAnswer


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Poll.objects.all()

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated],
            serializer_class=QuestionCreateSerializers)
    def create_question(self, request, pk=None):
        poll = Poll.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Question.objects.create(poll=poll,
                                    question_text=serializer.data['question_text'],
                                    question_type=serializer.data['question_type'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['delete'],
            permission_classes=[IsAuthenticated],
            url_path=r'delete_question/(?P<question_id>[^/.]+)')
    def delete_question(self, request, pk, question_id):
        ques = Question.objects.get(id=question_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['put'],
            permission_classes=[IsAuthenticated],
            serializer_class=QuestionUpdateSerializers,
            url_path=r'update_question/(?P<question_id>[^/.]+)')
    def update_question(self, request, pk, question_id):
        question = Question.objects.get(id=question_id)
        serializer = self.get_serializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated],
            serializer_class=ChoicesSerializer,
            url_path=r'question/(?P<question_id>[^/.]+)/add_choices')
    def add_choices(self, request, pk, question_id):
        ques = Question.objects.get(id=question_id)
        if ques.question_type == 1:
            return Response({"Невозможно добавить варианты ответа к вопросу с таким типом"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                Choices.objects.create(question=ques,
                                        choices_options=serializer.data['choices_options'])
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['get'],
            permission_classes=[IsAuthenticated],
            serializer_class=QuestionDetailSerializer,
            url_path=r'question/(?P<question_id>[^/.]+)/get_choices')
    def get_choices(self, request, pk, question_id):
        poll = Poll.objects.get(id=pk)
        ques = Question.objects.get(id=question_id)
        if ques.poll == poll:
            serializer = self.get_serializer(ques)
            return Response(serializer.data)
        else:
            return Response({"Вопрос с таким id относится к другому опросу"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['delete'],
            permission_classes=[IsAuthenticated],
            url_path=r'question/(?P<question_id>[^/.]+)/choices/(?P<choice_id>[^/.]+)')
    def delete_choices(self, request, pk, question_id, choice_id):
        poll = Poll.objects.get(id=pk)
        ques = Question.objects.get(id=question_id)
        choice = Choices.objects.get(id=choice_id)
        if ques.poll == poll and choice.question == ques:
            choice.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    action_to_serializer = {
        "retrieve": PollDetailSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class ActivePolls(APIView):

    def get(self, request):
        polls = Poll.objects.filter(end_date__gte=datetime.now())
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_active_poll(request, pk):
    poll = Poll.objects.get(id=pk)
    serializer = PollDetailSerializer(poll)
    return Response(serializer.data)


class CreateAnswer(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = ''
    serializer_class = UserAnswerSerializator

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data['user_id']
            poll = kwargs['pk']
            user_poll_ans = UserPollAnswer.objects.create(user_id=user_id, poll=poll)
            for question in serializer.data['questions']:
                question_origin = get_object_or_404(Question, pk=question['question_id'], question_text=question['question_text'])
                if question_origin.question_type == 1 and len(question['answer']) > 1:
                    return Response({'У этого вопроса свободный вариант ответа и он один'}, status=status.HTTP_400_BAD_REQUEST)
                elif question_origin.question_type == 2 and len(question['answer']) > 1:
                    if not Choices.objects.filter(question=question_origin, choices_options__contains=question['answer']):
                        return Response({'У этого вопроса только один вариант ответа. Выберите из списка вариантов ответа'},
                                        status=status.HTTP_400_BAD_REQUEST)
                elif question_origin.question_type == 3:
                    if not Choices.objects.filter(question=question_origin, choices_options__contains=question['answer']):
                        return Response({'Выберите ответы из списка вариантов ответов'}, status=status.HTTP_400_BAD_REQUEST)
                UserQuestionAnswer.objects.create(poll=user_poll_ans, question_id=question_origin.pk, question_text=question_origin.question_text, answer=question['answer'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_my_poll(request, pk):
    polls = UserPollAnswer.objects.filter(user_id=pk)
    response_list = []
    for poll in polls:
        questions = UserQuestionAnswer.objects.filter(poll=poll)
        response_list.append({'user_id': poll.user_id, 'poll': poll.poll,
                              'qustions': UserQuestionAnswerSerializer(questions, many=True).data})
    return Response(response_list, status=status.HTTP_200_OK)
