
'''
License:
  "NASA Open Source Agreement 1.3"

Description:
  Build science products from Landsat L4TM, L5TM, and L7ETM+ data.

History:
  Original Development (cdr_ecv.py) by David V. Hill, USGS/EROS
  Created Jan/2014 by Ron Dilley, USGS/EROS
    - Gutted the original implementation from cdr_ecv.py and placed it in this
      file.
'''

# espa-common objects and methods
from espa_constants import *


class ErrorCodes:
    '''
    Description:
      Defines the error codes to use for cdr_ecv core processing.
    '''

    ###########################################################################
    # Use EXIT_SUCCESS for 0
    # Use EXIT_FAILURE for 1
    ###########################################################################

    exception                 =  2 # Exited on an exception that does not have
                                   # a specific code

    # Generated by staging.initialize_processing_directory
    creating_stage_dir        =  3
    creating_work_dir         =  4
    creating_output_dir       =  5

    # Generated by transfer.stage_landsat_data
    staging_data              =  6

    # Generated by cdr_ecv.process
    unpacking                 =  7

    # Generated by science.build_landsat_science_products
    metadata                  =  8
    ledaps                    =  9
    browse                    = 10
    spectral_indices          = 11
    create_dem                = 12
    solr                      = 13
    cfmask                    = 14
    cfmask_append             = 15
    swe                       = 16
    sca                       = 17
    cleanup_work_dir          = 18

    # Generated by warp.warp_espa_data
    warping                   = 19

    # Generated by statistics.generate_statistics
    statistics                = 20

    # Generated by distribution.deliver_product
    packaging_product         = 21
    distributing_product      = 22
    verifing_checksum         = 23

    # Generated by science.build_landsat_science_products
    remove_products           = 24

    # Generated by warp.reformat
    # Generated by science.build_landsat_science_products
    # Generated by modis.process
    reformat                  = 25

# END class ErrorCodes


class ESPAException(Exception):
    '''
    Description:
      Create a special ESPA exception for returning errors back up to the main
      or top-level calling routine.  This allows that routine to make decisions
      based on the error code and move on.
    '''

    # Define our error code attribute
    error_code = EXIT_SUCCESS

    def __init__(self, error_code, message):

        # Call the base class constructor
        Exception.__init__(self, message)

        # Set our error code
        self.error_code = error_code
# END class ESPAException

