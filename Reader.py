import tabula
from pdf2image import convert_from_path

class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.pages = convert_from_path(filename)
    def read_page(self, page, area):
        data = tabula.read_pdf(self.filename, pages=page, lattice=True, area = area )
        return data
    def read_unorganized_table(self, page, area):
        data = tabula.read_pdf(self.filename, pages=page, area = area )
        return data

    def save_table_image(self, page, area):
        selected_page=self.pages[page-1]
        image_path = f"./images/{page}.jpg"
        image=selected_page.crop(area)
        selected_page.save(image_path, "JPEG")
        image.show()
        return image



reader = Reader("file.pdf")
