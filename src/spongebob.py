class SpongebobClass():

    def spongebob_format(self, text):
        lower_txt = text.lower()

        upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        txt_list = [char for char in lower_txt]

        string_builder = []
        character_flag = False
        for char in txt_list:
            if not char.isalpha():
                string_builder.append(char)
                continue

            if character_flag:
                idx = lower.index(char)
                string_builder.append(upper[idx])
            else:
                string_builder.append(char)

            character_flag = not character_flag

        return ''.join(string_builder)