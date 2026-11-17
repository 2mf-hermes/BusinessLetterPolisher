# Reconstructs the updater .cmd straight out of App.cs (string-literal order is the
# concatenation order) and actually runs it against a target folder whose path
# contains spaces -- the exact situation that produced "Windows 找不到 F:\\Program".
import io, os, re, shutil, subprocess, sys, tempfile

SRC = 'App.cs'
text = io.open(SRC, encoding='utf-8-sig', newline='').read()
start = text.index('string script = ')
end = text.index('File.WriteAllText(scriptPath', start)
region = re.sub(r'//[^\r\n]*', '', text[start:end])

ESCAPES = {'n': '\n', 'r': '\r', 't': '\t', '\\': '\\', '"': '"', '0': '\0'}


def read_literal(s, i):
    assert s[i] == '"'
    i += 1
    out = []
    while s[i] != '"':
        ch = s[i]
        if ch == '\\':
            i += 1
            out.append(ESCAPES[s[i]])
        else:
            out.append(ch)
        i += 1
    return ''.join(out), i + 1


def render(values):
    """Walk the C# expression: string literal -> text, identifier -> value."""
    out, i = [], 0
    while i < len(region):
        ch = region[i]
        if ch == '"':
            lit, i = read_literal(region, i)
            out.append(lit)
        elif ch.isalpha() or ch == '_':
            j = i
            while j < len(region) and (region[j].isalnum() or region[j] in '._()'):
                j += 1
            name = region[i:j]
            if name in values:
                out.append(values[name])
            elif name in ('string', 'script', 'Path', 'Process', 'GetCurrentProcess', 'Id'):
                pass
            i = j
        else:
            i += 1
    return ''.join(out)


def run_case(label, base):
    target = os.path.join(base, 'Program Files (Portable)', 'BusinessLetterPolisher')
    source = os.path.join(base, 'payload')
    temp_dir = os.path.join(base, 'BusinessLetterPolisherUpdate_test')
    logfile = os.path.join(base, 'blp-update-log.txt')
    for d in (target, source, temp_dir):
        os.makedirs(d, exist_ok=True)
    io.open(os.path.join(source, 'letter-polisher.html'), 'w', encoding='utf-8').write('new')
    io.open(os.path.join(source, 'version.json'), 'w', encoding='utf-8').write('{}')
    io.open(os.path.join(target, 'letter-polisher.html'), 'w', encoding='utf-8').write('old')
    # a real, harmless executable to prove `start "" "<path with spaces>\x.exe"` works
    shutil.copy(os.path.join(os.environ['SystemRoot'], 'System32', 'hostname.exe'),
                os.path.join(target, 'hostname.exe'))

    script = render({
        'exeDir': target,
        'payloadDir': source,
        'tempRoot': temp_dir,
        'updateLog': logfile,
        'exeName': 'hostname.exe',
        'Process.GetCurrentProcess().Id': '999999',   # never matches -> skip the wait
    })
    script_path = os.path.join(base, 'apply-update-test.cmd')
    io.open(script_path, 'w', encoding='mbcs', newline='').write(script)
    print('=== %s === generated script ===' % label)
    print(script.replace('\r\n', '\n').rstrip())

    # cmd /c with output redirected to a file: `start` hands its handles to the
    # launched process, so capturing pipes can block until that process exits.
    out_path = os.path.join(base, 'cmd-output.txt')
    with io.open(out_path, 'wb') as fh:
        proc = subprocess.Popen(['cmd', '/c', script_path], stdout=fh, stderr=subprocess.STDOUT)
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            print('  FAIL  cmd did not finish within 60s')
            print(io.open(out_path, encoding='utf-8', errors='replace').read())
            return False
    out = io.open(out_path, encoding='utf-8', errors='replace').read()
    log = io.open(logfile, encoding='utf-8', errors='replace').read() if os.path.exists(logfile) else ''

    checks = []
    # the final `del "%~f0"` makes cmd report "The batch file cannot be found."
    # once it runs out of script to read - expected, not a failure
    checks.append(('output has no path-splitting error',
                   not re.search(r'(找不到|not recognized|不是內部|command not found|invalid|無法)', out)))
    checks.append(('output only carries the expected self-delete notice',
                   all(('cannot be found' in l) or not l.strip() for l in out.splitlines())))
    checks.append(('robocopy copied the new payload file',
                   io.open(os.path.join(target, 'letter-polisher.html'), encoding='utf-8').read() == 'new'))
    checks.append(('robocopy copied version.json', os.path.exists(os.path.join(target, 'version.json'))))
    checks.append(('log records target as ONE unsplit path', ('target=' + target) in log))
    checks.append(('log records a robocopy exit code', 'robocopy exit=' in log))
    checks.append(('log records the relaunch path', 'relaunched "%s\\hostname.exe"' % target in log))
    checks.append(('temp dir removed', not os.path.isdir(temp_dir)))
    checks.append(('script deleted itself', not os.path.exists(script_path)))

    ok = True
    for name, good in checks:
        print(('  PASS  ' if good else '  FAIL  ') + name)
        ok = ok and good
    if not ok:
        print('--- log ---\n' + log)
        print('--- cmd output ---\n' + out)
    return ok


base = tempfile.mkdtemp(prefix='blp-test-')
ok1 = run_case('path WITH spaces', os.path.join(base, 'blp test'))
ok2 = run_case('path without spaces', os.path.join(base, 'blp-test'))
print('\nRESULT:', 'ALL PASS' if (ok1 and ok2) else 'FAILURES')
sys.exit(0 if (ok1 and ok2) else 1)
