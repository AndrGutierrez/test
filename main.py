import tabula
from dbconnection import db
from Reader import reader
import json
import io
from PIL import Image
from bson.objectid import ObjectId



def dataframe_to_json_serializable(df):
    records = df.to_dict(orient='records')
    return records  # or json_string if you want the JSON string instead

def show_images():
    '''Select all images from db and show'''
    tables= db.connection.data.find({})
    for table in tables:
        imageBytes = io.BytesIO(table["image"])
        image = Image.open(imageBytes)
        image.show()

def add_image(image, data):
    '''convert image to binary for database'''
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    input ={
        "image": image_bytes.getvalue(),
        "data": data
    }
    return input

def get_and_insert(area, crop_area, page):
    '''Insert into database'''
    tables = reader.read_page(page, area)
    # tables = reader.read_page(page, area) 
    table=list(tables)[0]
    data=dataframe_to_json_serializable(table)
    image = reader.save_table_image(page, crop_area)
    input = add_image(image, data)
    id = db.save(input).inserted_id
    return id

def scrape(page):
    '''Transform and format all data'''
    transform_area=lambda area: [area[1]*2.8, area[0]*2.75, area[2]*2.5, area[3]*3]
    transform_area_type2=lambda area: [area[1], area[0]*2.9, area[2]*2.5, area[3]*3]
    transform_area_type3 = lambda area: [area[1], area[0]*2.9, area[3]*2, area[2]*2.5]
    if page['type'] == 1:
        crop_area = transform_area(page['area'])
    elif page['type'] == 2:
        crop_area = transform_area_type2(page['area'])
    else:
        crop_area = transform_area_type3(page['area'])
    get_and_insert(page['area'], crop_area, page['page'])



if __name__ == '__main__':
    with open('pages.json') as json_file:
        data = json.load(json_file)
    for item in data:
        scrape(item)



# FIXME
    # area = [210, 50, 800, 700]
    # page=22
    # id= get_and_insert(area, page, unorganized=True)

    # area = [150, 40, 800, 650]
    # page=57
    # id= get_and_insert(area, page)
    # show_image(id)

# CAPTURA NO FUNCIONA IGUAL QUE EN LO DEM[AS]


    show_images()
    # db.connection.table.delete_many({})
