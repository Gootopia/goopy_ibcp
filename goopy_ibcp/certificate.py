# ssl_context.py
import ssl
from enum import Enum
from pathlib import Path
from dataclasses import dataclass


class CertificateError(Enum):
    Ok = 0,
    Invalid_Path = 1    # path is wrong or filename is bad
    Invalid_Certificate = 2    # ssl library doesn't consider file a good ssl_context


@dataclass
class CertificateReturn:
    """Information about an attempt to get a certificate"""
    ssl_context: ssl.SSLContext = None
    error: CertificateError = CertificateError.Ok
    error_msg: str = ''


# TODO: Add functionality to create SSL certificates
class Certificate:
    """ Instructions on how to make a ssl_context
    See: https://talkdotnet.wordpress.com/2019/08/07/generating-a-pem-private-and-public-certificate-with-openssl-on-windows/
    also see: https://adamtheautomator.com/openssl-windows-10/
    Perform the following in the same directory as this .py module
    1) openssl req -x509 -newkey rsa:4096 -keyout {keyname}.pem -out {publickey_name}.pem -nodes
    2) openssl x509 -outform der -in {publickey_name}.pem -out {publickey_name}.crt
    """
    @staticmethod
    def get_certificate(use_default=True, certificate_path='') -> CertificateReturn:
        """ Obtain a ssl_context for use in SSL operations.

        Parameters:
            - use_default (bool=True): True=>find and use local certifications (ignore any certificate path provided)
            - certificate_path (str=''): File path to the specific certificate (i.e: .pem).

        Returns:
            - CertificateError.InvalidPath => Bad path or file does not exist        
        """

        result = CertificateReturn()

        if Path(certificate_path).exists() is not True:
            result.error = CertificateError.Invalid_Path
            return result

        try:
            new_context = ssl.create_default_context()
            #new_context.verify_mode=ssl.CERT_REQUIRED            
            new_context.check_hostname = False
            new_context.verify_mode=ssl.CERT_NONE
            new_context.load_default_certs()
            result.ssl_context = new_context

        except ssl.SSLError as e:
            result.ssl_context = None
            result.error = CertificateError.Invalid_Certificate
            result.error_msg = e.args[0]
            pass
        except Exception as e:
            result.ssl_context = None
            result.error_msg = e.args[0]
            pass
        finally:
            return result

if __name__ == '__main__':
    pass