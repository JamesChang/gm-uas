# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='res_captcha.proto',
  package='',
  serialized_pb='\n\x11res_captcha.proto\"_\n\x12\x43\x61ptchaNewResponse\x12\x14\n\x0c\x63\x61ptcha_link\x18\x01 \x01(\t\x12\x15\n\rcaptcha_token\x18\x02 \x01(\t\x12\x1c\n\x14\x63\x61ptcha_simple_token\x18\x03 \x01(\tB\x12\n\x0eproto.responseH\x02')




_CAPTCHANEWRESPONSE = descriptor.Descriptor(
  name='CaptchaNewResponse',
  full_name='CaptchaNewResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='captcha_link', full_name='CaptchaNewResponse.captcha_link', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='captcha_token', full_name='CaptchaNewResponse.captcha_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='captcha_simple_token', full_name='CaptchaNewResponse.captcha_simple_token', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=21,
  serialized_end=116,
)



class CaptchaNewResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CAPTCHANEWRESPONSE
  
  # @@protoc_insertion_point(class_scope:CaptchaNewResponse)

# @@protoc_insertion_point(module_scope)
