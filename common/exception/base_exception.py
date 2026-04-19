from ..constant.message_constant import MessageConstant


class BaseException(Exception):
    def __init__(self, message=None):
        super().__init__(message or MessageConstant.UNKNOWN_ERROR.value)


class Account_ALREADY_EXISTS(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        else:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message or MessageConstant.ALREADY_EXISTS.value)
            self.message = message or MessageConstant.ALREADY_EXISTS.value

class AccountNotFoundException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用ACCOUNT_NOT_FOUND消息
            super().__init__(MessageConstant.ACCOUNT_NOT_FOUND.value)
            self.message = MessageConstant.ACCOUNT_NOT_FOUND.value

class AccountLockedException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用ACCOUNT_LOCKED消息
            super().__init__(MessageConstant.ACCOUNT_LOCKED.value)
            self.message = MessageConstant.ACCOUNT_LOCKED.value


class PasswordErrorException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用PASSWORD_ERROR消息
            super().__init__(MessageConstant.PASSWORD_ERROR.value)
            self.message = MessageConstant.PASSWORD_ERROR.value


class UserNotLoginException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用USER_NOT_LOGIN消息
            super().__init__(MessageConstant.USER_NOT_LOGIN.value)
            self.message = MessageConstant.USER_NOT_LOGIN.value


class LoginFailedException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用LOGIN_FAILED消息
            super().__init__(MessageConstant.LOGIN_FAILED.value)
            self.message = MessageConstant.LOGIN_FAILED.value


class UploadFailedException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用UPLOAD_FAILED消息
            super().__init__(MessageConstant.UPLOAD_FAILED.value)
            self.message = MessageConstant.UPLOAD_FAILED.value


class SetmealEnableFailedException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用SETMEAL_ENABLE_FAILED消息
            super().__init__(MessageConstant.SETMEAL_ENABLE_FAILED.value)
            self.message = MessageConstant.SETMEAL_ENABLE_FAILED.value


class PasswordEditFailedException(BaseException):
    def __init__(self, message=None):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        elif message:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message
        else:
            # 默认使用PASSWORD_EDIT_FAILED消息
            super().__init__(MessageConstant.PASSWORD_EDIT_FAILED.value)
            self.message = MessageConstant.PASSWORD_EDIT_FAILED.value


class DeletionNotAllowedException(BaseException):
    def __init__(self, message):
        if message and hasattr(message, 'value'):
            # 如果传入的是MessageConstant枚举，使用其value
            super().__init__(message.value)
            self.message = message.value
        else:
            # 如果传入的是普通字符串，直接使用
            super().__init__(message)
            self.message = message