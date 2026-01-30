"""Chemical rendering services using Indigo library."""


class ChemicalRenderer:
    """Renders chemical structures to images using Indigo library."""

    SUPPORTED_FORMATS = ("png", "svg", "pdf")
    DEFAULT_WIDTH = 300
    DEFAULT_HEIGHT = 300
    DEFAULT_FORMAT = "png"

    def _get_indigo(self):
        """Lazy load Indigo to avoid import-time initialization issues."""
        from indigo import Indigo
        from indigo.renderer import IndigoRenderer

        indigo = Indigo()
        renderer = IndigoRenderer(indigo)
        return indigo, renderer

    def render_smiles(
        self,
        smiles: str,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
    ) -> tuple[bytes, str]:
        """Render SMILES string to image."""
        indigo, renderer = self._get_indigo()
        molecule = indigo.loadMolecule(smiles)
        return self._render_molecule(
            indigo, renderer, molecule, width, height, image_format
        )

    def render_molfile(
        self,
        molfile_content: str,
        width: int | None = None,
        height: int | None = None,
        image_format: str | None = None,
    ) -> tuple[bytes, str]:
        """Render MOL file content to image."""
        indigo, renderer = self._get_indigo()
        molecule = indigo.loadMolecule(molfile_content)
        return self._render_molecule(
            indigo, renderer, molecule, width, height, image_format
        )

    def _render_molecule(
        self,
        indigo,
        renderer,
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

        indigo.setOption("render-output-format", image_format)
        indigo.setOption("render-image-width", width)
        indigo.setOption("render-image-height", height)
        indigo.setOption("render-coloring", True)
        indigo.setOption("render-margins", 10, 10)

        image_bytes = renderer.renderToBuffer(molecule)

        content_type_map = {
            "png": "image/png",
            "svg": "image/svg+xml",
            "pdf": "application/pdf",
        }

        return bytes(image_bytes), content_type_map[image_format]


def get_chemical_renderer():
    """Get chemical renderer instance."""
    return ChemicalRenderer()
