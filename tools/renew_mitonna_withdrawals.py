"""Local-only renewal of an existing trusted policy. No network or scheduler.

All participating local writers must use this lock. Remote publication still
requires the site owner's separately qualified route and a remote ref CAS.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import time

LOT = '571a388192d35158ab8032a55a15956ac7280b542c5c6d99e687bab01c92f952'
MAX_BYTES = 32768
MAX_SEQUENCE = 2147483647
TTL = 86400
RENEWAL_MARGIN = 21600
KEYS = {'schemaVersion','manifestSHA256','sequence','issuedAt','expiresAt','withdrawnIDs','reason'}
REASONS = {'safety','rights','quality','operator'}

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result

def validate(data, now):
    if len(data) > MAX_BYTES:
        raise ValueError('policy too large')
    try:
        value = json.loads(data.decode('utf-8'), object_pairs_hook=unique_object)
    except (ValueError, UnicodeError) as exc:
        raise ValueError('invalid JSON') from exc
    if type(value) is not dict or set(value) != KEYS:
        raise ValueError('strict seven-key policy required')
    if type(value['schemaVersion']) is not int or value['schemaVersion'] != 1 or value['manifestSHA256'] != LOT:
        raise ValueError('schema/manifest mismatch')
    for key in ('sequence','issuedAt','expiresAt'):
        if type(value[key]) is not int:
            raise ValueError('integer required')
    if not 1 <= value['sequence'] <= MAX_SEQUENCE:
        raise ValueError('sequence range')
    if not 0 <= value['issuedAt'] <= min(now,4102444800):
        raise ValueError('clock rollback or future issuance')
    if not value['issuedAt'] < value['expiresAt'] <= value['issuedAt'] + TTL:
        raise ValueError('TTL above 86400 or invalid expiry')
    ids = value['withdrawnIDs']
    if type(ids) is not list or len(ids) > 296 or any(type(i) is not str or not re.fullmatch(r'[A-Za-z0-9._:-]+',i,re.ASCII) for i in ids):
        raise ValueError('invalid IDs')
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate IDs')
    if type(value['reason']) is not str or value['reason'] not in REASONS:
        raise ValueError('invalid reason')
    return value

def due(policy, now):
    """Advisory only. No scheduler is installed or activated by this module."""
    return now >= policy['expiresAt'] - RENEWAL_MARGIN

def read_regular(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ValueError('regular non-symlink policy required') from exc
    with os.fdopen(fd,'rb') as source:
        if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
            raise ValueError('regular file required')
        return source.read(MAX_BYTES + 1)

def renew_file(path, expected_sha256, *, now=None):
    """Explicit renewal, even if valid: issue now, sequence+1, fixed 24h TTL.

    Existing tombstones/order/reason/manifest/schema are copied, not replaced
    by N=0. IDs must come from a previously consumer-qualified trusted policy;
    this renewal tool intentionally cannot add IDs or establish their origin.
    """
    path = Path(path)
    if not re.fullmatch(r'[0-9a-f]{64}',expected_sha256):
        raise ValueError('expected SHA256 required')
    # Stable sidecar inode: never unlink a lock that another writer may hold.
    lock = path.with_name('.' + path.name + '.renew.lock')
    try:
        fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    except OSError as exc:
        raise ValueError('unsafe lock') from exc
    with os.fdopen(fd,'a+b') as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise ValueError('unsafe lock')
        fcntl.flock(handle,fcntl.LOCK_EX)
        original = read_regular(path)
        if hashlib.sha256(original).hexdigest() != expected_sha256:
            raise ValueError('CAS conflict: re-read current policy, do not retry blindly')
        timestamp = int(time.time()) if now is None else now()
        if type(timestamp) is not int or not 0 <= timestamp <= 4102444800:
            raise ValueError('invalid current time')
        previous = validate(original,timestamp)
        if previous['sequence'] == MAX_SEQUENCE:
            raise ValueError('sequence exhausted, no reset allowed')
        value = dict(previous,sequence=previous['sequence']+1,issuedAt=timestamp,expiresAt=timestamp+TTL)
        payload = (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
        validate(payload,timestamp)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.withdrawal-renew-',delete=False) as output:
                temporary = output.name
                os.fchmod(output.fileno(),0o644)
                output.write(payload); output.flush(); os.fsync(output.fileno())
            if read_regular(path) != original:
                raise ValueError('CAS conflict before replace')
            os.replace(temporary,path)
            temporary = None
            directory = os.open(path.parent,os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if temporary is not None:
                os.unlink(temporary)
        return value

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy',type=Path,required=True,help='local working-copy policy, never a URL')
    parser.add_argument('--expected-sha256',required=True)
    parser.add_argument('--check-due',action='store_true',help='read-only; exit 3 if within six hours or expired')
    args = parser.parse_args()
    if args.check_due:
        data = read_regular(args.policy)
        if hashlib.sha256(data).hexdigest() != args.expected_sha256:
            raise ValueError('CAS conflict')
        timestamp = int(time.time())
        value = validate(data,timestamp)
        status = due(value,timestamp)
        print('DUE' if status else 'NOT_DUE')
        return 3 if status else 0
    value = renew_file(args.policy,args.expected_sha256)
    print('LOCAL ONLY: sequence',value['sequence'],'issuedAt',value['issuedAt'],'expiresAt',value['expiresAt'])
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
