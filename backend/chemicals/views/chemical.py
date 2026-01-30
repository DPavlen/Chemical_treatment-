from chemicals.schemas import get_extended_schema, post_extended_schema
from chemicals.serializers import ChemicalPostSerializer, SmilesGetSerializer
from chemicals.services import ChemicalRenderer, get_chemical_renderer, with_logging
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


def index_view(request):
    """Render the main page with the chemical structure form."""
    return render(request, "chemicals/index.html")


class ChemicalRenderView(APIView):
    """
    API endpoint for rendering chemical structures.
    Supports both SMILES strings and MOL files for chemical structure visualization.
    """

    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    @get_extended_schema
    @with_logging("GET")
    def get(self, request):
        """Render a chemical structure from SMILES string via GET request."""
        serializer = SmilesGetSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        image_format = data.get("format") or ChemicalRenderer.DEFAULT_FORMAT

        # Set logging data on request for decorator
        request._log_data = {
            "smiles": data["smiles"],
            "width": data.get("width"),
            "height": data.get("height"),
            "image_format": image_format,
        }

        image_bytes, content_type = get_chemical_renderer().render_smiles(
            smiles=data["smiles"],
            width=data.get("width"),
            height=data.get("height"),
            image_format=image_format,
        )

        response = HttpResponse(image_bytes, content_type=content_type)

        # Add download header if requested
        download = request.query_params.get("download", "").lower() in ("true", "1")
        if download:
            filename = f"molecule.{image_format}"
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    @post_extended_schema
    @with_logging("POST")
    def post(self, request):
        """Render a chemical structure from SMILES string or MOL file via POST request."""
        serializer = ChemicalPostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        image_format = data.get("format") or ChemicalRenderer.DEFAULT_FORMAT
        smiles = data.get("smiles")
        has_molfile = bool(data.get("molfile"))

        # Set logging data on request for decorator
        request._log_data = {
            "smiles": smiles,
            "has_molfile": has_molfile,
            "width": data.get("width"),
            "height": data.get("height"),
            "image_format": image_format,
        }

        if smiles:
            image_bytes, content_type = get_chemical_renderer().render_smiles(
                smiles=smiles,
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
            )
        else:
            molfile_content = data["molfile"].read().decode("utf-8")
            image_bytes, content_type = get_chemical_renderer().render_molfile(
                molfile_content=molfile_content,
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
            )

        return HttpResponse(image_bytes, content_type=content_type)
