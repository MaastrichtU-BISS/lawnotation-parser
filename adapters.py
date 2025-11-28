from abc import ABC, abstractmethod
import re
import copy
import random
import string

class Adapter(ABC):

    def __init__(self, full_text):
        self.full_text = full_text 
    
    @abstractmethod
    def convert(self, annotations):
        pass
    
class Gpt2Lawnotation(Adapter):
    
   def convert(self, annotations):
      converted_annotations = []
      repetitions = None
      for ann in annotations:
          if not 'start' in ann or not 'end' in ann:
            text = ann['text']
            label = ann['label']
            indices = self.find_text(text)
            if len(indices) > 1:
                if repetitions is None:
                    repetitions = []
                repetitions.append({
                    'label': label,
                    'text': text,
                    'occurrences': len(indices),
                })
            for idx in indices:
                new_ann = copy.deepcopy(ann)
                new_ann['start'] = idx[0]
                new_ann['end'] = idx[1]
                new_ann['ls_id'] = ''.join(random.choices(string.ascii_letters, k=10))
                converted_annotations.append(new_ann)
          else:
              converted_annotations.append(copy.deepcopy(ann))
      return converted_annotations, repetitions

   @abstractmethod
   def find_text(self, text):
       pass

class Gpt2LawnotationAll(Gpt2Lawnotation):
    
   def __init__(self, full_text):
       super().__init__(full_text)
       self.__unique_text = set()
   
   def find_text(self, text):
        escaped = re.escape(text)
        if text in self.__unique_text:
            return []
        self.__unique_text.add(escaped)
        return [(m.start(), m.end()) for m in re.finditer(escaped, self.full_text)]

# Use this adapter when you are sure each annotations will have at most one match in the assignment's text.
class Gpt2LawnotationFirst(Gpt2Lawnotation):
    
    def __init__(self, full_text):
        super().__init__(full_text)
    
    def find_text(self, text):
        escaped = re.escape(text)
        m = re.search(escaped, self.full_text)
        if m:
            return [(m.start(), m.end())]
        return []


