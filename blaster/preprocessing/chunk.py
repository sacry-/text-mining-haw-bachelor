class Chunk():

  def __init__(self, a):
    self.a = a
    self.index = a._index
    self.id = a.meta.id
    self.title = a.title
    self.text = a.text
    self.article_html = a.article_html

  def update_article(self):
    self.a.preprocessed = True
    self.a.save()