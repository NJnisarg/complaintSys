from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import TagSerializer, ComplaintSerializer, RestrictedComplaintSerializer, CommentSerializer
from .models import Complaint, Tag


# COMPLAINT APIs #


# API only for both user and resolver
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_all_complaints(request):
    if request.user.groups.all()[0].name == 'resolver':
        complaint_objs = Complaint.objects.all()
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    elif request.user.groups.all()[0].name == 'user':
        complaint_objs = Complaint.objects.filter(complainant=request.user.username)
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# API only for both user and resolver
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_complaint(request, pk):
    if request.user.groups.all()[0].name == 'resolver':
        complaint_obj = Complaint.objects.get(pk=pk)
        serializer = ComplaintSerializer(complaint_obj)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    elif request.user.groups.all()[0].name == 'user':
        complaint_obj = Complaint.objects.get(pk=pk)
        if complaint_obj.complainant == request.user.username:
            serializer = ComplaintSerializer(complaint_obj)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"msg": "This User is not allowed to access this complaint object"})


# API for both user and resolver
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_complaint_by_complainant(request, pk):
    try:
        complainant = User.objects.get(username=pk)
        complaint_objs = Complaint.objects.filter(complainant=complainant.username)
        if complaint_objs is not None:
            serializer = ComplaintSerializer(complaint_objs, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"msg": "No complaints by the user"})
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"msg": "User not found"})


# API for both user and resolver
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def get_complaint_by_tags(request, pk):

    try:
        tag = Tag.objects.get(pk=pk)
        complaint_objs = Complaint.objects.filter(tag=tag.name)
        if complaint_objs is not None:
            serializer = ComplaintSerializer(complaint_objs, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"msg": "No complaints associated with the tag"})
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"msg": "No such tag found in database"})


# API for both user and resolver
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_complaint_resolved(request):
    if request.user.groups.all()[0].name == 'user':
        complaint_objs = Complaint.objects.filter(complainant=request.user.username).filter(status=True)
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    elif request.user.groups.all()[0].name == 'resolver':
        complaint_objs = Complaint.objects.filter(status=True)
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# API for both user and resolver
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_complaint_unresolved(request):
    if request.user.groups.all()[0].name == 'user':
        complaint_objs = Complaint.objects.filter(complainant=request.user.username).filter(status=False)
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    elif request.user.groups.all()[0].name == 'resolver':
        complaint_objs = Complaint.objects.filter(status=False)
        serializer = ComplaintSerializer(complaint_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


# API for only user
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_complaint_data(request, pk):
    if request.user.groups.all()[0].name == 'user':
        complaint_obj = Complaint.objects.get(pk=pk)
        if complaint_obj.complainant == request.user.username:
            serializer = RestrictedComplaintSerializer(complaint_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_serializer = ComplaintSerializer(complaint_obj)
                return Response(status=status.HTTP_200_OK, data=response_serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"msg": "The Complaint Object does not belong to the user"})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"msg": "This user group is not allowed to update the Complaint"})


# API for only resolver
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def resolve_complaint(request, pk):
    if request.user.groups.all()[0].name == 'resolver':
        complaint_obj = Complaint.objects.get(pk=pk)
        if not complaint_obj.status:
            complaint_obj.status = True
            complaint_obj.respondent = request.user.username
            complaint_obj.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_204_NO_CONTENT, data={"msg": "The Complaint is already resolved"})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"msg": "This group of user is not allowed to resolve complaints"})


# API for only resolver
@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def add_comment_to_complaint(request, pk):
    if request.user.groups.all()[0].name == 'resolver':
        complaint_obj = Complaint.objects.get(pk=pk)
        serializer = CommentSerializer(complaint_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ComplaintSerializer(complaint_obj)
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"msg": "This group of user is not allowed to Add comments to complaints"})


# API only for user
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def generate_complaint(request):
    if request.user.groups.all()[0].name == 'user':
        serializer = RestrictedComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "Malformed Request"})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN,
                        data={"msg": "This group of users is not allowed to post complaints"})


# # API only for user
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# @api_view(['DELETE'])
# def delete_complaint():


# TAG APIS #


# API for both user and resolver
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_all_tags(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


# API only for resolver
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# @api_view(['PUT'])
# def update_tag(request, pk):
#     if request.user.groups.all()[0] == 'resolver':
#         tag = Tag.objects.get(pk=pk)
#         complaint_objs = Complaint.objects.filter(tag=tag.name)
#         for complaint_obj in complaint_objs:
#             complaint_obj.tag = tag.name
#         complaint_serializer = ComplaintSerializer(complaint_objs, many=True)
#         complaint_serializer.save()
#         serializer = TagSerializer(tag, data=request.data)
#         return Response(status=status.HTTP_200_OK, data=serializer.data)
#     else:
#         return Response(status=status.HTTP_403_FORBIDDEN,
# data={"msg": "user in this group not allowed to update tags"})


# API only for resolver
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_tag(request):
    if request.user.groups.all()[0].name == 'resolver':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"msg": "Malformed Request"})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={"msg": "user in this group not allowed to create tags"})
