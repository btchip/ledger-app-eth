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

parser = argparse.ArgumentParser()
parser.add_argument('--path', help="BIP 32 path to retrieve")
parser.add_argument('--display', help="Display address", action="store_true")
args = parser.parse_args()

if args.path == None:
	args.path = "21323'/0"

donglePath = parse_bip32_path(args.path)
apdu = struct.pack(">BBBBBB", 0xf0, 0x02, 0x01 if args.display else 0x00, 0x00, len(donglePath) + 1, int(len(donglePath) / 4)) + donglePath

dongle = getDongle(True)
result = dongle.exchange(bytes(apdu))

print("Public key " + str(binascii.hexlify(result)))

