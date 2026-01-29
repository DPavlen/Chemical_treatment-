"""API views for chemical structure rendering."""

import time

from chemicals.models import RequestLog
from chemicals.schemas import get_schema, post_schema
from chemicals.serializers import ChemicalPostSerializer, SmilesGetSerializer
from chemicals.services import ChemicalRenderer, chemical_renderer
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


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

    def _log_request(
        self,
        request,
        method: str,
        smiles: str | None = None,
        has_molfile: bool = False,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
        success: bool = True,
        error_message: str | None = None,
        response_time_ms: int | None = None,
    ):
        """Log API request to database."""
        user = request.user if request.user.is_authenticated else None
        RequestLog.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            method=method,
            smiles=smiles,
            has_molfile=has_molfile,
            width=width,
            height=height,
            image_format=image_format or "",
            success=success,
            error_message=error_message,
            response_time_ms=response_time_ms,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )

    @get_schema
    def get(self, request):
        """Render a chemical structure from SMILES string via GET request."""
        start_time = time.time()
        serializer = SmilesGetSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        image_format = data.get("format") or ChemicalRenderer.DEFAULT_FORMAT

        try:
            image_bytes, content_type = chemical_renderer.render_smiles(
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

            # Log successful request
            response_time_ms = int((time.time() - start_time) * 1000)
            self._log_request(
                request=request,
                method="GET",
                smiles=data["smiles"],
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
                success=True,
                response_time_ms=response_time_ms,
            )

            return response

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self._log_request(
                request=request,
                method="GET",
                smiles=data.get("smiles"),
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
                success=False,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )
            return Response(
                {"error": f"Failed to render molecule: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @post_schema
    def post(self, request):
        """Render a chemical structure from SMILES string or MOL file via POST request."""
        start_time = time.time()
        serializer = ChemicalPostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        image_format = data.get("format") or ChemicalRenderer.DEFAULT_FORMAT
        smiles = data.get("smiles")
        has_molfile = bool(data.get("molfile"))

        try:
            if smiles:
                image_bytes, content_type = chemical_renderer.render_smiles(
                    smiles=smiles,
                    width=data.get("width"),
                    height=data.get("height"),
                    image_format=image_format,
                )
            else:
                molfile_content = data["molfile"].read().decode("utf-8")
                image_bytes, content_type = chemical_renderer.render_molfile(
                    molfile_content=molfile_content,
                    width=data.get("width"),
                    height=data.get("height"),
                    image_format=image_format,
                )

            # Log successful request
            response_time_ms = int((time.time() - start_time) * 1000)
            self._log_request(
                request=request,
                method="POST",
                smiles=smiles,
                has_molfile=has_molfile,
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
                success=True,
                response_time_ms=response_time_ms,
            )

            return HttpResponse(image_bytes, content_type=content_type)

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self._log_request(
                request=request,
                method="POST",
                smiles=smiles,
                has_molfile=has_molfile,
                width=data.get("width"),
                height=data.get("height"),
                image_format=image_format,
                success=False,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )
            return Response(
                {"error": f"Failed to render molecule: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
