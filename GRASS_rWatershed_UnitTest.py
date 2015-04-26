"""
Name:       GRASS_rWatershed_UnitTest
Purpose:    This script is to demonstrate a unit test for GRASS's r.Watershed
            module for GIS582 at NCSU. This Unit Test must be placed in the
            directory testsuite of the GRASS installation.

Author:     Stephanie Wendel - sawendel
GRASS:      7.1.svn-r665096-56
Version:    1.4
Modified:   4/20/2015
Copyright:  (c) sawendel 2015
Licence:    GNU GPL
"""

# import grass testing module gunittest
import grass.gunittest
from grass.gunittest import TestCase, test

#test case for watershed module which is derived from grass.gunittest.TestCase
class TestWatershed(grass.gunittest.TestCase):

    #Setup variables to be used for outputs
    accumulation ='test_accumulation'
    drainage ='test_drainage'
    basin ='test_basin'
    stream ='test_stream'
    halfbasin ='test_halfbasin'
    slopelength='test_slopelength'
    slopesteepness = 'test_slopesteepness'
    elevation = 'elevation'

    @classmethod
    def setUpClass(cls):
        """Ensures expected computational region and setup"""
        #Always use the computational region of the raster elevation
        cls.use_temp_region()
        cls.runModule('g.region', raster=cls.elevation)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary region"""
        cls.del_temp_region()

    def tearDown(cls):
        """Remove the outputs created from the watershed module after each test
        is run."""
        cls.runModule('g.remove', flags='f', type='raster',
            name='{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(cls.accumulation,
            cls.drainage, cls.basin, cls.stream, cls.halfbasin,
            cls.slopelength, cls.slopesteepness, 'test_lengthslope_4',
            'test_stream_4'))

    def test_OutputCreated(self):
        """Test to see if the outputs are created"""
        #run the watershed module
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='10000', accumulation=self.accumulation,
            drainage=self.drainage, basin=self.basin, stream=self.stream,
            half_basin=self.halfbasin, length_slope=self.slopelength,
            slope_steepness=self.slopesteepness)
        #check to see if accumulation output is in mapset
        self.assertRasterExists(self.accumulation,
            msg='accumulation output was not created')
        #check to see if drainage output is in mapset
        self.assertRasterExists(self.drainage,
            msg='drainage output was not created')
        #check to see if basin output is in mapset
        self.assertRasterExists(self.basin,
            msg='basin output was not created')
        #check to see if stream output is in mapset
        self.assertRasterExists(self.stream,
            msg='stream output was not created')
        #check to see if half.basin output is in mapset
        self.assertRasterExists(self.halfbasin,
            msg='half.basin output was not created')
        #check to see if length.slope output is in mapset
        self.assertRasterExists(self.slopelength,
            msg='length.slope output was not created')
        #check to see if slope.steepness output is in mapset
        self.assertRasterExists(self.slopesteepness,
            msg='slope.steepness output was not created')

    def test_fourFlag(self):
        """Test the -4 flag to see if the stream and slope lengths are
        approximately the same as the outputs from the default module run"""
        #Run module with default settings
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='10000', stream=self.stream,
            length_slope=self.slopelength, overwrite=True)
        #Run module with flag 4
        self.assertModule('r.watershed', flags='4', elevation='elevation',
            threshold='10000', stream='test_stream_4',
            length_slope='test_lengthslope_4')
        #Use the assertRastersNoDifference with precsion 100 to see if close
        #Compare stream output
        self.assertRastersNoDifference('test_stream_4', self.stream, 100)
        #Compare length_slope output
        self.assertRastersNoDifference('test_lengthslope_4',
            self.slopelength, 10)

    def test_watershedThreadholdfail(self):
        """Check to see if it will allow for a threshold of 0 or a negative"""
        self.assertModuleFail('r.watershed', elevation=self.elevation,
            threshold='0', stream=self.stream, overwrite=True,
            msg='Threshold value of 0 considered valid.')
        self.assertModuleFail('r.watershed', elevation=self.elevation,
            threshold='-1', stream=self.stream, overwrite=True,
            msg='Threshold value of 0 considered valid.')

    def test_thresholdsize(self):
        """Check to see if the basin output is within the range of values
        expected"""
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='100000', basin=self.basin, overwrite=True)
        # it is expected that 100k Threshold has a min=2 and max=12 for this data
        self.assertRasterMinMax(self.basin, 2, 12)
        # it is expected that 100k Threshold has a min=2 and max=256 for this data
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='10000', basin=self.basin, overwrite=True)
        self.assertRasterMinMax(self.basin, 2, 256)

    def test_drainageDirection(self):
        """Check to see if the drainage direction is between -8 and 8."""
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='100000', drainage=self.drainage)
        #Make sure the min/max is between -8 and 8
        self.assertRasterMinMax(self.drainage, -8, 8,
            msg='Direction must be between -8 and 8')

    def test_basinValue(self):
        """Check to see if the basin value is 0 or greater"""
        self.assertModule('r.watershed', elevation=self.elevation,
            threshold='10000', basin=self.basin)
        #Make sure the minimum value is 0 for basin value representing unique positive integer.
        self.assertRasterMinMax(self.basin, 0, 1000000,
            msg='A basin value is less than 0 or greater than 1000000')

if __name__ == '__main__':
    test()