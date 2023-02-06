"""
Adjusts the contrast of an image.
"""

from typing import Any, Dict

import cv2

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.base import ThresholdCheckerMixin


class Node(ThresholdCheckerMixin, AbstractNode):
    """Adjusts the contrast of an image, by multiplying with a gain/`alpha
    parameter <https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html>`_.
    Inputs:
        |img_data|
    Outputs:
        |img_data|
    Configs:
        clipLimit (:obj:`float`): **[0.0, 3.0], default = 1.0**. |br|
            Threshold for contrast limiting. 
        tileGridSize (:obj:`tuple`): **[0.0, 3.0], default = 1.0**. |br|
            Size of grid for histogram equalization. Input image will be divided into equally sized rectangular tiles. 
            tileGridSize defines the number of tiles in row and column.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        #self.check_bounds("alpha", "[0.0, 3.0]")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Adjusts the contrast of an image frame.
        Args:
            inputs (Dict): Inputs dictionary with the key `img`.
        Returns:
            (Dict): Outputs dictionary with the key `img`.
        """
        
        img = inputs["img"]
        
        
        
        # converting to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        
        # create a CLAHE object.
        clahe = cv2.createCLAHE(clipLimit=self.clipLimit, tileGridSize=self.tileGridSize)
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        
        # Converting image from LAB Color model to BGR color space
        enhanced_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return {"img": enhanced_img}

    def _get_config_types(self) -> Dict[str, Any]:
        """Returns dictionary mapping the node's config keys to respective types."""
        return {"clipLimit": float, "tileGridSize": list}