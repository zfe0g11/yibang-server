import hashlib

class PasswordUtil:
    @staticmethod
    def encrypt(password: str) -> str:
        """
        对密码进行MD5加密
        :param password: 原始密码
        :return: 加密后的密码
        """
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @staticmethod
    def matches(encrypted_password: str, password: str) -> bool:
        """
        验证密码是否匹配
        :param encrypted_password: 加密后的密码
        :param password: 原始密码
        :return: 是否匹配
        """
        return encrypted_password == hashlib.md5(password.encode('utf-8')).hexdigest()