"""
Name:       GRASS_rWatershed_UnitTest
Purpose:    This script is to demonstrate a unit test for GRASS's r.Watershed
            module for GIS582 at NCSU. This Unit Test must be placed in the
            directory testsuite of the GRASS installation.

Author:     Stephanie Wendel - sawendel
GRASS:      7.1.svn-r64925-36
Version:    1.1
Modified:   3/3/2015
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
            name='test_accumulation,test_basin')

    def test_OutputCreated(self):
        """Test to see if the outputs are created"""
        #run the watershed module
        self.assertModule('r.watershed', elevation='elevation',
            threshold='10000', accumulation='test_accumulation',
            basin='test_basin')
        #check to see if accumulation output is in mapset
        self.assertRasterExists('test_accumulation',
            msg='test_accumulation output was not created')
        self.assertRasterExists('test_basin',
            msg='test_basin output was not created')

if __name__ == '__main__':
    test()