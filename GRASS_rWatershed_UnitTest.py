"""
Name:       GRASS_rWatershed_UnitTest
Purpose:    This script is to demonstrate a unit test for GRASS's r.Watershed
            module for GIS582 at NCSU. This Unit Test must be placed in the
            directory testsuite of the GRASS installation.

Author:     Stephanie Wendel - sawendel
GRASS:      7.1.svn-r64925-36
Version:    1.2
Modified:   4/8/2015
Copyright:  (c) sawendel 2015
Licence:    GNU GPL
"""

# import grass testing module gunittest
import grass.gunittest
from grass.gunittest import TestCase, test

#test case for watershed module which is derived from grass.gunittest.TestCase
class TestWatershed(grass.gunittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Ensures expected computational region and setup"""
        #Always use the computational region of the raster elevation
        self.use_temp_region()
        self.runModule('g.region', raster='elevation')

    @classmethod
    def tearDownClass(self):
        """Remove the temporary region"""
        self.del_temp_region()

    def tearDown(self):
        """Remove the outputs created from the watershed module after each test
        is run."""
        self.runModule('g.remove', flags='f', type='raster',
            name='test_accumulation,test_drainage,test_basin,test_stream,test_halfbasin,test_lengthslope,test_slopesteepness')
        self.runModule('g.remove', flags='f', type='raster',
            name='test_stream_4,test_lengthslope_4,test_stream_8,test_lengthslope_8')

    def test_OutputCreated(self):
        """Test to see if the outputs are created"""
        #run the watershed module
        self.assertModule('r.watershed', elevation='elevation',
            threshold='10000', accumulation='test_accumulation',
            drainage='test_drainage', basin='test_basin', stream='test_stream',
            half_basin='test_halfbasin', length_slope='test_lengthslope',
            slope_steepness='test_slopesteepness')
        #check to see if accumulation output is in mapset
        self.assertRasterExists('test_accumulation',
            msg='test_accumulation output was not created')
        #check to see if drainage output is in mapset
        self.assertRasterExists('test_drainage',
            msg='test_drainage output was not created')
        #check to see if basin output is in mapset
        self.assertRasterExists('test_basin',
            msg='test_basin output was not created')
        #check to see if stream output is in mapset
        self.assertRasterExists('test_stream',
            msg='test_stream output was not created')
        #check to see if half.basin output is in mapset
        self.assertRasterExists('test_halfbasin',
            msg='test_halfbasin output was not created')
        #check to see if length.slope output is in mapset
        self.assertRasterExists('test_lengthslope',
            msg='test_lengthslope output was not created')
        #check to see if slope.steepness output is in mapset
        self.assertRasterExists('test_slopesteepness',
            msg='test_slopesteepness output was not created')

    def test_fourFlag(self):
        """Test the -4 flag to see if the stream and slope lengths are
        approximately the same as the outputs from the default module run"""
        #Run module with default settings
        self.assertModule('r.watershed', elevation='elevation',
            threshold='10000', stream='test_stream_8',
            length_slope='test_lengthslope_8')
        #Run module with flag 4
        self.assertModule('r.watershed', flags='4', elevation='elevation',
            threshold='10000', stream='test_stream_4',
            length_slope='test_lengthslope_4')
        #Use the assertRastersNoDifference with precsion 10 to see if close
        #Compare stream output
        self.assertRastersNoDifference('test_stream_4', 'test_stream_8', 10)
        #Compare length_slope output
        self.assertRastersNoDifference('test_lengthslope_4',
            'test_lengthslope_8', 10)

    def test_watershedThreadholdfail(self):
        """Check to see if it will allow for a threshold of 0 or a negative"""
        self.assertModuleFail('r.watershed', elevation='elevation', threshold='0',
            stream='test_stream2', msg='Threshold value of 0 considered valid.')
        self.assertModuleFail('r.watershed', elevation='elevation',
            threshold='-1', stream='test_stream3',
            msg='Threshold value of 0 considered valid.')



if __name__ == '__main__':
    test()