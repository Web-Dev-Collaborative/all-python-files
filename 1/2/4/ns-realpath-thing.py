import os,ctypes,struct,errno,sys

CLONE_NEWIPC = 0x08000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWNET = 0x40000000

start_uid = os.getuid()
start_gid = os.getgid()
    
c = ctypes.CDLL("libc.so.6", use_errno = True)

def drop_caps():
    c.capset(struct.pack("=Ii", 0x19980330, 0), "\x00" * 12)

def set_idmap():
    with open("/proc/self/uid_map", "w") as f:
        f.write("%d %d 1\n" % (start_uid, start_uid))
    try:
      with open("/proc/self/setgroups", "w") as f:
        f.write("deny")
    except IOError as e:
      if e.errno != errno.ENOENT:
        raise
    with open("/proc/self/gid_map", "w") as f:
        f.write("%d %d 1\n" % (start_gid, start_gid))

if c.unshare(CLONE_NEWNET | CLONE_NEWIPC) == -1:
    errno = ctypes.get_errno()
    raise OSError(errno, os.strerror(errno))
set_idmap()
drop_caps()

buf = "\x00" * 4096
if c.realpath(sys.argv[1], buf) == 0:
    errno = ctypes.get_errno()
    raise OSError(errno, os.strerror(errno))
print buf[:buf.index("\x00")]
