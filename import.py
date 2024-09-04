class DatasetUploadView(APIView):
    serializer_class = DatasetUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            userId = serializer.validated_data['userId']
            file_path = default_storage.save(uploaded_file.name, uploaded_file)

            file_size_bytes = uploaded_file.size
            file_size_gb =