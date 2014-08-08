import settings
import re
import os
import util
import datetime

class SensorProduct(object):

    # full path to the file containing the input product
    input_file_path = None
    
    # full path where the output file should be placed
    output_file_path = None
    
    # http, ftp, scp, file, etc
    input_scheme = None    
    input_host = None
    input_port = None
    input_file_name = None
    input_user = None
    input_pw = None
    input_url = None
    
    # http, ftp, scp, file, etc
    output_scheme = None
    output_host = None    
    output_port = None
    output_file_name = None
    output_user = None
    output_pw = None
    output_url = None
  
    # landsat sceneid, modis tile name, aster granule id, etc.
    product_id = None
    
    # landsat l1t, modis 09A1, 09A2, etc.
    product_code = None
    
    # lt5, le7, mod, myd, etc
    sensor_code = None
    
    # tm, etm, terra, aqua, etc
    sensor_name = None
    
    # four digits
    year = None
    
    # three digits
    doy = None
    
    # last 5 for LANDSAT, collection # for MODIS
    version = None

    # this is in meters    
    default_pixel_size = None
    
           
    def __init__(self, product_id):
        self.product_id = product_id
        self.sensor_code = product_id[0:3]
        self.sensor_name = settings.SENSOR_NAMES[self.sensor_code.upper()]
        
    # subclasses should override, construct and return string    
    def input_exists(self):
        raise NotImplementedError()
        
    # subclasses should override, construct and return string
    def output_exists(self):
        raise NotImplementedError()
    
    def get_input_product(self, target_directory):
        raise NotImplementedError()
        
         
class Modis(SensorProduct):
    version = None
    short_name = None
    horizontal = None
    vertical = None
    date_acquired = None
    date_produced = None
    
    def __init__(self, product_id):
        
        super(Modis, self).__init__(product_id)
        
        self.input_file_name = ''.join([product_id,
                                       settings.MODIS_INPUT_FILENAME_EXTENSION])
        
        parts = product_id.strip().split('.')

        self.short_name = parts[0]
        self.date_acquired = parts[1][1:]
        self.year = self.date_acquired[0:4]
        self.doy = self.date_acquired[4:8]
        
        hv = parts[2]
        self.horizontal = hv[1:3]
        self.vertical = hv[4:6]
        self.version = parts[3]
        self.date_produced = parts[4]
        
        self.product_code = self.short_name[3:7]
        
    def build_input_file_path(self, base_source_path):
        print(self.year)
        print(self.doy)
        
        date = util.date_from_doy(self.year, self.doy)

        path_date = "%s.%s.%s" % (date.year, 
                                  str(date.month).zfill(2),
                                  str(date.day).zfill(2))
        
        self.input_file_path = os.path.join(
            base_source_path,
            '.'.join([self.short_name.upper(), self.version.upper()]),
            path_date.upper(),
            self.input_file_name)

        
class Terra(Modis):
    def __init__(self, product_id):
        super(Terra, self).__init__(product_id)
        self.build_input_file_path(settings.TERRA_BASE_SOURCE_PATH)
        
        
class Aqua(Modis):
    def __init__(self, product_id):
        super(Aqua, self).__init__(product_id)
        self.build_input_file_path(settings.AQUA_BASE_SOURCE_PATH)
        
               
class ModisTerra09A1(Terra):
    def __init__(self, product_id):
        super(ModisTerra09A1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09A1']
        
        
class ModisTerra09GA(Terra):
    def __init__(self, product_id):
        super(ModisTerra09GA, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09GA']


class ModisTerra09GQ(Terra):
    def __init__(self, product_id):
        super(ModisTerra09GQ, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09GQ']
        
        
class ModisTerra09Q1(Terra):
    def __init__(self, product_id):
        super(ModisTerra09Q1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09Q1']
        
        
class ModisTerra13A1(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A1']


class ModisTerra13A2(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A2, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A2']

        
class ModisTerra13A3(Terra):
    def __init__(self, product_id):
        super(ModisTerra13A3, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A3']

        
class ModisTerra13Q1(Terra):
    def __init__(self, product_id):
        super(ModisTerra13Q1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13Q1']
        
        
class ModisAqua09A1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09A1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09A1']
        
        
class ModisAqua09GA(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09GA, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09GA']


class ModisAqua09GQ(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09GQ, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09GQ']
        
        
class ModisAqua09Q1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua09Q1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['09Q1']
        
        
class ModisAqua13A1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A1']


class ModisAqua13A2(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A2, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A2']

        
class ModisAqua13A3(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13A3, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13A3']

        
class ModisAqua13Q1(Aqua):
    def __init__(self, product_id):
        super(ModisAqua13Q1, self).__init__(product_id)
        self.default_pixel_size = settings.DEFAULT_PIXEL_SIZE['13Q1']

              
class Landsat(SensorProduct):
    path = None
    row = None
    station = None
    
    def __init__(self, product_id):

        product_id = product_id.strip()
        
        super(Landsat, self).__init__(product_id)

        self.input_file_name = ''.join([product_id,
                                        settings.LANDSAT_INPUT_FILENAME_EXTENSION])
        
        self.default_pixel_size = \
            settings.DEFAULT_PIXEL_SIZE[self.sensor_code.upper()]
        
        self.path = util.strip_zeros(product_id[3:6])
        self.row = util.strip_zeros(product_id[6:9])
        self.year = product_id[9:13]
        self.doy = product_id[13:16]
        self.station = product_id[16:19]
        self.version = product_id[19:21]
        
        self.input_file_path = os.path.join(
            settings.LANDSAT_BASE_SOURCE_PATH,
            self.sensor_name,
            self.path,
            self.row,
            self.year,
            self.input_file_name)
        

    
class LandsatTM(Landsat):
    def __init__(self, product_id):
        super(LandsatTM, self).__init__(product_id)
               
        
class LandsatETM(Landsat):
    def __init__(self, product_id):
        super(LandsatETM, self).__init__(product_id)
        

def instance(product_id):
    '''
    Supported MODIS products
    MOD09A1	 MOD09GA MOD09GQ MOD09Q1 MYD09A1 MYD09GA MYD09GQ MYD09Q1
    MOD13A1	 MOD13A2 MOD13A3 MOD13Q1 MYD13A1 MYD13A2 MYD13A3 MYD13Q1
    
    MODIS FORMAT:   MOD09GQ.A2000072.h02v09.005.2008237032813
    
    Supported LANDSAT products
    LT4 LT5 LE7
    
    LANDSAT FORMAT: LE72181092013069PFS00
        
    '''
    
    _id = product_id.lower().strip()
        
    instances = {
        'tm': (r'^lt[4|5]\d{3}\d{3}\d{4}\d{3}[a-z]{3}[a-z0-9]{2}$',
               LandsatTM),
               
        'etm': (r'^le7\d{3}\d{3}\d{4}\d{3}\w{3}.{2}$',
                LandsatETM),
                
        'mod09a1': (r'^mod09a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisTerra09A1),
                  
        'mod09ga': (r'^mod09ga\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisTerra09GA),
                  
        'mod09gq': (r'^mod09gq\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisTerra09GQ),
                  
        'mod09q1': (r'^mod09q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisTerra09Q1),
                  
        'mod13a1': (r'^mod13a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A1),
                    
        'mod13a2': (r'^mod13a2\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A2),
                    
        'mod13a3': (r'^mod13a3\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13A3),
                    
        'mod13q1': (r'^mod13q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisTerra13Q1),
                    
        'myd09a1': (r'^myd09a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisAqua09A1),
                  
        'myd09ga': (r'^myd09ga\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisAqua09GA),
                  
        'myd09gq': (r'^myd09gq\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisAqua09GQ),
        
        'myd09q1': (r'^myd09q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                  ModisAqua09Q1),
                  
        'myd13a1': (r'^myd13a1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A1),
                    
        'myd13a2': (r'^myd13a2\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A2),
        
        'myd13a3': (r'^myd13a3\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13A3),
                    
        'myd13q1': (r'^myd13q1\.a\d{7}\.h\d{2}v\d{2}\.005\.\d{13}$',
                    ModisAqua13Q1)
    }
            
    for key in instances.iterkeys():
        if re.match(instances[key][0], _id):
            return instances[key][1](product_id)
            
    msg = "[%s] is not a supported sensor product" % product_id
    raise NotImplementedError(msg)
    