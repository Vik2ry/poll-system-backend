from rest_framework import viewsets, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import Poll, Option
from .serializers import UserSerializer, PollSerializer, OptionSerializer, VoteSerializer
from .permissions import IsSuperUser, IsParticipant
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count
from drf_yasg import openapi

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint to manage users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    
    
    @swagger_auto_schema(
        operation_description="Retrieve all users created by superusers.",
        operation_summary="Retrieve all users.",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_description="Create a new participant user by providing required fields.",
        operation_summary="Create a new user.",
        request_body=UserSerializer,
        responses={201: UserSerializer(many=True)}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    # def get_permissions(self):
    #     """Allows anyone to register and only superusers to view/edit users"""
    #     if self.action == 'create':
    #         return [AllowAny()]
    #     return [IsAdminUser()]
    

class PollViewSet(viewsets.ModelViewSet):
    """
        API endpoint to manage polls.
        list: Retrieve all active polls.
        options_list: Retrieve the list of options for a poll.
        cast_vote: Submit a vote for a poll.
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(is_active=True, options__isnull=False).distinct()
    
    def get_permissions(self):
        if self.action == 'cast_vote':
            return [IsParticipant()]
        elif self.action == 'list':
            return [IsAuthenticated()] 
        return [IsSuperUser()]
    
    def get_serializer_class(self):
        if self.action in ["options_list"]:
            return OptionSerializer
        elif self.action == "cast_vote":
            return VoteSerializer
        else:
            return super().get_serializer_class()
        
        
    @swagger_auto_schema(
        operation_description="Retrieve all polls created by superusers.",
        operation_summary="Retrieve all polls.",
        responses={200: PollSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_description="Create a new poll by providing required fields.",
        operation_summary="Create a new poll.",
        request_body=PollSerializer,
        responses={201: PollSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_description="Retrieve a poll by providing the poll ID.",
        operation_summary="Retrieve a poll.",
        responses={200: PollSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    
    @swagger_auto_schema(
        operation_description="Update a poll by providing the poll ID and the fields to update.",
        operation_summary="Update a poll.",
        request_body=PollSerializer,
        responses={200: PollSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_description="Partially update a poll by providing the poll ID and the fields to update.",
        operation_summary="Partially update a poll.",
        request_body=PollSerializer,
        responses={200: PollSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a poll by providing the poll ID.",
        operation_summary="Delete a poll.",
        responses={204: "Poll deleted successfully ✔."}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


    # options action
    @swagger_auto_schema(
        method='get',
        operation_summary="Retrieve the list of options for a poll.",
        operation_description="Retrieve the list of options for a poll by providing the poll ID.",
        responses={200: OptionSerializer(many=True)}
    )
    @swagger_auto_schema(
        method='post',
        operation_summary="Add a new option to a poll.",
        operation_description="Add a new option to a poll.",
        request_body=OptionSerializer,
        responses={201: OptionSerializer(many=True)}
    )
    @action(detail=True, methods=['get', 'post'], url_path='options')
    def options_list(self, request, pk=None):
        poll = self.get_object()

        if request.method == 'GET':
            options = poll.options.all()
            serializer = self.get_serializer(options, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(poll=poll)
                return Response(self.get_serializer(Option.objects.filter(poll=poll), many=True).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='patch',
        operation_summary="Update an option in a poll.",
        operation_description="Update an option label in a poll by providing the poll ID and the option ID.",
        request_body=OptionSerializer,
        responses={200: OptionSerializer}
    )
    @swagger_auto_schema(
        method='delete',
        operation_summary="Delete an option in a poll.",
        operation_description="Delete an option in a poll by providing the poll ID and the option ID.",
        responses={204: "Option deleted successfully ✔."}
    )
    @action(detail=True, methods=['patch', 'delete'], url_path='options/(?P<option_id>[^/.]+)')
    def options_detail(self, request, pk=None, option_id=None):
        poll = self.get_object()
        option = get_object_or_404(Option, poll=poll, id=option_id)

        if request.method == 'PATCH':
            serializer = self.get_serializer(option, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            option.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    # cast-vote action
    @swagger_auto_schema(
        method='post',
        operation_description='allows a participant(registered user) to cast a vote for a poll',
        operation_summary="Submit a vote for a poll.",
        request_body=VoteSerializer,
        responses={201: "Vote cast successfully ✔."}
    )
    @action(detail=True, methods=['post'], url_path='cast-vote')
    def cast_vote(self, request, pk=None):
        poll = self.get_object()
        serializer = VoteSerializer(data=request.data, context={'request': request, 'poll': poll})
        if serializer.is_valid():
            serializer.save() 
            return Response({"message": "Vote cast successfully ✔."}, status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # results action
    @swagger_auto_schema(
        method='get',
        operation_summary="Retrieve the results of a poll.",
        operation_description="Retrieve the results of a poll by providing the poll ID.",
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=True, methods=['get'], url_path='results')
    def results(self, request, pk=None):
        poll = self.get_object()

        # Annotate the options with the number of votes : Query optimization
        options = poll.options.annotate(vote_count=Count('votes'))
        
        # build the response with the option label and the number of votes
        data = {option.label: option.vote_count for option in options}
        return Response(data, status=status.HTTP_200_OK)
    
