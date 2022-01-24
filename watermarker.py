from PIL import Image


class Watermarker:

    def __init__(self, img="download.jpg"):
        self.image = Image.open(img)
        self.dimensions = (self.image.width, self.image.height)
        self.adjustment = 0
        self.watermark = ""
        self.mark_size = ()
        self.placements = []

    def set_watermark(self, watermark="download.jpg", mark_width=0, mark_height=0):
        self.watermark = watermark
        self.watermark_img = Image.open(watermark)
        self.adjustment = int(self.image.height * .15)
        if self.watermark_img.height > self.watermark_img.width:
            self.adjustment = int(self.image.height * .2)
            print(self.adjustment)
        if mark_width != 0 and mark_height != 0:
            self.mark_size = (mark_width, mark_height)
        elif self.watermark_img.height < self.adjustment:
            self.mark_size = (self.watermark_img.width, self.watermark_img.height)
        else:
            self.mark_size = (int((self.watermark_img.width/self.watermark_img.height) * self.adjustment),
                              self.adjustment)

    def watermark_image(self, position="lr"):
        self.watermark_img.thumbnail((self.mark_size[0], self.mark_size[1]))
        placements = {"lr": ((self.dimensions[0] - self.mark_size[0] - 10),
                             (self.dimensions[1] - self.mark_size[1] - 10)),
                      "ul": (10, 10),
                      "ur": ((self.dimensions[0] - self.mark_size[0] - 10), 10),
                      "ll": (10, (self.dimensions[1] - self.mark_size[1] - 10))}
        if "png" in self.watermark.lower():
            self.image.paste(self.watermark_img, placements[position], mask=self.watermark_img)
        else:
            self.image.paste(self.watermark_img, placements[position])

    def save_image(self, save_location="new_image.jpg"):
        self.image.save(save_location)
