import re
from typing import List, Optional
from bs4 import BeautifulSoup
from bs4.element import Tag

def parse_list(html: str, regexp, tag: str='a') -> List[str]:
  def is_valid_tag(x):
    if x.name != tag:
      return False
    if regexp is None:
      return True

    return True in [bool(re.match(regexp, content)) for content in x.contents]

  soup = BeautifulSoup(html, 'html.parser')
  buckets = soup.find_all(is_valid_tag)
  return [bucket.contents[0] for bucket in buckets]
  