#!/usr/bin/env python
"""
*******************************************************************************
*   Ledger Blue
*   (c) 2016 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
import argparse
import struct
import binascii

def parse_bip32_path(path):
	if len(path) == 0:
		return bytes() 
	result = bytes() 
	elements = path.split('/')
	for pathElement in elements:
		element = pathElement.split('\'')
		if len(element) == 1:
			result = result + struct.pack(">I", int(element[0]))			
		else:
			result = result + struct.pack(">I", 0x80000000 | int(element[0]))
	return result

def encode_256_be(num):	
	return binascii.unhexlify(hex(int(num))[2:].zfill(64))

parser = argparse.ArgumentParser()
parser.add_argument('--path', help="BIP 32 path to retrieve")
parser.add_argument('--contractTransfer', help="Contract address of the token to be transferred (hex) or none for ETH")
parser.add_argument('--descriptorTransfer', help="ERC 20 signed descriptor of the token to be transferred (hex)")
parser.add_argument('--quantumTransfer', help="Quantization of the token to be transferred", default=1)
parser.add_argument('--remoteKey', help="Remote Stark key to transfer to")
parser.add_argument('--sourceVault', help="ID of the source vault")
parser.add_argument('--destinationVault', help="ID of the destination vault")
parser.add_argument('--amountTransfer', help="Amount to be transferred")
parser.add_argument('--nonce', help="Transaction nonce")
parser.add_argument('--timestamp', help="Transaction timestamp")

args = parser.parse_args()

if args.path == None:
	args.path = "21323'/0"

dongle = getDongle(True)

if args.descriptorTransfer != None:
	descriptor = binascii.unhexlify(args.descriptorTransfer)
	apdu = struct.pack(">BBBBB", 0xE0, 0x0A, 0x00, 0x00, len(descriptor)) + descriptor
	dongle.exchange(bytes(apdu))

if args.contractTransfer == None:
	args.contractTransfer = "00"*20

donglePath = parse_bip32_path(args.path)
apduData = binascii.unhexlify(args.contractTransfer) + encode_256_be(args.quantumTransfer)
apduData += binascii.unhexlify(args.remoteKey)
apduData += struct.pack(">IIQII", int(args.sourceVault), int(args.destinationVault), int(args.amountTransfer), int(args.nonce), int(args.timestamp))
apdu = struct.pack(">BBBBBB", 0xf0, 0x04, 0x02, 0x00, len(donglePath) + 1 + len(apduData), int(len(donglePath) / 4)) + donglePath + apduData


result = dongle.exchange(bytes(apdu))

print("Signature " + str(binascii.hexlify(result)))

