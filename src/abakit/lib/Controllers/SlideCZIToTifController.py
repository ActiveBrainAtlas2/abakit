from abakit.lib.Controllers.Controller import Controller
from abakit.model.slide_czi_to_tif import SlideCziTif
from abakit.model.slide import Slide
class SlideCZIToTifController(Controller):
    def get_tif(self, ID):
        """
        Args:
            id: integer primary key

        Returns: one tif
        """
        return self.session.query(SlideCziTif).get(ID)

    def get_slide_czi_to_tifs(self, channel):
        slides = self.session.query(Slide).filter(Slide.scan_run_id == self.scan_run.id)\
            .filter(Slide.slide_status == 'Good').all()
        slide_czi_to_tifs = self.session.query(SlideCziTif).filter(SlideCziTif.channel == channel)\
            .filter(SlideCziTif.slide_id.in_([slide.id for slide in slides]))\
            .filter(SlideCziTif.active == 1).all()

        return slide_czi_to_tifs

    def update_tif(self, id, width, height):
        try:
            self.session.query(SlideCziTif).filter(
                SlideCziTif.id == id).update({'width': width, 'height': height})
            self.session.commit()
        except Exception as e:
            print(f'No merge for  {e}')
            self.session.rollback()
