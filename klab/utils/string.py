import re


class strUtils:
        '''
        Utility class for String Manipulation
        '''
        
        @staticmethod
        #TODO: Find a Cleaner way to do this. Replicate the Java implementation for this somehow
        def remove_escape_char(oldStr: str) -> str:
                """
                Converts sequences like '\\n', '\\:', '\\=' into their unescaped versions.
                Required to get the updated string for the PGP Key from the certificate
                """

                # Replaces \n with an actual newline
                newStr = oldStr.replace("\\n", "\n")
                # Replaces \: with :
                newStr = newStr.replace("\\:", ":")
                # Replaces \= with =
                newStr = newStr.replace("\\=", "=")
                # Replaces any \x with x, where x is any character
                newStr = re.sub(r'\\(.)', r'\1', newStr)
                return newStr