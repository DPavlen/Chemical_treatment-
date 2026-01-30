from chemicals.serializers import ChemicalPostSerializer
from chemicals.services import ChemicalRenderer
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

# Response definitions
IMAGE_RESPONSES = {
    200: {
        "content": {
            "image/png": {},
            "image/svg+xml": {},
            "application/pdf": {},
        },
        "description": "Rendered chemical structure image",
    },
    400: {"description": "Invalid input or parameters"},
}

get_extended_schema = extend_schema(
    tags=["Chemical Rendering"],
    summary="Render chemical structure from SMILES",
    description="Generate an image of a chemical structure from a SMILES string.",
    parameters=[
        OpenApiParameter(
            name="smiles",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="SMILES string (e.g., CCO for ethanol, c1ccccc1 for benzene)",
            examples=[
                OpenApiExample(
                    "Ethanol",
                    value="CCO",
                    description="Ethanol molecule",
                ),
                OpenApiExample(
                    "Benzene",
                    value="c1ccccc1",
                    description="Benzene ring",
                ),
                OpenApiExample(
                    "Aspirin",
                    value="CC(=O)Oc1ccccc1C(=O)O",
                    description="Aspirin (acetylsalicylic acid)",
                ),
            ],
        ),
        OpenApiParameter(
            name="width",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description=f"Image width in pixels (default: {ChemicalRenderer.DEFAULT_WIDTH})",
        ),
        OpenApiParameter(
            name="height",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description=f"Image height in pixels (default: {ChemicalRenderer.DEFAULT_HEIGHT})",
        ),
        OpenApiParameter(
            name="format",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=list(ChemicalRenderer.SUPPORTED_FORMATS),
            description=f"Image format (default: {ChemicalRenderer.DEFAULT_FORMAT})",
        ),
        OpenApiParameter(
            name="download",
            type=bool,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Set to true to download file instead of displaying",
        ),
    ],
    responses=IMAGE_RESPONSES,
)

post_extended_schema = extend_schema(
    tags=["Chemical Rendering"],
    summary="Render chemical structure from SMILES or MOL file",
    description=(
        "Generate an image of a chemical structure from either a SMILES string "
        "or a MOL file upload. Use multipart/form-data for file uploads."
    ),
    request={
        "multipart/form-data": ChemicalPostSerializer,
    },
    examples=[
        OpenApiExample(
            "SMILES Example",
            value={
                "smiles": "CC(=O)Oc1ccccc1C(=O)O",
                "width": 400,
                "height": 400,
                "format": "png",
            },
            request_only=True,
            media_type="multipart/form-data",
        ),
    ],
    responses=IMAGE_RESPONSES,
)
