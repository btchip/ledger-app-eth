#ifdef HAVE_STARKWARE

#include "shared_context.h"
#include "stark_utils.h"

static unsigned char const C_cx_Stark256_n[]  = {
  //n: 0x0800000000000010ffffffffffffffffb781126dcae7b2321e66a241adc64d2f
  0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
  0xb7, 0x81, 0x12, 0x6d, 0xca, 0xe7, 0xb2, 0x32, 0x1e, 0x66, 0xa2, 0x41, 0xad, 0xc6, 0x4d, 0x2f};

void starkDerivePrivateKey(uint32_t *bip32Path, uint32_t bip32PathLength, uint8_t *privateKeyData) {  
  // Sanity check 
  if (bip32Path[0] != STARK_BIP32_PATH_0)  {
    PRINTF("Invalid Stark derivation path %d\n", bip32Path[0]);
    THROW(0x6a80);
  }
  os_perso_derive_node_bip32(CX_CURVE_256K1, bip32Path, bip32PathLength, privateKeyData, NULL);  
  PRINTF("Private key before processing %.*H\n", 32, privateKeyData);
  // TODO - support additional schemes
  cx_math_modm(privateKeyData, 32, C_cx_Stark256_n, 32);
  PRINTF("Private key after processing %.*H\n", 32, privateKeyData);
}

void stark_get_amount_string(uint8_t *contractAddress, uint8_t *quantum256, uint8_t *amount64, char *tmp100, char *target100) {
  uint256_t amountPre, quantum, amount;
  uint8_t decimals;    
  char *ticker = (char*)PIC(chainConfig->coinName);  

  PRINTF("stark_get_amount_string %.*H\n", 20, contractAddress);

  if (allzeroes(contractAddress, 20)) {
    decimals = WEI_TO_ETHER;
    PRINTF("stark_get_amount_string - ETH\n");
  }
  else {
    tokenDefinition_t *token = getKnownToken(contractAddress);
    if (token == NULL) { // caught earlier
      THROW(0x6A80);
    }
    decimals = token->decimals;
    ticker = token->ticker;
    PRINTF("stark_get_amount_string - decimals %d ticker %s\n", decimals, ticker);
  }
  convertUint256BE(amount64, 8, &amountPre);
  readu256BE(quantum256, &quantum);
  mul256(&amountPre, &quantum, &amount);
  tostring256(&amount, 10, tmp100, 100);
  PRINTF("stark_get_amount_string - mul256 %s\n", tmp100);
  strcpy(target100, ticker);
  adjustDecimals(tmp100, strlen(tmp100), target100 + strlen(ticker), 100, decimals);
  PRINTF("get_amount_string %s\n", target100);
}


#endif // HAVE_STARK
