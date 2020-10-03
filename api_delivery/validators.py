import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):

    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
    #valid_extensions = ['.png', '.jpeg', '.jpg', '.git']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

def validate_image(image):
    file_size = image.file.size  # bite 사이즈로 들어옴

    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
       raise ValidationError("Max size of file is %s MB" % limit_mb)