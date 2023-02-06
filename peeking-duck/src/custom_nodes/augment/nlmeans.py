from typing import Any, Dict

import cv2 as cv

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.base import ThresholdCheckerMixin

class Node(ThresholdCheckerMixin, AbstractNode):
    """Using Non-local Means Denoising algorithm to remove noise in the image.
    <https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html>
    
    Inputs:
        |img_data|
    Outputs:
        |img_data|
    Configs:
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
        
        dst = cv.fastNlMeansDenoisingColored(img,self.h,self.hColor,self.templateWindowSize,self.searchWindowSize)
        
        return {"img": dst}

    def _get_config_types(self) -> Dict[str, Any]:
        """Returns dictionary mapping the node's config keys to respective types."""
        return {"h": float, "hColor": float,"templateWindowSize": int, "searchWindowSize":int}
    