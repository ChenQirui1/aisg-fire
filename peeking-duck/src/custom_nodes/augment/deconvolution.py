import numpy as np
from skimage import color, restoration
from skimage.restoration import wiener
from scipy.signal import convolve2d
import cv2

from typing import Any, Dict

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.base import ThresholdCheckerMixin

class Node(ThresholdCheckerMixin, AbstractNode):
    """Adjusts the contrast of an image, by multiplying with a gain/`alpha
    parameter <https://docs.opencv.org/4.x/d3/dc1/tutorial_basic_
    linear_transform.html>`_.
    Inputs:
        |img_data|
    Outputs:
        |img_data|
    Configs:
        alpha (:obj:`float`): **[0.0, 3.0], default = 1.0**. |br|
            Increasing the value of alpha increases the contrast.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Adjusts the contrast of an image frame.
        Args:
            inputs (Dict): Inputs dictionary with the key `img`.
        Returns:
            (Dict): Outputs dictionary with the key `img`.
        """
        
        img = inputs['img']
        
        #transform to ycc
        transcol=cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
        
        #y-extraction 
        y_component = transcol[:,:,0]
        
        y_deconvolved = self.wiener_filter(y_component)
        
        #get r,g,b deconvolved
        r_deconvolved = self.wiener_filter(img[:,:,0])
        
        g_deconvolved = self.wiener_filter(img[:,:,1])
        
        b_deconvolved = self.wiener_filter(img[:,:,2])
        
        rgb = np.dstack((r_deconvolved,g_deconvolved,b_deconvolved))
        
        rgb = cv2.imread("rgb", rgb.astype(np.uint8))
        
        print(rgb.shape)
        #transform to ycc
        rgb_deconvolved = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCR_CB)
        
        #cr_cb extraction
        cr_deconvolved = rgb_deconvolved[:,:,1]
        cb_deconvolved = rgb_deconvolved[:,:,2]
        
        ycr_cb_deconvolved =  np.dstack((y_deconvolved,cr_deconvolved,cb_deconvolved))
        
        #return to rgb 
        image_rgb = cv2.cvtColor(ycr_cb_deconvolved, cv2.COLOR_YCR_CB2RGB)
        
        
        return {"img": image_rgb}
    
    def wiener_filter(self,img):
        rng = np.random.default_rng()

        psf = np.ones((5, 5)) / 25
        img = convolve2d(img, psf, 'same')
        img += 0.1 * img.std() * rng.standard_normal(img.shape)

        deconvolved, _ = restoration.unsupervised_wiener(img, psf)
        
        return deconvolved

    def _get_config_types(self) -> Dict[str, Any]:
        """Returns dictionary mapping the node's config keys to respective types."""
        return {}