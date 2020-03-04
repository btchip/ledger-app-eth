def get_msg(instruction_type, vault0, vault1, amount0, amount1,
            nonce, expiration_timestamp):
    """
    Creates a message to sign on.
    """
    packed_message = instruction_type
    packed_message = packed_message * 2**31 + vault0
    packed_message = packed_message * 2**31 + vault1
    packed_message = packed_message * 2**63 + amount0
    packed_message = packed_message * 2**63 + amount1
    packed_message = packed_message * 2**31 + nonce
    packed_message = packed_message * 2**22 + expiration_timestamp
    return packed_message

msg = get_msg(1, 1, 1, 100000, 0, 3434, 5656)
print(msg)
print(hex(msg)[2:].zfill(64))


