import warnings
from pathlib import Path
from rag_document_viewer.rag_document_viewer import RAG_Document_Viewer


class Unstructured_Document_Viewer(RAG_Document_Viewer):
    """
    Unstructured Document Viewer - Extension of RAG_Document_Viewer for Unstructured.io
    ====================================================================================

    This class extends RAG_Document_Viewer to provide native support for Unstructured.io's
    element format. It automatically converts pixel-based coordinates from Unstructured's
    API response to the ratio-based bounding box format required by the viewer.

    The class handles the coordinate transformation internally, allowing users to pass
    Unstructured elements directly without manual conversion.

    Coordinate Transformation:
        Unstructured uses pixel-based coordinates with four corner points arranged
        counter-clockwise from the top-left. This class converts them to ratios (0.0 to 1.0)
        relative to page dimensions:
        - top = y1 / layout_height
        - left = x1 / layout_width
        - height = (y2 - y1) / layout_height
        - width = (x2 - x1) / layout_width
    """

    def __init__(self, filepath, distpath=None, elements: list[dict] = None, chunks: list[list[str]] = None, configs={}):
        """
        Initialise the Unstructured document viewer converter.

        Args:
            filepath (str): Path to the input document file.
            distpath (str, optional): Output directory path. Defaults to input file directory.
            elements (list[dict]): Raw Unstructured API response containing element dictionaries.
                                   Each element should have 'element_id' and 'metadata' with
                                   'coordinates' and 'page_number'.
            chunks (list[list[str]]): List of chunks where each chunk is a list of element_ids.
                                      e.g., [["id1", "id2"], ["id3"]] means chunk 0 contains
                                      elements id1 and id2, chunk 1 contains element id3.
                                      If None or empty, each element with valid coordinates
                                      becomes its own chunk.
            configs (dict): Configuration options for styling and features.
        """
        if elements is None:
            raise Exception("Please pass Unstructured elements to build the previewer.")

        boxes = self._convert_unstructured_to_boxes(elements, chunks)
        super().__init__(filepath, distpath, boxes, configs)

    def _has_valid_coordinates(self, element: dict) -> bool:
        """
        Check if an Unstructured element has valid coordinates for conversion.

        Args:
            element: An element dict from Unstructured API response.

        Returns:
            True if element has all required coordinate data, False otherwise.
        """
        try:
            metadata = element.get("metadata")
            if not metadata:
                return False

            coords = metadata.get("coordinates")
            if not coords:
                return False

            points = coords.get("points")
            layout_width = coords.get("layout_width")
            layout_height = coords.get("layout_height")
            page_number = metadata.get("page_number")

            if not points or len(points) < 3:
                return False
            if not layout_width or layout_width <= 0:
                return False
            if not layout_height or layout_height <= 0:
                return False
            if page_number is None:
                return False

            return True
        except (TypeError, KeyError, IndexError):
            return False

    def _convert_unstructured_to_boxes(self, elements: list[dict], chunks: list[list[str]] = None) -> list[list[dict]]:
        """
        Convert Unstructured.io elements to RAG_Document_Viewer box format.

        Args:
            elements: Raw Unstructured API response (list of element dicts).
            chunks: List of chunks where each chunk is a list of element_ids.
                    If None or empty, each element with valid coordinates
                    becomes its own chunk.

        Returns:
            List of chunks in RAG_Document_Viewer format.
        """
        if not elements:
            return []

        element_lookup = {el.get("element_id"): el for el in elements if el.get("element_id")}

        # Auto-generate if not provided
        if not chunks:
            chunks = []
            for element in elements:
                element_id = element.get("element_id")
                if element_id and self._has_valid_coordinates(element):
                    chunks.append([element_id])
                elif element_id:
                    warnings.warn(f"Element '{element_id}' has no valid coordinates, skipping.")

        result = []
        for chunk_ids in chunks:
            chunk_boxes = []
            for element_id in chunk_ids:
                element = element_lookup.get(element_id)
                if not element:
                    warnings.warn(f"Element ID '{element_id}' not found in elements, skipping.")
                    continue

                if not self._has_valid_coordinates(element):
                    warnings.warn(f"Element '{element_id}' has no valid coordinates, skipping.")
                    continue

                metadata = element["metadata"]
                coords = metadata["coordinates"]
                points = coords["points"]
                layout_width = coords["layout_width"]
                layout_height = coords["layout_height"]
                page_number = metadata["page_number"]

                # Counter-clockwise from top-left: [0]=top-left, [1]=bottom-left, [2]=bottom-right
                x1, y1 = points[0][0], points[0][1]
                x2, y2 = points[2][0], points[1][1]

                width = x2 - x1
                height = y2 - y1

                if width < 0 or height < 0:
                    warnings.warn(f"Element '{element_id}' has negative dimensions, skipping.")
                    continue

                box = {
                    "page": page_number,
                    "top": y1 / layout_height,
                    "left": x1 / layout_width,
                    "height": height / layout_height,
                    "width": width / layout_width
                }
                chunk_boxes.append(box)

            result.append(chunk_boxes)

        return result


def Unstructured_DV(file_path: str = None, store_path: str = None, elements: list = None, chunks: list = None, **kwargs):
    """
    Unstructured_DV - Wrapper for Unstructured_Document_Viewer.

    This function provides a simple interface for generating interactive HTML previews
    from documents using Unstructured.io's element format. It handles coordinate
    conversion automatically.

    Args:
        file_path (str): Path to the input document file.
        store_path (str, optional): Output directory path. If not provided, creates a
                                    directory named after the input file.
        elements (list): Unstructured elements - either raw partition() output (Element objects)
                         or list of element dictionaries from the API response.
        chunks (list, optional): List of chunks where each chunk is a list of element_ids
                                 to group together. If not provided, each element with
                                 valid coordinates becomes its own chunk.
        **kwargs: Additional configuration options passed to the viewer.

    Raises:
        FileNotFoundError: If the specified file_path does not exist.
        FileExistsError: If the store_path directory already exists.
    """
    if file_path is None:
        raise FileNotFoundError(f"[{file_path}] not exist, please check.")

    # Handle both partition() output (Element objects) and list of dicts
    if elements and len(elements) > 0:
        if hasattr(elements[0], 'to_dict'):
            elements = [el.to_dict() for el in elements]

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"[{file_path}] not exist, please check.")

    if store_path is None:
        store_path = Path(file_path.parent / file_path.stem)
    else:
        store_path = Path(store_path)

    if not store_path.exists():
        store_path.mkdir(parents=True)
    else:
        raise FileExistsError(f"[{store_path}] already exist, please check.")

    configs = {}
    for key, value in kwargs.items():
        configs[key] = value

    viewer = Unstructured_Document_Viewer(file_path, store_path, elements, chunks, configs)
    viewer.convert_document()
