# encoding: utf-8
# Copyright (C) 2016 John Törnblom

import unittest
import xtuml
import bridgepoint

class TestRelateUnrelate(unittest.TestCase):
    '''
    Test suite for xtuml relate/unrelate operations
    '''
    def setUp(self):
        self.m = bridgepoint.load_metamodel()

    def tearDown(self):
        del self.m

    def test_relate(self):
        s_edt = self.m.new('S_EDT')
        s_dt = self.m.new('S_DT')
        pe_pe = self.m.new('PE_PE')
        self.assertTrue(xtuml.relate(s_dt, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_dt, s_edt, 17))
        self.assertEqual(s_edt, xtuml.navigate_one(s_dt).S_EDT[17]())

    def test_relate_reflexive_one_to_other(self):
        inst1 = self.m.new('ACT_SMT')
        inst2 = self.m.new('ACT_SMT')
        act_blk = self.m.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        self.assertTrue(xtuml.relate(inst1, inst2, 661, 'precedes'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
    def test_relate_reflexive_other_to_one(self):
        inst1 = self.m.new('ACT_SMT')
        inst2 = self.m.new('ACT_SMT')
        act_blk = self.m.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, inst1, 661, 'succeeds'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
    def test_relate_reflexive_without_phrase(self):
        inst1 = self.m.new('ACT_SMT')
        inst2 = self.m.new('ACT_SMT')
        
        self.assertRaises(xtuml.RelateException, xtuml.relate,
                          inst1, inst2, 661, '<invalid phrase>')
        
    def test_relate_inverted_order(self):
        s_edt = self.m.new('S_EDT')
        s_dt = self.m.new('S_DT')
        pe_pe = self.m.new('PE_PE')
        self.assertTrue(xtuml.relate(pe_pe, s_dt, 8001))
        self.assertTrue(xtuml.relate(s_edt, s_dt, 17))
        self.assertEqual(s_edt, xtuml.navigate_one(s_dt).S_EDT[17]())
    
    def test_relate_invalid_relid(self):
        s_edt = self.m.new('S_EDT')
        s_dt = self.m.new('S_DT')
        self.assertRaises(xtuml.UnknownLinkException, xtuml.relate, s_edt, s_dt, 0)
        
    def test_unrelate(self):
        inst1 = self.m.new('ACT_SMT')
        inst2 = self.m.new('ACT_SMT')
        act_blk = self.m.new('ACT_BLK')

        self.assertTrue(xtuml.relate(inst1, act_blk, 602))
        self.assertTrue(xtuml.relate(inst2, act_blk, 602))
        
        self.assertTrue(xtuml.relate(inst1, inst2, 661, 'precedes'))
        self.assertEqual(inst2, xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
        self.assertEqual(inst1, xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        
        self.assertTrue(xtuml.unrelate(inst1, inst2, 661, 'precedes'))
        self.assertIsNone(xtuml.navigate_one(inst2).ACT_SMT[661, 'precedes']())
        self.assertIsNone(xtuml.navigate_one(inst1).ACT_SMT[661, 'succeeds']())
            
    def test_relate_in_wrong_order(self):
        s_ee = self.m.new('S_EE')
        pe_pe = self.m.new('PE_PE')
        EE_ID = s_ee.EE_ID
        Element_ID = pe_pe.Element_ID
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertNotEqual(EE_ID, s_ee.EE_ID)
        self.assertEqual(Element_ID, pe_pe.Element_ID)

    def test_relate_top_down(self):
        s_dt = self.m.select_one('S_DT', xtuml.where_eq(Name='string'))
        s_bparm = self.m.new('S_BPARM', Name='My_Parameter')
        s_ee = self.m.new('S_EE', Name='My_External_Entity', Key_Lett='My_External_Entity')
        pe_pe = self.m.new('PE_PE', Visibility=True, type=5)
        s_brg = self.m.new('S_BRG', Name='My_Bridge_Operation')

        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_brg, s_ee, 19))
        self.assertTrue(xtuml.relate(s_brg, s_dt, 20))
        self.assertTrue(xtuml.relate(s_bparm, s_brg, 21))
        self.assertTrue(xtuml.relate(s_bparm, s_dt, 22))
            
        inst = xtuml.navigate_any(pe_pe).S_EE[8001].S_BRG[19].S_BPARM[21]()
        self.assertEqual(inst, s_bparm)
        
    def test_relate_bottom_up(self):
        s_dt = self.m.select_one('S_DT', xtuml.where_eq(Name='string'))
        s_bparm = self.m.new('S_BPARM', Name='My_Parameter')
        s_ee = self.m.new('S_EE', Name='My_External_Entity', Key_Lett='My_External_Entity')
        pe_pe = self.m.new('PE_PE', Visibility=True, type=5)
        s_brg = self.m.new('S_BRG', Name='My_Bridge_Operation')
        
        self.assertTrue(xtuml.relate(s_bparm, s_dt, 22))
        self.assertTrue(xtuml.relate(s_bparm, s_brg, 21))
        self.assertTrue(xtuml.relate(s_brg, s_dt, 20))
        self.assertTrue(xtuml.relate(s_ee, pe_pe, 8001))
        self.assertTrue(xtuml.relate(s_brg, s_ee, 19))
        
        inst = xtuml.navigate_any(pe_pe).S_EE[8001].S_BRG[19].S_BPARM[21]()
        self.assertEqual(inst, s_bparm)


        
if __name__ == "__main__":
    unittest.main()
