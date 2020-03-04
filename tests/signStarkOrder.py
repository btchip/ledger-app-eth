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
parser.add_argument('--contractSell', help="Contract address of the token to be sold (hex) or none for ETH")
parser.add_argument('--descriptorSell', help="ERC 20 signed descriptor of the token to be sold (hex)")
parser.add_argument('--quantumSell', help="Quantization of the token to be sold", default=1)
parser.add_argument('--contractBuy', help="Contract address of the token to be bought (hex) or none for ETH")
parser.add_argument('--descriptorBuy', help="ERC 20 signed descriptor of the token to be bought (hex)")
parser.add_argument('--quantumBuy', help="Quantization of the token to be bought", default=1)
parser.add_argument('--sourceVault', help="ID of the source vault")
parser.add_argument('--destinationVault', help="ID of the destination vault")
parser.add_argument('--amountSell', help="Amount to be sold")
parser.add_argument('--amountBuy', help="Amount to be bought")
parser.add_argument('--nonce', help="Transaction nonce")
parser.add_argument('--timestamp', help="Transaction timestamp")

args = parser.parse_args()

if args.path == None:
	args.path = "21323'/0"

dongle = getDongle(True)

if args.descriptorSell != None:
	descriptor = binascii.unhexlify(args.descriptorSell)
	apdu = struct.pack(">BBBBB", 0xE0, 0x0A, 0x00, 0x00, len(descriptor)) + descriptor
	dongle.exchange(bytes(apdu))

if args.descriptorBuy != None:
	descriptor = binascii.unhexlify(args.descriptorBuy)
	apdu = struct.pack(">BBBBB", 0xE0, 0x0A, 0x00, 0x00, len(descriptor)) + descriptor
	dongle.exchange(bytes(apdu))

if args.contractSell == None:
	args.contractSell = "00"*20
if args.contractBuy == None:
	args.contractBuy = "00"*20	

donglePath = parse_bip32_path(args.path)
apduData = binascii.unhexlify(args.contractSell) + encode_256_be(args.quantumSell)
apduData += binascii.unhexlify(args.contractBuy) + encode_256_be(args.quantumBuy)
apduData += struct.pack(">IIQQII", int(args.sourceVault), int(args.destinationVault), int(args.amountSell), int(args.amountBuy), int(args.nonce), int(args.timestamp))
apdu = struct.pack(">BBBBBB", 0xf0, 0x04, 0x01, 0x00, len(donglePath) + 1 + len(apduData), int(len(donglePath) / 4)) + donglePath + apduData


result = dongle.exchange(bytes(apdu))

print("Signature " + str(binascii.hexlify(result)))

