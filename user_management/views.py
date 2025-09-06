from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny  
from .models import Inspector, Admin, Worker, Client
from .serializers import InspectorReadSerializer, AdminReadSerializer, WorkerReadSerializer \
    , ClientReadSerializer, InspectorUpdateSerializer, AdminUpdateSerializer, WorkerUpdateSerializer \
    , ClientUpdateSerializer, WorkerRegistrationSerializer, \
    AdminRegistrationSerializer, InspectorRegistrationSerializer, ClientRegistrationSerializer 
from core.permissions import IsAdminOnly, IsWorkerOrInspector, IsAdminOrInspector


# Worker List/Create View

class InspectorListCreateView(generics.ListCreateAPIView):
    queryset = Inspector.objects.filter(inspector__is_active=True)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrInspector()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return InspectorRegistrationSerializer
        return InspectorReadSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the created objects from serializer
        created_objects = serializer.save()
        inspector = created_objects['inspector']
        
        # Return the inspector data using the read serializer
        read_serializer = InspectorReadSerializer(inspector)
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class InspectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inspector.objects.filter(inspector__is_active=True)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsAdminOrInspector()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return InspectorUpdateSerializer
        return InspectorReadSerializer

    def perform_destroy(self, instance):
        instance.inspector.is_active = False
        instance.inspector.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Inspector deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
        

# Admin List/Create View
class AdminListCreateView(generics.ListCreateAPIView):
    queryset = Admin.objects.filter(admin__is_active=True)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOnly()]
        return [AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminRegistrationSerializer
        return AdminReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_objects = serializer.save()
        
        # Return the admin data using read serializer
        read_serializer = AdminReadSerializer(created_objects['admin'])
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Admin.objects.filter(admin__is_active=True)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsAdminOnly()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminUpdateSerializer
        return AdminReadSerializer

    def perform_destroy(self, instance):
        instance.admin.is_active = False
        instance.admin.save()


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Admin deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    
# Worker List/Create View
class WorkerListCreateView(generics.ListCreateAPIView):
    queryset = Worker.objects.filter(worker__is_active=True)
    serializer_class = WorkerReadSerializer  # Default for GET requests

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrInspector()]
        return [AllowAny()]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkerRegistrationSerializer
        return WorkerReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            created_objects = serializer.save()
            worker_instance = created_objects['worker']
            
            # Use WorkerReadSerializer for response
            read_serializer = WorkerReadSerializer(worker_instance)
            headers = self.get_success_headers(read_serializer.data)
            return Response(
                read_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except KeyError:
            logger.error("Worker creation failed - no worker instance returned")
            return Response(
                {'error': 'Worker profile creation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Worker creation error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class WorkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.filter(worker__is_active=True)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsAdminOrInspector()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WorkerUpdateSerializer
        return WorkerReadSerializer

    def perform_destroy(self, instance):
        instance.worker.is_active = False
        instance.worker.save()


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Worker deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


# Client List/Create View
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.filter(client__is_active=True)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrInspector()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ClientRegistrationSerializer
        return ClientReadSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            created_objects = serializer.save()
            client_instance = created_objects['client']
            
            # Use ClientReadSerializer for response
            read_serializer = ClientReadSerializer(client_instance)
            headers = self.get_success_headers(read_serializer.data)
            return Response(
                read_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except KeyError:
            logger.error("Client creation failed - no client instance returned")
            return Response(
                {'error': 'Client profile creation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Client creation error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.filter(client__is_active=True)
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated(), IsAdminOrInspector()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ClientUpdateSerializer
        return ClientReadSerializer

    def perform_destroy(self, instance):
        instance.client.is_active = False
        instance.client.save()


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Client deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


