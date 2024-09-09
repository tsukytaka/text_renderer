from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np
from text_renderer.utils.errors import PanicError
from text_renderer.utils.utils import load_chars_file, random_choice

from .corpus import Corpus, CorpusCfg


@dataclass
class RandRegexCorpusCfg(CorpusCfg):
    length: Tuple[int, int] = (5, 10)
    chars_file: Path = None
    filter_font: bool = False
    filter_font_min_support_chars: int = 100


class RandRegexCorpus(Corpus):

    def __init__(self, cfg: "CorpusCfg"):
        super().__init__(cfg)

        self.cfg: RandRegexCorpusCfg
        if self.cfg.chars_file is None or not self.cfg.chars_file.exists():
            raise PanicError(f"chars_file not exists: {self.cfg.chars_file}")

        self.chars = list(load_chars_file(self.cfg.chars_file))

        self.font_manager.update_font_support_chars(self.cfg.chars_file)
        if self.cfg.filter_font:
            self.font_manager.filter_font_path(self.cfg.filter_font_min_support_chars)

    def get_text(self):
        chars = self.chars
        chars.sort(reverse=True)
        length = np.random.randint(*self.cfg.length)
        head_length = np.random.randint(1,3)
        tail_length = np.random.randint(1,4)
        body_length = 0
        if length > head_length:
            body_length = length - head_length
        head_chars = chars[:26]
        tail_chars = chars[26:36]
        body_chars = chars[26:]
        print("head_chars: ", head_chars)
        print("body_chars: ", body_chars)
        print("length: ", length)
        print("head_length: ", head_length)
        print("body_length: ", body_length)
        head_text = "".join(random_choice(head_chars, head_length))
        tail_text = "".join(random_choice(tail_chars, tail_length))
        body_text = "".join(random_choice(body_chars, body_length))
        print("head_text: ", head_text)
        print("body_text: ", body_text)
        text = head_text + body_text + tail_text
        print("text: ", text)
        return text
