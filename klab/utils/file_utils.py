from pathlib import Path

class FileUtils:
    
    @staticmethod
    def parseCertFile(cert_filepath:str= Path.home() / ".klab" / "klab.cert")->dict:
            '''
            Parses a key=value formatted certificate file.
            Args:
                path (str): Path to the certificate file.
            Returns:
                dict: A dictionary with key-value pairs from the file.
            '''
            cert_dict = {}
            with open(cert_filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "=" not in line or line.startswith("#"):
                        continue  # skip empty lines, comments, or malformed lines
                    key, value = line.split("=", 1)
                    cert_dict[key.strip()] = value.strip()
            return cert_dict