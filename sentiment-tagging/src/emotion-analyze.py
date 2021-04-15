import sys
import os
import text2emotion as te

sys.path.append(os.path.abspath("../lib"))
from analysis_helper import perform_analysis_tagging


perform_analysis_tagging("../../data-collection/data/complete_en_US.csv",
                         "../data/txt2emotion_stemmed_tagged.csv",
                         te.get_emotion,
                         ['Sad', 'Angry', 'Surprise', 'Fear', 'Happy'])
