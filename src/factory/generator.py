"""Font generator"""

from os import path


class Generator(object):
    """Subclass to modify font metadata and generate font file"""

    MANUFACTURE = "Trần Đức Nam (aka. Dynamo, me@dynamotn.dev)"
    COPYRIGHT = (
        " Programming ligatures added by "
        + MANUFACTURE
        + " from FiraCode."
        + " FiraCode Copyright Ⓒ 2015 by Nikita Prokopov"
    )
    VERSION = "v1.18.0"

    def __init__(self, base_font):
        """
        Args:
            base_font: (FontForge's font object) Base font to create new font
        """
        self.base_font = base_font

    def replace_sfnt(self, key, value):
        """Replace value of a key in SFNT metadata of base font to new value"""
        self.base_font.sfnt_names = tuple(
            (row[0], key, value) if row[1] == key else row
            for row in self.base_font.sfnt_names
        )

    def update_font_metadata(self, prefix, name, suffix):
        """Update font metadata with new name

        Args:
            prefix: (string) Prefix of font name
            name: (string) Font's family name
            suffix: (string) Suffix of font name
        """
        old_name = self.base_font.familyname
        if name:
            self.base_font.familyname = name
        new_name = self.base_font.familyname
        self.base_font.fullname = ("%s %s %s" % (prefix, new_name, suffix)).strip()
        self.base_font.fontname = "%s" % (self.base_font.fullname.replace(" ", ""))

        print(
            "Based on font %s (%s) to generate '%s'"
            % (old_name, path.basename(self.base_font.path), new_name)
        )

        self.base_font.copyright += Generator.COPYRIGHT
        self.replace_sfnt("UniqueID", "%s" % self.base_font.fullname)
        self.replace_sfnt("Preferred Family", new_name)
        self.replace_sfnt("Compatible Full", new_name)
        self.replace_sfnt("Family", new_name)
        self.replace_sfnt("WWS Family", new_name)
        self.replace_sfnt("Version", Generator.VERSION)

    def generate(self, directory):
        """Generate new font from base font

        Args:
            directory: (string) Path of directory to generate file
        """
        # Generate font type (TTF or OTF) corresponding to input font extension
        if self.base_font.path[-4:].lower() == ".otf":
            output_font_type = ".otf"
        else:
            output_font_type = ".ttf"

        # Generate font & move to output directory
        output_font_file = path.join(
            directory,
            self.base_font.fullname.lower().replace(" ", "-") + output_font_type,
        )
        print(
            "Generating %s font to '%s'" % (self.base_font.fullname, output_font_file)
        )
        self.base_font.generate(output_font_file)
