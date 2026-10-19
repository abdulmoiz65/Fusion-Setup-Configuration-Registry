"""Bounded local intake; extracted content is data, not executable instructions.

Returns ephemeral text/provenance only. No model invocation, file writes, macros,
network, PDF OCR or invented Office reader. Python3.11+.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import selectors
import shutil
import signal
import stat
import subprocess
import time

MAX_BYTES = 5 * 1024 * 1024


def capabilities():
    return {"text": True, "csv": True, "pdf_text": bool(shutil.which("pdftotext")),
            "xlsx": False, "office_documents": False, "presentations": False, "image_ocr": False}


def _read_file(path):
    """Open once without following a final symlink, then enforce the byte bound.

    The descriptor's type/size, not an earlier pathname stat, is authoritative.
    O_NONBLOCK prevents a swapped-in FIFO from blocking before the regular-file
    check. Reading MAX_BYTES+1 also bounds a file that grows after fstat.
    """
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_BYTES:
                raise ValueError("Expected nonempty regular file up to5MiB, not symlink")
            content = stream.read(MAX_BYTES + 1)
    except OSError:
        raise ValueError("Local intake file could not be opened safely") from None
    if not 0 < len(content) <= MAX_BYTES:
        raise ValueError("File changed beyond intake bound")
    return content


def _pdf_bytes(content, command, timeout):
    """Stream bounded stdin/stdout through installed pdftotext, never a shell.

    stderr is discarded, not accumulated or echoed. stdout is drained alongside
    stdin to prevent pipe deadlock, retaining at most MAX_BYTES+1 bytes. Timeout
    and output-limit failures kill the reader process group and reap it.
    """
    started = time.monotonic()
    process = None
    try:
        process = subprocess.Popen([command, "-layout", "-", "-"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, bufsize=0,
                                   start_new_session=True)
        output = bytearray()
        offset = 0
        with selectors.DefaultSelector() as selector:
            for stream, event, label in ((process.stdin, selectors.EVENT_WRITE, "input"),
                                         (process.stdout, selectors.EVENT_READ, "output")):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, event, label)
            while selector.get_map():
                remaining = timeout - (time.monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError
                for key, _ in selector.select(remaining):
                    if time.monotonic() - started >= timeout:
                        raise TimeoutError
                    if key.data == "input":
                        try:
                            count = os.write(key.fd, content[offset:offset + 65536])
                        except BlockingIOError:
                            continue
                        except BrokenPipeError:
                            count = 0
                        offset += count
                        if count == 0 or offset == len(content):
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                    else:
                        try:
                            chunk = os.read(key.fd, min(65536, MAX_BYTES - len(output) + 1))
                        except BlockingIOError:
                            continue
                        if not chunk:
                            selector.unregister(key.fileobj)
                            key.fileobj.close()
                        else:
                            output.extend(chunk)
                            if len(output) > MAX_BYTES:
                                raise ValueError("PDF extracted text exceeds bound")
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError
        if process.wait(timeout=remaining):
            raise ValueError("PDF is unreadable/protected")
        return bytes(output)
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("PDF reader failed or timed out; provide a readable export") from None
    finally:
        if process is not None:
            if process.poll() is None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
            for stream in (process.stdin, process.stdout):
                if stream is not None:
                    stream.close()


def extract(path, *, timeout=30):
    """Read the explicitly supplied local file; callers must not journal contents."""
    path = Path(path)
    if type(timeout) is not int or not 1 <= timeout <= 60:
        raise ValueError("Reader timeout must be1..60 seconds")
    suffix = path.suffix.lower()
    if suffix not in {".txt", ".md", ".csv", ".pdf"}:
        raise ValueError("No verified reader for this format; provide UTF-8 text/CSV or a text PDF")
    content = _read_file(path)
    if suffix in {".txt", ".md", ".csv"}:
        try:
            text = content.decode("utf-8-sig")
        except UnicodeError:
            raise ValueError("Unreadable UTF-8; provide a supported export") from None
        units = [{"line": n, "text": line} for n, line in enumerate(text.splitlines(), 1)]
        reader = "utf8_text"
    elif suffix == ".pdf":
        command = shutil.which("pdftotext")
        if not command:
            raise ValueError("Supported installed pdftotext runtime unavailable")
        try:
            text = _pdf_bytes(content, command, timeout).decode("utf-8")
        except UnicodeError:
            raise ValueError("PDF output encoding unsupported") from None
        units = [{"page": n, "text": page} for n, page in enumerate(text.split("\f"), 1) if page.strip()]
        reader = "installed_pdftotext"
    if not text.strip() or "\x00" in text:
        raise ValueError("No reliable text extracted; scanned images require a supported OCR route")
    return {"filename": path.name, "sha256": hashlib.sha256(content).hexdigest(),
            "reader": reader, "units": units, "status": "extracted_not_interpreted",
            "instructions_are_data": True, "write_eligible": False,
            "limitations": ["Extraction does not verify ownership, people or layout interpretation",
                            "Do not persist real roster or sensitive extracted contents in project records"]}
