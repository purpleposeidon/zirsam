

class BitBuffer:
  def __init__(self, fd, maxsize):
    """
      fd is file for reading/writing
      maxsize is what the maximum number of bits to be used is
      implementation should probably treat BitBuffer.read() == 0 as EOF?
    """
    self.fd = fd
    self.width = len('{0:b}'.format(maxsize)) #':b' formats as binary
    self.buffer = []
    
  def write(self, i):
    s = '{0:b}'.format(i).rjust(self.width, '0')
    if not (len(s) <= self.width):
      raise ValueError("Item is too large to write ({0})".format(s))
    self.buffer += [_ for _ in s]
    while len(self.buffer) >= 8:
      d = self.buffer[:8]
      del self.buffer[:8]
      d = ''.join(d)
      r = int(''.join(d), 2)
      self.fd.write(bytes([r]))
  def end(self):
    #Put on some trailing 0's
    self.buffer += ['0']*(8-len(self.buffer))
    self.write(0)
    #s = b''.join(self.buffer).ljust(self.width, '0')
    #s = bytes()
    #self.fd.write(bytes([int(s, 2)]))
      
  def read(self):
    while len(self.buffer) <= self.width:
      r = self.fd.read(1)
      if not r:
        raise EOFError
      c = ord(r)
      s = '{0:b}'.format(c).rjust(8, '0')
      self.buffer = self.buffer + [_ for _ in s]
    d = self.buffer[:self.width]
    d = ''.join(d)
    del self.buffer[:self.width]
    return int(d, 2)

if __name__ == '__main__':
  test = [237, 93, 125,1234,  890]
  #test = [5, 10, 15, 20]
  #test = [50, 2]
  macks = max(test)
  import io
  f = io.BytesIO()
  b = BitBuffer(f, macks)
  for t in test:
    b.write(t)
  b.end()
  #f.open()
  f.seek(0)
  c = BitBuffer(f, macks)
  for t in test:
    v = c.read()
    print(t, '-->', v)
    #assert t == v

