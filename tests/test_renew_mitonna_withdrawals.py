"""Offline causal tests. Never use the tracked policy as a test output."""
import hashlib
import importlib.util
import json
import multiprocessing
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('renew', ROOT/'tools/renew_mitonna_withdrawals.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
NOW = 1794800000

def worker(path, expected, start, results):
    start.wait()
    try:
        m.renew_file(Path(path), expected, now=lambda: NOW)
        results.put('ok')
    except ValueError:
        results.put('cas')

class RenewalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ['M20_TEST_TMPDIR'])
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'policy.json'
        self.old = json.loads((ROOT/'mitonna/retraits-recettes.json').read_bytes())
        self.old.update(sequence=7, issuedAt=NOW-86300, expiresAt=NOW+100, withdrawnIDs=['recipe:test-1'])
        self.path.write_text(json.dumps(self.old))
        self.sha = hashlib.sha256(self.path.read_bytes()).hexdigest()
    def renew(self):
        return m.renew_file(self.path, self.sha, now=lambda: NOW)
    def test_valid_policy_is_reissued_not_noop(self):
        new = self.renew()
        self.assertEqual((new['sequence'],new['issuedAt'],new['expiresAt']), (8,NOW,NOW+86400))
        for key in ('withdrawnIDs','manifestSHA256','schemaVersion','reason'):
            self.assertEqual(new[key],self.old[key])
        self.assertEqual(json.loads(self.path.read_bytes()),new)
    def test_expired_keeps_all_tombstones(self):
        self.old.update(issuedAt=NOW-86401,expiresAt=NOW-1)
        self.path.write_text(json.dumps(self.old)); self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
        self.assertEqual(self.renew()['withdrawnIDs'],self.old['withdrawnIDs'])
    def test_wrong_cas_preserves_bytes(self):
        old=self.path.read_bytes()
        with self.assertRaises(ValueError):m.renew_file(self.path,'0'*64,now=lambda:NOW)
        self.assertEqual(self.path.read_bytes(),old)
    def test_second_writer_cannot_reuse_old_cas(self):
        self.renew(); old=self.path.read_bytes()
        with self.assertRaises(ValueError):self.renew()
        self.assertEqual(self.path.read_bytes(),old)
    def test_concurrent_writers_exactly_one_wins(self):
        ctx=multiprocessing.get_context('fork'); start=ctx.Event(); results=ctx.Queue()
        procs=[ctx.Process(target=worker,args=(str(self.path),self.sha,start,results)) for _ in range(2)]
        for p in procs:p.start()
        start.set()
        for p in procs:p.join(5); self.assertEqual(p.exitcode,0)
        self.assertEqual(sorted(results.get(timeout=1) for _ in procs),['cas','ok'])
        results.close();results.join_thread()
        self.assertEqual(json.loads(self.path.read_bytes())['sequence'],8)
    def test_ttl_above_86400_rejected_not_normalized(self):
        self.old['expiresAt']=self.old['issuedAt']+86401
        self.path.write_text(json.dumps(self.old));self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
        old=self.path.read_bytes()
        with self.assertRaises(ValueError):self.renew()
        self.assertEqual(self.path.read_bytes(),old)
    def test_strict_schema_duplicate_fields_and_rollback(self):
        variants=[dict(self.old,sequence=True),dict(self.old,sequence=2147483647),dict(self.old,schemaVersion=2),dict(self.old,manifestSHA256='0'*64),dict(self.old,issuedAt=NOW+1,expiresAt=NOW+86400),dict(self.old,extra='x'),dict(self.old,withdrawnIDs=['x','x'])]
        for v in variants:
            with self.subTest(v=v):
                self.path.write_text(json.dumps(v)); self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
                with self.assertRaises(ValueError):self.renew()
        self.path.write_text(json.dumps(self.old).replace('"sequence": 7','"sequence": 7,"sequence": 7'))
        self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
        with self.assertRaises(ValueError):self.renew()
    def test_margin_has_six_hours_not_larger_ttl(self):
        self.assertEqual(m.RENEWAL_MARGIN,21600)
        self.assertTrue(m.due(self.old,NOW))
        self.assertFalse(m.due(dict(self.old,expiresAt=NOW+21601),NOW))
        self.assertTrue(m.due(dict(self.old,expiresAt=NOW+21600),NOW))
    def test_nzero_and_real_clock_injection(self):
        self.old['withdrawnIDs']=[];self.path.write_text(json.dumps(self.old));self.sha=hashlib.sha256(self.path.read_bytes()).hexdigest()
        called=[]
        def clock():called.append(True);return NOW
        new=m.renew_file(self.path,self.sha,now=clock)
        self.assertEqual(called,[True]);self.assertEqual(new['withdrawnIDs'],[])
    def test_symlink_refused(self):
        link=Path(self.temp.name)/'link.json';link.symlink_to(self.path)
        with self.assertRaises(ValueError):m.renew_file(link,self.sha,now=lambda:NOW)

if __name__=='__main__':unittest.main(verbosity=2)
