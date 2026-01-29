"""Serializers for chemical structure API."""

from chemicals.services import ChemicalRenderer
from rest_framework import serializers


class RenderOptionsSerializer(serializers.Serializer):
    """Common render options for chemical structure visualization."""

    width = serializers.IntegerField(
        required=False,
        min_value=50,
        max_value=2000,
        default=ChemicalRenderer.DEFAULT_WIDTH,
        help_text="Image width in pixels (50-2000)",
    )
    height = serializers.IntegerField(
        required=False,
        min_value=50,
        max_value=2000,
        default=ChemicalRenderer.DEFAULT_HEIGHT,
        help_text="Image height in pixels (50-2000)",
    )
    format = serializers.ChoiceField(
        required=False,
        choices=[(f, f.upper()) for f in ChemicalRenderer.SUPPORTED_FORMATS],
        default=ChemicalRenderer.DEFAULT_FORMAT,
        help_text="Output image format",
    )


class SmilesGetSerializer(RenderOptionsSerializer):
    """Serializer for GET request with SMILES string."""

    smiles = serializers.CharField(
        required=True,
        help_text="SMILES string representing the chemical structure (e.g., CCO for ethanol)",
    )
    download = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Set to true to download file instead of displaying",
    )


class ChemicalPostSerializer(RenderOptionsSerializer):
    """Serializer for POST request with SMILES or MOL file."""

    smiles = serializers.CharField(
        required=False,
        help_text="SMILES string representing the chemical structure",
    )
    molfile = serializers.FileField(
        required=False,
        help_text="MOL file containing the chemical structure",
    )

    def validate(self, attrs):
        """Ensure at least one of smiles or molfile is provided."""
        smiles = attrs.get("smiles")
        molfile = attrs.get("molfile")

        if not smiles and not molfile:
            raise serializers.ValidationError(
                "Either 'smiles' or 'molfile' must be provided."
            )

        if smiles and molfile:
            raise serializers.ValidationError(
                "Provide either 'smiles' or 'molfile', not both."
            )

        return attrs
