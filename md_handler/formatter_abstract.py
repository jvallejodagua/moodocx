class FormatterAbstract:

    def __init__(self):
        '''
        General regex
        '''
        # Simple regex
        self.numeral_character = r'\b\d{1,3}\b'
        self.space_but_new_line = r'[^\S\n]+'
        self.optional_space_but_new_line = r'[^\S\n]*'
        self.new_line = r'[^\S \t\r\f\v]+'
        self.punctuation_separator = r'[\.\)]'
        self.accent_mark = r'[*]*'
        self.literal_A_character = r'\b[aA]\b'
        self.literal_B_character = r'\b[bB]\b'
        self.literal_C_character = r'\b[cC]\b'
        self.literal_D_character = r'\b[dD]\b'
        self.soft_new_line = r'\\\n'
        self.pandoc_comment_raw = r'<!-- -->'
        self.worng_italic_mark = r'\*{3}'
        self.worng_bold_mark = r'\*{4}'
        self.comment_mark = r'^>'
        self.escaped_underline = r'\\_'
        self.open_bracket = r'\['
        self.close_bracket = r'\]'
        self.open_braces = r'\{'
        self.closed_braces = r'\}'
        # Dotall
        self.one_line_dotall = r'[^\n]+'
        self.multiline_dotall = r'.+?'
        # self.last_added_text = rf'.+?(?=\n{self.pandoc_comment_raw}\n)'
        self.last_added_text = (
            rf'{self.multiline_dotall}(?={self.accent_mark}'
            rf'{self.numeral_character}'
            rf'{self.punctuation_separator}{self.accent_mark}'
            rf'{self.space_but_new_line}{self.accent_mark}'
            rf'{self.one_line_dotall}'
            rf'|\Z)'
        )
        #rf'.*?(?=\n{self.optional_space_but_new_line}{self.accent_mark}'

        self.pandoc_comment = rf'\n{self.pandoc_comment_raw}\n'
        self.end_document = r'\Z'
        
        # Multiline 
        self.raw_chunk_multiline = r'.+?'
        self.to_end_chunk_multiline = r'.*$'
        
        # No Flags
        self.bracket_mark = r'\[(.+?)\]\{.+?\}'
        self.code_block_pattern = (
            rf'```[\s\S]*?```\s*|'
            rf'{self.pandoc_comment_raw}'
        )
        self.windows_r_chars = r'\r'
        
        self.any_literal = (
            rf'(?:\b[aAbBcCdD]\b)'
            rf'{self.punctuation_separator}'
        )

        # Output regex
        self.output_punctuation = r'. '
        self.simple_new_line = r'\n'
        self.md_newline = r'\n\n'
        self.italic_mark = '*'
        self.bold_mark = '**'
        self.underline = r'_'
        
        '''
        Regex dictionary keys
        '''
        self.accent_mark_numeral_key = "accent_mark_numeral"
        self.numeral_search_key = "numeral_search"
        self.accent_mark_post_numeral_key = "accent_mark_post_numeral"
        self.punctuation_numeral_key = "punctuation_numeral"
        self.empty_space_numeral_key = "empty_space_numeral"
        self.accent_prompt_key = "accent_prompt"
        self.prompt_key = "prompt"
        self.added_prompt_text_key = "added_prompt_text"
        self.new_line_A_key = "literal_A_new_line"
        self.accent_mark_A_key = "accent_mark_A"
        self.literal_A_key = "literal_A"
        self.punctuation_separator_A_key = "punctuation_separator_A"
        self.empty_space_A_key = "empty_space_A"
        self.option_A_key = "option_A"
        self.added_option_A_key = "added_option_A"
        self.new_line_B_key = "literal_B_new_line"
        self.accent_mark_B_key = "accent_mark_B"
        self.literal_B_key = "literal_B"
        self.punctuation_separator_B_key = "punctuation_separator_B"
        self.empty_space_B_key = "empty_space_B"
        self.option_B_key = "option_B"
        self.added_option_B_key = "added_option_B"
        self.new_line_C_key = "literal_C_new_line"
        self.accent_mark_C_key = "accent_mark_C"
        self.literal_C_key = "literal_C"
        self.punctuation_separator_C_key = "punctuation_separator_C"
        self.empty_space_C_key = "empty_space_C"
        self.option_C_key = "option_C"
        self.added_option_C_key = "added_option_C"
        self.new_line_D_key = "literal_D_new_line"
        self.accent_mark_D_key = "accent_mark_D"
        self.literal_D_key = "literal_D"
        self.punctuation_separator_D_key = "punctuation_separator_D"
        self.empty_space_D_key = "empty_space_D"
        self.option_D_key = "option_D"
        self.added_option_D_key = "added_option_D"
        self.pandoc_comment_key = "pandoc_comment"
        
        '''
        Single line numerals Template
        '''
        # Single line numerals regex
        self.single_line_pattern = {
            self.accent_mark_numeral_key : self.accent_mark,
            self.numeral_search_key : self.numeral_character,
            self.accent_mark_post_numeral_key : self.accent_mark,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.empty_space_numeral_key : self.space_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.raw_chunk_multiline,
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_but_new_line,
            self.option_A_key : self.raw_chunk_multiline,
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_but_new_line,
            self.option_B_key : self.raw_chunk_multiline,
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_but_new_line,
            self.option_C_key : self.raw_chunk_multiline,
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_but_new_line,
            self.option_D_key : self.to_end_chunk_multiline
        }
        # Single line formatted question pattern
        self.ouput_single_line_order = self.build_search_pattern(
            rf'\g<{self.numeral_search_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_numeral_key}>',
            rf'\g<{self.accent_mark_post_numeral_key}>',
            rf'\g<{self.accent_prompt_key}>',
            rf'\g<{self.prompt_key}>\n\n',
            rf'\g<{self.literal_A_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_A_key}>',
            rf'\g<{self.option_A_key}>\n\n',
            rf'\g<{self.literal_B_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_B_key}>',
            rf'\g<{self.option_B_key}>\n\n',
            rf'\g<{self.literal_C_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_C_key}>',
            rf'\g<{self.option_C_key}>\n\n',
            rf'\g<{self.literal_D_key}>',
            self.output_punctuation,
            rf'\g<{self.accent_mark_D_key}>',
            rf'\g<{self.option_D_key}>\n\n',
            rf'{self.pandoc_comment_raw}',
        )

        '''
        Multiline numerals
        '''
        # Multiline numerals regex
        self.multiline_pattern = {
            self.accent_mark_numeral_key : self.accent_mark,
            self.numeral_search_key : self.numeral_character,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.accent_mark_post_numeral_key : self.accent_mark,
            self.empty_space_numeral_key : self.space_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.one_line_dotall,
            self.added_prompt_text_key : self.get_interine_text(self.literal_A_character),
            self.new_line_A_key : self.new_line,
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_but_new_line,
            self.option_A_key : self.one_line_dotall,
            self.added_option_A_key : self.get_interine_text(self.literal_B_character),
            self.new_line_B_key : self.new_line,
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_but_new_line,
            self.option_B_key : self.one_line_dotall,
            self.added_option_B_key : self.get_interine_text(self.literal_C_character),
            self.new_line_C_key : self.new_line,
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_but_new_line,
            self.option_C_key : self.one_line_dotall,
            self.added_option_C_key : self.get_interine_text(self.literal_D_character),
            self.new_line_D_key : self.new_line,
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_but_new_line,
            self.option_D_key : self.one_line_dotall,
            self.added_option_D_key : self.last_added_text
            #self.pandoc_comment_key : self.pandoc_comment,
        }

        # Multiple line formatted question pattern
        self.ouput_multiline_order = self.build_search_pattern(
            # rf'\g<{self.numeral_search_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_prompt_key}>',
            # rf'\g<{self.prompt_key}>',
            # rf'\g<{self.added_prompt_text_key}>',
            # rf'\g<{self.literal_A_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_A_key}>',
            # rf'\g<{self.option_A_key}>',
            # rf'\g<{self.added_option_A_key}>'
            # rf'\g<{self.literal_B_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_B_key}>',
            # rf'\g<{self.option_B_key}>',
            # rf'\g<{self.literal_C_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_C_key}>',
            # rf'\g<{self.option_C_key}>',
            # rf'\g<{self.literal_D_key}>',
            # self.output_punctuation,
            # rf'\g<{self.accent_mark_D_key}>',
            # rf'\g<{self.option_D_key}>',
            # rf'\g<{self.pandoc_comment_key}>',
        )

        self.output_multiline_list = [
            self.numeral_search_key,
            self.output_punctuation,
            self.accent_mark_numeral_key,
            self.accent_prompt_key,
            self.prompt_key,
            self.accent_mark_post_numeral_key,
            self.added_prompt_text_key,
            self.new_line_A_key,
            self.literal_A_key,
            self.output_punctuation,
            self.accent_mark_A_key,
            self.option_A_key,
            self.added_option_A_key,
            self.new_line_B_key,
            self.literal_B_key,
            self.output_punctuation,
            self.accent_mark_B_key,
            self.option_B_key,
            self.added_option_B_key,
            self.new_line_C_key,
            self.literal_C_key,
            self.output_punctuation,
            self.accent_mark_C_key,
            self.option_C_key,
            self.added_option_C_key,
            self.new_line_D_key,
            self.literal_D_key,
            self.output_punctuation,
            self.accent_mark_D_key,
            self.option_D_key,
            self.added_option_D_key,
            # self.pandoc_comment_key
        ]

        # Singleline option regex
        self.singleline_option_pattern = {
            self.accent_mark_numeral_key : self.accent_mark,
            self.numeral_search_key : self.numeral_character,
            self.punctuation_numeral_key : self.punctuation_separator,
            self.accent_mark_post_numeral_key : self.accent_mark,
            self.empty_space_numeral_key : self.space_but_new_line,
            self.accent_prompt_key : self.accent_mark,
            self.prompt_key : self.one_line_dotall,
            self.added_prompt_text_key : self.get_interine_text(self.literal_A_character),
            self.new_line_A_key : self.new_line,
            self.accent_mark_A_key : self.accent_mark,
            self.literal_A_key : self.literal_A_character,
            self.punctuation_separator_A_key : self.punctuation_separator,
            self.empty_space_A_key : self.space_but_new_line,
            self.option_A_key : self.one_line_dotall,
            self.new_line_B_key : self.new_line,
            self.accent_mark_B_key : self.accent_mark,
            self.literal_B_key : self.literal_B_character,
            self.punctuation_separator_B_key : self.punctuation_separator,
            self.empty_space_B_key : self.space_but_new_line,
            self.option_B_key : self.one_line_dotall,
            self.new_line_C_key : self.new_line,
            self.accent_mark_C_key : self.accent_mark,
            self.literal_C_key : self.literal_C_character,
            self.punctuation_separator_C_key : self.punctuation_separator,
            self.empty_space_C_key : self.space_but_new_line,
            self.option_C_key : self.one_line_dotall,
            self.new_line_D_key : self.new_line,
            self.accent_mark_D_key : self.accent_mark,
            self.literal_D_key : self.literal_D_character,
            self.punctuation_separator_D_key : self.punctuation_separator,
            self.empty_space_D_key : self.space_but_new_line,
            self.option_D_key : self.one_line_dotall,
        }
    
        self.output_singleline_option_list = [
            self.numeral_search_key,
            self.output_punctuation,
            self.accent_mark_numeral_key,
            self.accent_prompt_key,
            self.prompt_key,
            self.accent_mark_post_numeral_key,
            self.added_prompt_text_key,
            self.new_line_A_key,
            self.literal_A_key,
            self.output_punctuation,
            self.accent_mark_A_key,
            self.option_A_key,
            self.new_line_B_key,
            self.literal_B_key,
            self.output_punctuation,
            self.accent_mark_B_key,
            self.option_B_key,
            self.new_line_C_key,
            self.literal_C_key,
            self.output_punctuation,
            self.accent_mark_C_key,
            self.option_C_key,
            self.new_line_D_key,
            self.literal_D_key,
            self.output_punctuation,
            self.accent_mark_D_key,
            self.option_D_key,
        ]

    def build_search_pattern(self, *args):
        search_pattern=""
        for arg in args:
            search_pattern += rf'{arg}'
        return rf'{search_pattern}'

    def get_interine_text(self, literal_match):
        return (
            rf'.+?(?={self.new_line}'
            rf'{self.accent_mark}{literal_match}{self.punctuation_separator}'
            rf'{self.space_but_new_line}{self.one_line_dotall})'
        )

    def build_group_atomic_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>(?>{search_pattern}))'

    def build_group_simple_regex(self, pattern_name, search_pattern):
        return rf'(?P<{pattern_name}>{search_pattern})'