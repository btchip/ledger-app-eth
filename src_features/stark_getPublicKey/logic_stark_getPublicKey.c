#ifdef HAVE_STARKWARE

#include "shared_context.h"

uint32_t set_result_get_stark_publicKey() {
    uint32_t tx = 0;
    os_memmove(G_io_apdu_buffer + tx, tmpCtx.publicKeyContext.publicKey.W + 1, 32);
    tx += 32;
    return tx;
}

#endif


