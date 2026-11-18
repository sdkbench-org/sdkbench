"""Private Linux launcher. Standard library only, before any participant import.

Executed by absolute filename in isolated Python mode, not imported as a package.
Resource controls are inherited across exec/fork. Failure never executes the command.
"""
import ctypes
import errno
import json
import os
from pathlib import Path
import resource
import sys


def deny_network():
    library = ctypes.CDLL('libseccomp.so.2', use_errno=True)
    library.seccomp_init.argtypes = [ctypes.c_uint32]
    library.seccomp_init.restype = ctypes.c_void_p
    library.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    library.seccomp_syscall_resolve_name.restype = ctypes.c_int
    library.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    library.seccomp_rule_add.restype = ctypes.c_int
    library.seccomp_load.argtypes = [ctypes.c_void_p]
    library.seccomp_load.restype = ctypes.c_int
    library.seccomp_release.argtypes = [ctypes.c_void_p]
    context = library.seccomp_init(0x7fff0000)  # SCMP_ACT_ALLOW
    if not context:raise OSError('Cannot initialize seccomp')
    try:
        denied = ['socket', 'socketpair', 'connect', 'bind', 'listen', 'accept', 'accept4',
                  'sendto', 'sendmsg', 'sendmmsg', 'recvfrom', 'recvmsg', 'recvmmsg',
                  'io_uring_setup', 'io_uring_enter', 'io_uring_register', 'setns', 'unshare',
                  'ptrace', 'process_vm_writev', 'bpf']
        for name in denied:
            number = library.seccomp_syscall_resolve_name(name.encode())
            if number < 0:raise OSError('Unresolved required syscall: ' + name)
            if library.seccomp_rule_add(context, 0x00050000 | errno.EPERM, number, 0) != 0:
                raise OSError('Cannot install syscall restriction: ' + name)
        # libseccomp sets no_new_privs before loading the filter.
        if library.seccomp_load(context) != 0:raise OSError('Cannot enforce seccomp network policy')
    finally:library.seccomp_release(context)


def main():
    config = json.loads(Path(sys.argv[1]).read_text())
    ready = int(sys.argv[2])
    try:
        Path(config['cgroup'], 'cgroup.procs').write_text(str(os.getpid()))
        os.sched_setaffinity(0, {config['cpu']})
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_FSIZE, (config['file_bytes'], config['file_bytes']))
        os.chdir(config['cwd'])
        deny_network()
        os.write(ready, b'ready\n'); os.close(ready)
        os.execvpe(config['argv'][0], config['argv'], config['environment'])
    except BaseException as exc:
        os.write(2, ('P0 isolation setup failed: ' + str(exc) + '\n').encode())
        os._exit(125)


if __name__ == '__main__':main()
