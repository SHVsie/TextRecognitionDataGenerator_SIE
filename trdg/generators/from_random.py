import os

from .from_strings import GeneratorFromStrings
from ..data_generator import FakeTextDataGenerator
from ..string_generator import create_strings_randomly
from ..utils import load_dict, load_fonts


class GeneratorFromRandom:
    """Generator that uses randomly generated words"""

    def __init__(
            self,
            count=-1,
            length=1,
            allow_variable=False,
            use_letters=True,
            use_numbers=True,
            use_symbols=True,
            fonts=[],
            language="en",
            size=32,
            skewing_angle=0,
            random_skew=False,
            blur=0,
            random_blur=False,
            background_type=0,
            distorsion_type=0,
            distorsion_orientation=0,
            is_handwritten=False,
            width=-1,
            height=-1,
            alignment=1,
            text_color="#282828",
            orientation=0,
            space_width=1.0,
            character_spacing=0,
            margins=(5, 5, 5, 5),
            fit=False,
            output_mask=False,
            word_split=False,
            image_dir=os.path.join(
                "..", os.path.split(os.path.realpath(__file__))[0], "images"
            ),
            stroke_width=0,
            stroke_fill="#282828",
            image_mode="RGB",
            output_bboxes=0,
    ):
        self.generated_count = 0
        self.count = count
        self.length = length
        self.allow_variable = allow_variable
        self.use_letters = use_letters
        self.use_numbers = use_numbers
        self.use_symbols = use_symbols
        self.language = language

        self.batch_size = min(max(count, 1), 1000)
        self.steps_until_regeneration = self.batch_size
        self.generator = GeneratorFromStrings(
            create_strings_randomly(
                self.length,
                self.allow_variable,
                self.batch_size,
                self.use_letters,
                self.use_numbers,
                self.use_symbols,
                self.language,
            ),
            count,
            fonts if len(fonts) else load_fonts(language),
            language,
            size,
            skewing_angle,
            random_skew,
            blur,
            random_blur,
            background_type,
            distorsion_type,
            distorsion_orientation,
            is_handwritten,
            width,
            height,
            alignment,
            text_color,
            orientation,
            space_width,
            character_spacing,
            margins,
            fit,
            output_mask,
            word_split,
            image_dir,
            stroke_width,
            stroke_fill,
            image_mode,
            output_bboxes,
        )

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated_count == self.count:
            raise StopIteration
        self.generated_count += 1
        return self.next()

    def next(self):
        if self.generator.generated_count >= self.steps_until_regeneration:
            self.generator.strings = create_strings_randomly(
                self.length,
                self.allow_variable,
                self.batch_size,
                self.use_letters,
                self.use_numbers,
                self.use_symbols,
                self.language,
            )
            self.steps_until_regeneration += self.batch_size
        return self.generator.next()
