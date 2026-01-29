from indigo import Indigo
from indigo.renderer import IndigoRenderer


class ChemicalRenderer:
    """Renders chemical structures to images using Indigo library."""

    SUPPORTED_FORMATS = ("png", "svg", "pdf")
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 300
    DEFAULT_FORMAT = "png"

    def __init__(self):
        self.indigo = Indigo()
        self.renderer = IndigoRenderer(self.indigo)

    def render_smiles(
        self,
        smiles: str,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
    ) -> tuple[bytes, str]:
        """
        Render SMILES string to image.
        """
        molecule = self.indigo.loadMolecule(smiles)
        return self._render_molecule(molecule, width, height, image_format)

    def render_molfile(
        self,
        molfile_content: str,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
    ) -> tuple[bytes, str]:
        """
        Render MOL file content to image.
        """
        molecule = self.indigo.loadMolecule(molfile_content)
        return self._render_molecule(molecule, width, height, image_format)

    def _render_molecule(
        self,
        molecule,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
    ) -> tuple[bytes, str]:
        """Render molecule object to image bytes."""
        width = width or self.DEFAULT_WIDTH
        height = height or self.DEFAULT_HEIGHT
        image_format = (image_format or self.DEFAULT_FORMAT).lower()

        if image_format not in self.SUPPORTED_FORMATS:
            image_format = self.DEFAULT_FORMAT

        self.indigo.setOption("render-output-format", image_format)
        self.indigo.setOption("render-image-width", width)
        self.indigo.setOption("render-image-height", height)
        self.indigo.setOption("render-coloring", True)
        self.indigo.setOption("render-margins", 10, 10)

        image_bytes = self.renderer.renderToBuffer(molecule)

        content_type_map = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
        }

        return bytes(image_bytes), content_type_map[image_format]


chemical_renderer = ChemicalRenderer()
