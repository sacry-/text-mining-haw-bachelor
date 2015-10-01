


class Proxy():
  def __init__(self):
    self.a = "a"
    self.b = "b"

class Data():
  def __init__(self, proxy):
    self.a = proxy.a
    self.b = proxy.b

  def w00t(self):
    print("w00t")

class NYTimes(Data):
  def __init__(self, proxy):
    super(NYTimes, self).__init__(proxy)

  def is_valid(self):
    pass


p = Proxy()
n = NYTimes(p)

n.w00t()
n.whitelist()