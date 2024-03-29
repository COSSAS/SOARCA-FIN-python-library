from enum import Enum


class VariableTypeEnum(str, Enum):
    bool = "bool"
    dictionary = "dictionary"
    float = "float"
    hexstring = "hexstring"
    integer = "integer"
    ipv4_addr = "ipv4-addr"
    ipv6_addr = "ipv6-addr"
    long = "long"
    mac_addr = "mac-addr"
    hash = "hash"
    md5_hash = "md5-hash"
    sha256_hash = "sha256-hash"
    string = "string"
    uri = "uri"
    uuid = "uuid"
